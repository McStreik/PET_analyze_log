import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Функция для парсинга логов
def parse_log_file(file_path):
    log_pattern = r'(\S+)\s+-\s+-\s+\[(.*?)\]\s+"(.*?)"\s+(\d{3})\s+(\d+|-)'    
    logs = []

    with open(file_path, "r") as f:
        for line in f:
            match = re.match(log_pattern, line)
            if match:
                ip, timestamp, request, status, size = match.groups()
                method, url, protocol = request.split()
                logs.append(
                    {
                        "ip": ip,
                        "timestamp": timestamp,
                        "method": method,
                        "url": url,
                        "status": int(status),
                        "size": int(size) if size != "-" else 0,
                    }
                )
    df = pd.DataFrame(logs)

        # Проверяем, что все необходимые столбцы присутствуют
    required_columns = {'ip', 'timestamp', 'method', 'url', 'status', 'size'}
    if not required_columns.issubset(df.columns):
        missing_columns = required_columns - set(df.columns)
        raise ValueError(f"Отсутствуют необходимые столбцы: {missing_columns}")
    
    return df


# Функция для очистки данных


def clean_data(df):
    # Преобразование timestamp в datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d/%b/%Y:%H:%M:%S %z")

    # Удаление дубликатов
    df.drop_duplicates(inplace=True)

    # Фильтрация некорректных значений
    df = df[df["status"] >= 200]
    df = df[df["status"] < 600]

    return df


# Функция для анализа данных
def analyze_data(df):
    # Топ 10 свмых популярных страниц
    top_pages = df["url"].value_counts().head(10)

    # Количество ошибок 404
    errors_404 = df[df["status"] == 404]

    # Распределение трафика по часам
    df["hour"] = df["timestamp"].dt.hour
    traffic_by_hour = df["hour"].value_counts().sort_index()

    # Средний размер ответа
    average_response_size = df["size"].mean()

    return top_pages, errors_404, traffic_by_hour, average_response_size


# Функция для визуализации результатов
def visualize_data(top_pages, traffic_by_hoour):
    # График топ 10 страниц
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_pages.values, y=top_pages.index, palette="viridis")
    plt.title("Топ 10 самых популярных страниц")
    plt.xlabel("Количество запросов")
    plt.ylabel("URL")
    plt.show()

    # График распределения трафика по часам
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=traffic_by_hoour.index, y=traffic_by_hoour.values, markers="o")
    plt.title("Распределение трафика по часам")
    plt.xlabel("Час")
    plt.ylabel("Количество запросов")
    plt.grid(True)
    plt.show()


# Основная функция
if __name__ == "__main__":
    # Путь к файлу с логами
    log_file_path = "access.log"

    # Чтение и парсинг логов
    print("Чтение и парсинг логов...")
    try:
        df = parse_log_file(log_file_path)
    except ValueError as e:
        print(f"Ошибка при парсинге логов: {e}")
        exit()

    # Очистка данных
    print("Очистка данных...")
    df = clean_data(df)

    # Анализ данных
    print("Анализ данных...")
    top_pages, errors_404, traffic_by_hour, average_response_size = analyze_data(df)

    # Вывод результатов
    print("\nТоп 10 страниц:")
    print(top_pages)

    print("\nКоличество ошибок 404:")
    print(len(errors_404))

    print(f"\nСредний размер ответа: {average_response_size:.2f} байт")

    # Визуализация данных
    print("Визуализация данных...")
    visualize_data(top_pages, traffic_by_hour)
