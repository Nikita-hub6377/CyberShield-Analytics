import os
import pandas as pd


# ==================================================
# CYBERSHIELD ANALYTICS
# MASTER ML DATASET CREATION
# ==================================================

print("=" * 60)
print("CYBERSHIELD ANALYTICS - MASTER ML DATASET")
print("=" * 60)


# --------------------------------------------------
# STEP 1: LOAD PROCESSED DATA
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/cybersecurity_processed.csv"
)

print("\nProcessed dataset loaded!")
print("Shape:", df.shape)


# --------------------------------------------------
# STEP 2: LOAD FULL RANDOM FOREST PREDICTIONS
# --------------------------------------------------

rf_df = pd.read_csv(
    "outputs/ml/full_incident_predictions.csv"
)

print("Full Random Forest predictions loaded!")
print("Shape:", rf_df.shape)


# --------------------------------------------------
# STEP 3: SELECT RANDOM FOREST RESULTS
# --------------------------------------------------

rf_selected = rf_df[
    [
        "incident_id",
        "predicted_risk_level",
        "priority",
        "model_confidence",
        "confidence_level"
    ]
].copy()


# --------------------------------------------------
# STEP 4: MERGE RANDOM FOREST RESULTS
# --------------------------------------------------

master_df = df.merge(
    rf_selected,
    on="incident_id",
    how="left"
)


# --------------------------------------------------
# STEP 5: LOAD ANOMALY RESULTS
# --------------------------------------------------

anomaly_df = pd.read_csv(
    "outputs/ml/anomaly_detection_results.csv"
)

print("Anomaly results loaded!")
print("Shape:", anomaly_df.shape)


# --------------------------------------------------
# STEP 6: SELECT ANOMALY RESULTS
# --------------------------------------------------

anomaly_selected = anomaly_df[
    [
        "incident_id",
        "anomaly_prediction",
        "anomaly_status",
        "anomaly_score",
        "anomaly_reason"
    ]
].copy()


# --------------------------------------------------
# STEP 7: MERGE ANOMALY RESULTS
# --------------------------------------------------

master_df = master_df.merge(
    anomaly_selected,
    on="incident_id",
    how="left"
)


# --------------------------------------------------
# STEP 8: LOAD RISK MONITORING RESULTS
# --------------------------------------------------

risk_monitoring_df = pd.read_csv(
    "data/processed/risk_monitoring_results.csv"
)

print("Risk monitoring results loaded!")
print("Shape:", risk_monitoring_df.shape)


# --------------------------------------------------
# STEP 9: SELECT RISK MONITORING RESULTS
# --------------------------------------------------

risk_monitoring_selected = risk_monitoring_df[
    [
        "incident_id",
        "monitored_risk_level",
        "previous_risk_score",
        "risk_change",
        "risk_change_status",
        "early_warning",
        "risk_comparison"
    ]
].copy()


# --------------------------------------------------
# STEP 10: MERGE RISK MONITORING RESULTS
# --------------------------------------------------

master_df = master_df.merge(
    risk_monitoring_selected,
    on="incident_id",
    how="left"
)


# --------------------------------------------------
# STEP 11: CHECK MISSING VALUES
# --------------------------------------------------

print("\nMissing Random Forest values:")

print(
    master_df[
        [
            "predicted_risk_level",
            "priority",
            "model_confidence",
            "confidence_level"
        ]
    ].isna().sum()
)


print("\nMissing Anomaly values:")

print(
    master_df[
        [
            "anomaly_prediction",
            "anomaly_status",
            "anomaly_score"
        ]
    ].isna().sum()
)


print("\nMissing Risk Monitoring values:")

print(
    master_df[
        [
            "monitored_risk_level",
            "risk_change",
            "risk_change_status",
            "early_warning",
            "risk_comparison"
        ]
    ].isna().sum()
)


# --------------------------------------------------
# STEP 12: SAVE MASTER DATASET
# --------------------------------------------------

output_dir = "outputs/ml"

os.makedirs(
    output_dir,
    exist_ok=True
)

output_path = (
    "outputs/ml/cybershield_master_ml_dataset.csv"
)

master_df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# STEP 13: DISPLAY FINAL RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("MASTER DATASET CREATED SUCCESSFULLY!")
print("=" * 60)

print("\nFinal Shape:", master_df.shape)

print("\nFinal ML columns:")

print(
    master_df[
        [
            "risk_score",
            "risk_level",
            "predicted_risk_level",
            "priority",
            "model_confidence",
            "confidence_level",
            "anomaly_status",
            "anomaly_score",
            "anomaly_reason",
            "monitored_risk_level",
            "risk_change",
            "risk_change_status",
            "early_warning",
            "risk_comparison"
        ]
    ].head(10).to_string(index=False)
)

print("\nSaved to:")
print(output_path)

print("\n" + "=" * 60)
print("CYBERSHIELD ANALYTICS MASTER DATASET READY!")
print("=" * 60)