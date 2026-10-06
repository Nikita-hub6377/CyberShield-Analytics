import os
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder


# ==================================================
# CYBERSHIELD ANALYTICS
# FULL DATASET RISK PREDICTION
# ==================================================

print("=" * 60)
print("CYBERSHIELD ANALYTICS - FULL INCIDENT PREDICTION")
print("=" * 60)


# --------------------------------------------------
# STEP 1: LOAD PROCESSED DATASET
# --------------------------------------------------

data_path = "data/processed/cybersecurity_processed.csv"

df = pd.read_csv(data_path)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)


# --------------------------------------------------
# STEP 2: LOAD TRAINED MODEL
# --------------------------------------------------

model_path = "models/random_forest_model.pkl"
encoder_path = "models/risk_level_encoder.pkl"

model = joblib.load(model_path)
target_encoder = joblib.load(encoder_path)

print("\nRandom Forest model loaded successfully!")
print("Risk level encoder loaded successfully!")


# --------------------------------------------------
# STEP 3: SELECT EXACT TRAINING FEATURES
# --------------------------------------------------

feature_columns = [
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

X = df[feature_columns].copy()


# --------------------------------------------------
# STEP 4: ENCODE CATEGORICAL FEATURES
# --------------------------------------------------

categorical_columns = X.select_dtypes(
    include=["object", "string"]
).columns

print("\nEncoding categorical features:")

for column in categorical_columns:

    encoder = LabelEncoder()

    encoder.fit(df[column])

    X[column] = encoder.transform(X[column])

    print(column, "encoded successfully")


# --------------------------------------------------
# STEP 5: GENERATE PREDICTIONS
# --------------------------------------------------

predictions_encoded = model.predict(X)

df["predicted_risk_level"] = (
    target_encoder.inverse_transform(
        predictions_encoded
    )
)


# --------------------------------------------------
# STEP 6: CALCULATE MODEL CONFIDENCE
# --------------------------------------------------

prediction_probabilities = model.predict_proba(X)

df["model_confidence"] = (
    prediction_probabilities.max(axis=1) * 100
).round(2)


# --------------------------------------------------
# STEP 7: CONFIDENCE LEVEL
# --------------------------------------------------

def assign_confidence_level(confidence):

    if confidence >= 80:
        return "High"

    elif confidence >= 60:
        return "Medium"

    else:
        return "Low"


df["confidence_level"] = (
    df["model_confidence"]
    .apply(assign_confidence_level)
)


# --------------------------------------------------
# STEP 8: INCIDENT PRIORITY
# --------------------------------------------------

def assign_priority(score):

    if score >= 80:
        return "Critical"

    elif score >= 67:
        return "High"

    elif score >= 34:
        return "Medium"

    else:
        return "Low"


df["priority"] = (
    df["risk_score"]
    .apply(assign_priority)
)


# --------------------------------------------------
# STEP 9: SAVE FULL PREDICTIONS
# --------------------------------------------------

output_dir = "outputs/ml"

os.makedirs(
    output_dir,
    exist_ok=True
)

output_path = os.path.join(
    output_dir,
    "full_incident_predictions.csv"
)

df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# STEP 10: DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 60)
print("FULL INCIDENT PREDICTION COMPLETED!")
print("=" * 60)

print("\nTotal incidents predicted:", len(df))

print("\nPredicted Risk Distribution:")
print(
    df["predicted_risk_level"]
    .value_counts()
)

print("\nConfidence Distribution:")
print(
    df["confidence_level"]
    .value_counts()
)

print("\nPriority Distribution:")
print(
    df["priority"]
    .value_counts()
)

print("\nSample Predictions:")

print(
    df[
        [
            "incident_id",
            "risk_score",
            "risk_level",
            "predicted_risk_level",
            "model_confidence",
            "confidence_level",
            "priority"
        ]
    ].head(10).to_string(index=False)
)

print("\nOutput saved to:")
print(output_path)

print("\n" + "=" * 60)
print("ALL 3000 INCIDENTS PROCESSED SUCCESSFULLY!")
print("=" * 60)