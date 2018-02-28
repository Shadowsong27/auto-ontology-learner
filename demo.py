import pandas as pd


print("read data")
for chunk in pd.read_csv(r'resources/Train.csv', chunksize=10000):
    print(chunk)
    break

