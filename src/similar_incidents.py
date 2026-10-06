import os
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

# ==================================================
# CYBERSHIELD ANALYTICS
# SIMILAR INCIDENT ANALYSIS
# ==================================================

print("=" * 60)
print("CYBERSHIELD ANALYTICS - SIMILAR INCIDENT ANALYSIS")
print("=" * 60)

# --------------------------------------------------
# STEP 1: LOAD THE PROCESSED DATASET
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/cybersecurity_processed.csv"
)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)

# --------------------------------------------------
# STEP 2: SELECT FEATURES FOR SIMILARITY
# --------------------------------------------------

similarity_features = [
    "financial_loss_million",
    "affected_users",
    "resolution_time_hours",
    "risk_score"
]

X = df[similarity_features].copy()

print("\nFeatures used for similarity analysis:")
print(similarity_features)

# --------------------------------------------------
# STEP 3: SCALE THE FEATURES
# --------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\nFeatures scaled successfully!")

# --------------------------------------------------
# STEP 4: CALCULATE SIMILARITY
# --------------------------------------------------

similarity_matrix = cosine_similarity(
    X_scaled
)

print("\nSimilarity matrix calculated successfully!")

# --------------------------------------------------
# STEP 5: SELECT A SAMPLE INCIDENT
# --------------------------------------------------

selected_index = 0

selected_incident = df.iloc[selected_index]

print("\nSelected Incident:")
print(
    selected_incident[
        [
            "incident_id",
            "country",
            "attack_type",
            "target_industry",
            "risk_score"
        ]
    ]
)

# --------------------------------------------------
# STEP 6: FIND TOP SIMILAR INCIDENTS
# --------------------------------------------------

similarity_scores = list(
    enumerate(
        similarity_matrix[selected_index]
    )
)

similarity_scores = sorted(
    similarity_scores,
    key=lambda x: x[1],
    reverse=True
)

# Remove the incident itself
similar_incident_indexes = [
    index
    for index, score in similarity_scores[1:6]
]

similar_incidents = df.iloc[
    similar_incident_indexes
].copy()

similar_incidents["similarity_score"] = [
    similarity_matrix[
        selected_index,
        index
    ]
    for index in similar_incident_indexes
]

print("\nTop 5 Similar Historical Incidents:")

print(
    similar_incidents[
        [
            "incident_id",
            "country",
            "attack_type",
            "target_industry",
            "financial_loss_million",
            "affected_users",
            "resolution_time_hours",
            "risk_score",
            "similarity_score"
        ]
    ]
)

# --------------------------------------------------
# STEP 7: SAVE RESULTS
# --------------------------------------------------

os.makedirs(
    "outputs/ml",
    exist_ok=True
)

similar_incidents.to_csv(
    "outputs/ml/similar_incidents.csv",
    index=False
)

print("\nSimilar incident results saved successfully!")
print(
    "Location: outputs/ml/similar_incidents.csv"
)
# --------------------------------------------------
# STEP 8: COMPARE CURRENT AND HISTORICAL INCIDENTS
# --------------------------------------------------

comparison_data = []

# Compare the selected incident with each similar incident
for _, row in similar_incidents.iterrows():
    comparison_data.append({
        "selected_incident_id": selected_incident["incident_id"],
        "similar_incident_id": row["incident_id"],

        "selected_financial_loss_million":
            selected_incident["financial_loss_million"],

        "historical_financial_loss_million":
            row["financial_loss_million"],

        "selected_affected_users":
            selected_incident["affected_users"],

        "historical_affected_users":
            row["affected_users"],

        "selected_resolution_time_hours":
            selected_incident["resolution_time_hours"],

        "historical_resolution_time_hours":
            row["resolution_time_hours"],

        "selected_risk_score":
            selected_incident["risk_score"],

        "historical_risk_score":
            row["risk_score"],

        "similarity_score":
            row["similarity_score"]
    })

# Create comparison DataFrame
comparison_df = pd.DataFrame(comparison_data)

print("\n" + "=" * 60)
print("CURRENT VS HISTORICAL INCIDENT COMPARISON")
print("=" * 60)

print("\nComparison Results:")
print(comparison_df)

# --------------------------------------------------
# STEP 9: SAVE COMPARISON RESULTS
# --------------------------------------------------

comparison_df.to_csv(
    "outputs/ml/incident_comparison.csv",
    index=False
)

print("\nIncident comparison saved successfully!")
print(
    "Location: outputs/ml/incident_comparison.csv"
)
# --------------------------------------------------
# STEP 6: CURRENT vs HISTORICAL INCIDENT COMPARISON
# --------------------------------------------------

print("\n" + "=" * 60)
print("CURRENT vs HISTORICAL INCIDENT COMPARISON")
print("=" * 60)

# Historical averages
historical_avg_risk = df["risk_score"].mean()
historical_avg_loss = df["financial_loss_million"].mean()
historical_avg_users = df["affected_users"].mean()
historical_avg_resolution = df[
    "incident_resolution_time_hours"
].mean()

print("\nHistorical Dataset Averages:")
print(f"Average Risk Score: {historical_avg_risk:.2f}")
print(f"Average Financial Loss: ${historical_avg_loss:.2f} Million")
print(f"Average Affected Users: {historical_avg_users:,.0f}")
print(f"Average Resolution Time: {historical_avg_resolution:.2f} Hours")

# Compare monitored incidents with historical averages
df["risk_vs_historical"] = (
    df["risk_score"] - historical_avg_risk
)

df["loss_vs_historical"] = (
    df["financial_loss_million"] - historical_avg_loss
)

df["users_vs_historical"] = (
    df["affected_users"] - historical_avg_users
)

df["resolution_vs_historical"] = (
    df["incident_resolution_time_hours"]
    - historical_avg_resolution
)

# Comparison status
def comparison_status(value):
    if value > 0:
        return "Above Historical Average"
    elif value < 0:
        return "Below Historical Average"
    else:
        return "Equal to Historical Average"


df["risk_comparison"] = df[
    "risk_vs_historical"
].apply(comparison_status)

print("\nRisk Comparison:")
print(
    df["risk_comparison"].value_counts()
)

# Display high-risk incidents compared with history
comparison = df[
    df["risk_score"] >= 67
][
    [
        "incident_id",
        "risk_score",
        "risk_comparison",
        "financial_loss_million",
        "affected_users",
        "incident_resolution_time_hours"
    ]
]

print("\nHigh-Risk Incidents Compared With Historical Data:")
print(comparison.head(10))

print("\nTotal High-Risk Incidents:")
print(len(comparison))

print("=" * 60)