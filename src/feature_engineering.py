import pandas as pd
from pathlib import Path

# File paths
input_path = Path("data/cleaned/cybersecurity_cleaned.csv")
output_path = Path("data/processed/cybersecurity_processed.csv")

# Load cleaned dataset
df = pd.read_csv(input_path)

print("Starting shape:", df.shape)

# -------------------------------------------------
# 1. Create a unique Incident ID
# -------------------------------------------------
df.insert(0, "incident_id", range(1, len(df) + 1))

# -------------------------------------------------
# 2. Create normalized risk components
# -------------------------------------------------
df["financial_loss_score"] = (
    df["financial_loss_million"] /
    df["financial_loss_million"].max()
) * 100

df["affected_users_score"] = (
    df["affected_users"] /
    df["affected_users"].max()
) * 100

df["resolution_time_score"] = (
    df["resolution_time_hours"] /
    df["resolution_time_hours"].max()
) * 100

# -------------------------------------------------
# 3. Create initial Risk Score (0-100)
# -------------------------------------------------
df["risk_score"] = (
    0.50 * df["financial_loss_score"] +
    0.30 * df["affected_users_score"] +
    0.20 * df["resolution_time_score"]
).round(2)

# -------------------------------------------------
# 4. Create Risk Level
# -------------------------------------------------
df["risk_level"] = pd.cut(
    df["risk_score"],
    bins=[-1, 33, 66, 100],
    labels=["Low", "Medium", "High"]
)

# -------------------------------------------------
# Save processed dataset
# -------------------------------------------------
df.to_csv(output_path, index=False)

print("Processed shape:", df.shape)
print("\nNew columns created:")
print([
    "incident_id",
    "financial_loss_score",
    "affected_users_score",
    "resolution_time_score",
    "risk_score",
    "risk_level"
])

print("\nRisk level distribution:")
print(df["risk_level"].value_counts())

print("\nProcessed dataset saved successfully!")
print("Location:", output_path)