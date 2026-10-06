import pandas as pd
from pathlib import Path

# Load dataset
data_path = Path("data/raw/Global_Cybersecurity_Threats_2015-2024.csv")
df = pd.read_csv(data_path)

print("=" * 60)
print("CYBERSHIELD ANALYTICS - DATA UNDERSTANDING REPORT")
print("=" * 60)

# 1. Dataset shape
print("\n1. DATASET SHAPE")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 2. Missing values
print("\n2. MISSING VALUES")
print(df.isnull().sum())

# 3. Duplicate rows
print("\n3. DUPLICATE ROWS")
print("Total duplicate rows:", df.duplicated().sum())

# 4. Data types
print("\n4. DATA TYPES")
print(df.dtypes)

# 5. Numerical statistics
print("\n5. NUMERICAL STATISTICS")
print(df.describe())

# 6. Year range
print("\n6. YEAR RANGE")
print("Minimum Year:", df["Year"].min())
print("Maximum Year:", df["Year"].max())

# 7. Unique values in categorical columns
categorical_columns = [
    "Country",
    "Attack Type",
    "Target Industry",
    "Attack Source",
    "Security Vulnerability Type",
    "Defense Mechanism Used"
]

print("\n7. UNIQUE VALUES IN CATEGORICAL COLUMNS")

for column in categorical_columns:
    print(f"\n--- {column} ---")
    print("Number of unique values:", df[column].nunique())
    print("Values:", df[column].unique())

print("\n" + "=" * 60)
print("DATA UNDERSTANDING COMPLETED SUCCESSFULLY")
print("=" * 60)
print("\n8. FULL NUMERICAL STATISTICS")

numerical_columns = [
    "Year",
    "Financial Loss (in Million $)",
    "Number of Affected Users",
    "Incident Resolution Time (in Hours)"
]

for column in numerical_columns:
    print(f"\n--- {column} ---")
    print(df[column].describe())

print("\n9. CHECK FOR NEGATIVE VALUES")

for column in numerical_columns[1:]:
    negative_count = (df[column] < 0).sum()
    print(f"{column}: {negative_count} negative values")