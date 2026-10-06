import pandas as pd
from pathlib import Path

# File paths
input_path = Path("data/raw/Global_Cybersecurity_Threats_2015-2024.csv")
output_path = Path("data/cleaned/cybersecurity_cleaned.csv")

# Load raw data
df = pd.read_csv(input_path)

print("Original shape:", df.shape)

# Remove accidental spaces from text columns
text_columns = df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# Remove duplicates as a safety check
df = df.drop_duplicates()

# Standardize column names for easier Python, SQL and ML work
df.columns = [
    "country",
    "year",
    "attack_type",
    "target_industry",
    "financial_loss_million",
    "affected_users",
    "attack_source",
    "vulnerability_type",
    "defense_mechanism",
    "resolution_time_hours"
]

# Save cleaned dataset
df.to_csv(output_path, index=False)

print("Cleaned shape:", df.shape)
print("Cleaned dataset saved successfully!")
print("Location:", output_path)