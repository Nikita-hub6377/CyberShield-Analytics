import pandas as pd
from pathlib import Path

# Correct location of the raw dataset
data_folder = Path("data/raw")

print("Files inside data/raw:")
for file in data_folder.iterdir():
    print("-", file.name)

# Find CSV files
files = list(data_folder.glob("*.csv"))

if not files:
    print("\nNo CSV file found inside data/raw.")
else:
    data_file = files[0]
    print(f"\nLoading: {data_file}")

    df = pd.read_csv(data_file)

    print("\nDataset loaded successfully!")

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nDataset Information:")
    df.info()