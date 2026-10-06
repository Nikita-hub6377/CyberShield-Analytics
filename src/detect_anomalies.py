import os
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ==================================================
# CYBERSHIELD ANALYTICS
# ANOMALY DETECTION USING ISOLATION FOREST
# ==================================================

print("=" * 60)
print("CYBERSHIELD ANALYTICS - ANOMALY DETECTION")
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
# STEP 2: SELECT FEATURES FOR ANOMALY DETECTION
# --------------------------------------------------

anomaly_features = [
    "financial_loss_million",
    "affected_users",
    "resolution_time_hours",
    "risk_score"
]

X = df[anomaly_features].copy()

print("\nFeatures selected for anomaly detection:")
print(anomaly_features)

# --------------------------------------------------
# STEP 3: SCALE THE FEATURES
# --------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\nFeatures scaled successfully!")

# --------------------------------------------------
# STEP 4: CREATE ISOLATION FOREST MODEL
# --------------------------------------------------

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# --------------------------------------------------
# STEP 5: DETECT ANOMALIES
# --------------------------------------------------

df["anomaly_prediction"] = model.fit_predict(
    X_scaled
)

# Convert Isolation Forest output:
# -1 = Anomaly
#  1 = Normal

df["anomaly_status"] = df[
    "anomaly_prediction"
].map({
    -1: "Anomaly",
    1: "Normal"
})

# --------------------------------------------------
# STEP 6: CREATE ANOMALY SCORE
# --------------------------------------------------

df["anomaly_score"] = (
    -model.decision_function(X_scaled)
).round(4)

# --------------------------------------------------
# STEP 7: DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("ANOMALY DETECTION COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nAnomaly Status Distribution:")
print(df["anomaly_status"].value_counts())

print("\nTotal Anomalies Detected:")
print(
    (df["anomaly_status"] == "Anomaly").sum()
)

print("\nTop 10 Most Unusual Incidents:")

top_anomalies = df[
    df["anomaly_status"] == "Anomaly"
].sort_values(
    by="anomaly_score",
    ascending=False
)

print(
    top_anomalies[
        [
            "incident_id",
            "country",
            "attack_type",
            "financial_loss_million",
            "affected_users",
            "resolution_time_hours",
            "risk_score",
            "anomaly_score",
            "anomaly_status"
        ]
    ].head(10)
)

# --------------------------------------------------
# STEP 8: SAVE ANOMALY RESULTS
# --------------------------------------------------

os.makedirs(
    "outputs/ml",
    exist_ok=True
)

df.to_csv(
    "outputs/ml/anomaly_detection_results.csv",
    index=False
)

print("\nAnomaly results saved successfully!")
print(
    "Location: outputs/ml/anomaly_detection_results.csv"
)
# --------------------------------------------------
# STEP 9: ANALYZE WHY INCIDENTS ARE UNUSUAL
# --------------------------------------------------

# Calculate the mean of each anomaly feature
feature_means = df[anomaly_features].mean()

# Create a function to explain unusual incidents
def explain_anomaly(row):
    reasons = []

    for feature in anomaly_features:
        mean_value = feature_means[feature]
        value = row[feature]

        # Check if the value is much higher than average
        if value > mean_value * 1.5:
            reasons.append(f"High {feature}")

        # Check if the value is much lower than average
        elif value < mean_value * 0.5:
            reasons.append(f"Low {feature}")

    if reasons:
        return ", ".join(reasons)

    return "Unusual combination of incident characteristics"


# Add anomaly reason only for anomalies
df["anomaly_reason"] = ""

anomaly_mask = df["anomaly_status"] == "Anomaly"

df.loc[
    anomaly_mask,
    "anomaly_reason"
] = df.loc[
    anomaly_mask
].apply(
    explain_anomaly,
    axis=1
)

print("\n" + "=" * 60)
print("ANOMALY REASON ANALYSIS COMPLETED!")
print("=" * 60)

print("\nSample Anomaly Explanations:")

print(
    df[
        df["anomaly_status"] == "Anomaly"
    ][
        [
            "incident_id",
            "anomaly_score",
            "anomaly_reason"
        ]
    ].head(10)
)

# Save updated anomaly results
df.to_csv(
    "outputs/ml/anomaly_detection_results.csv",
    index=False
)

print("\nUpdated anomaly results saved successfully!")