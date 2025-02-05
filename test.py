import pandas as pd
import numpy as np

# Создание простого DataFrame
data = {"A": [1, 2, 3], "B": [4, 5, 6]}
df = pd.DataFrame(data)

print("Pandas works:")
print(df)

print("\nNumpy works:")
print(np.array([1, 2, 3]))
