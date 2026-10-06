import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load processed dataset
data_path = Path("data/processed/cybersecurity_processed.csv")
df = pd.read_csv(data_path)

# Create output folder automatically
output_folder = Path("outputs/eda")
output_folder.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("CYBERSHIELD ANALYTICS - EDA")
print("=" * 60)

# 1. Basic summary
print("\nDataset Shape:", df.shape)

# 2. Attack type distribution
print("\nAttack Type Distribution:")
print(df["attack_type"].value_counts())

plt.figure(figsize=(8, 5))
df["attack_type"].value_counts().plot(kind="bar")
plt.title("Cybersecurity Incidents by Attack Type")
plt.xlabel("Attack Type")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "attack_type_distribution.png")
plt.close()

# 3. Target industry distribution
print("\nTarget Industry Distribution:")
print(df["target_industry"].value_counts())

plt.figure(figsize=(9, 5))
df["target_industry"].value_counts().plot(kind="bar")
plt.title("Cybersecurity Incidents by Target Industry")
plt.xlabel("Industry")
plt.ylabel("Number of Incidents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "industry_distribution.png")
plt.close()

# 4. Risk level distribution
print("\nRisk Level Distribution:")
print(df["risk_level"].value_counts())

plt.figure(figsize=(6, 5))
df["risk_level"].value_counts().plot(kind="bar")
plt.title("Incident Risk Level Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Number of Incidents")
plt.tight_layout()
plt.savefig(output_folder / "risk_level_distribution.png")
plt.close()

# 5. Incidents by year
year_counts = df["year"].value_counts().sort_index()

print("\nIncidents by Year:")
print(year_counts)

plt.figure(figsize=(8, 5))
plt.plot(year_counts.index, year_counts.values, marker="o")
plt.title("Cybersecurity Incidents by Year")
plt.xlabel("Year")
plt.ylabel("Number of Incidents")
plt.xticks(year_counts.index, rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "incidents_by_year.png")
plt.close()

# 6. Financial loss by attack type
loss_by_attack = (
    df.groupby("attack_type")["financial_loss_million"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Financial Loss by Attack Type:")
print(loss_by_attack)

plt.figure(figsize=(8, 5))
loss_by_attack.plot(kind="bar")
plt.title("Average Financial Loss by Attack Type")
plt.xlabel("Attack Type")
plt.ylabel("Average Loss (Million $)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "average_loss_by_attack_type.png")
plt.close()

# 7. Average risk score by industry
risk_by_industry = (
    df.groupby("target_industry")["risk_score"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Risk Score by Industry:")
print(risk_by_industry)

plt.figure(figsize=(9, 5))
risk_by_industry.plot(kind="bar")
plt.title("Average Risk Score by Target Industry")
plt.xlabel("Industry")
plt.ylabel("Average Risk Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_folder / "average_risk_by_industry.png")
plt.close()

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("Charts saved in: outputs/eda")
print("=" * 60)