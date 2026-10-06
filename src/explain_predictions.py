import os
import pandas as pd
import joblib
import shap
from sklearn.preprocessing import LabelEncoder


# ==================================================
# CYBERSHIELD ANALYTICS
# SHAP PREDICTION EXPLAINABILITY
# AND MODEL CONFIDENCE
# ==================================================

print("=" * 60)
print("CYBERSHIELD ANALYTICS - PREDICTION EXPLAINABILITY")
print("=" * 60)


# --------------------------------------------------
# STEP 1: LOAD PROCESSED DATASET
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/cybersecurity_processed.csv"
)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)


# --------------------------------------------------
# STEP 2: LOAD RANDOM FOREST MODEL
# --------------------------------------------------

model = joblib.load(
    "models/random_forest_model.pkl"
)

print("\nRandom Forest model loaded successfully!")


# Load target encoder
target_encoder = joblib.load(
    "models/risk_level_encoder.pkl"
)

print("Risk level encoder loaded successfully!")


# --------------------------------------------------
# STEP 3: SELECT SHAP FEATURES
# --------------------------------------------------

feature_columns = [
    "financial_loss_score",
    "affected_users_score",
    "resolution_time_score"
]

X = df[feature_columns].copy()

print("\nFeatures selected for SHAP analysis:")
print(feature_columns)


# --------------------------------------------------
# STEP 4: CREATE SHAP EXPLAINER
# --------------------------------------------------

print("\nCreating SHAP explainer...")

explainer = shap.TreeExplainer(model)

print("SHAP explainer created successfully!")


# --------------------------------------------------
# STEP 5: CALCULATE SHAP VALUES
# --------------------------------------------------

# IMPORTANT:
# The Random Forest was trained using 10 encoded
# original features, while SHAP is currently being
# applied to the 3 engineered score features.
#
# Therefore, SHAP analysis here is kept as a
# separate explainability analysis of the selected
# engineered features.

X_sample = X.iloc[[0]]

print(
    "\nCalculating SHAP values for 1 sample incident..."
)

shap_values = explainer.shap_values(
    X_sample,
    check_additivity=False
)

print(
    "\nSHAP values calculated successfully!"
)

print(
    "SHAP values type:",
    type(shap_values)
)


# --------------------------------------------------
# STEP 6: SHAP FEATURE IMPORTANCE
# --------------------------------------------------

print(
    "\nCalculating SHAP feature importance..."
)


if isinstance(shap_values, list):

    shap_array = shap_values[0]

else:

    shap_array = shap_values


shap_array = abs(shap_array)


if len(shap_array.shape) == 3:

    mean_shap_values = (
        shap_array.mean(axis=(0, 2))
    )

elif len(shap_array.shape) == 2:

    mean_shap_values = (
        shap_array.mean(axis=0)
    )

else:

    mean_shap_values = shap_array


shap_importance = pd.DataFrame({

    "feature":
        feature_columns,

    "mean_shap_value":
        mean_shap_values

})


shap_importance = (
    shap_importance
    .sort_values(
        by="mean_shap_value",
        ascending=False
    )
)


print(
    "\n" + "=" * 60
)

print(
    "SHAP FEATURE IMPORTANCE"
)

print(
    "=" * 60
)

print(
    shap_importance
)


# --------------------------------------------------
# STEP 7: SAVE SHAP FEATURE IMPORTANCE
# --------------------------------------------------

os.makedirs(
    "outputs/ml",
    exist_ok=True
)


shap_importance.to_csv(
    "outputs/ml/shap_feature_importance.csv",
    index=False
)


print(
    "\nSHAP feature importance saved successfully!"
)

print(
    "Location: "
    "outputs/ml/shap_feature_importance.csv"
)


# --------------------------------------------------
# STEP 8: INDIVIDUAL INCIDENT SHAP EXPLANATION
# --------------------------------------------------

selected_index = 0

selected_incident = X.iloc[
    [selected_index]
]


print(
    "\n" + "=" * 60
)

print(
    "INDIVIDUAL INCIDENT SHAP EXPLANATION"
)

print(
    "=" * 60
)


print(
    "\nSelected Incident ID:"
)

print(
    df.iloc[selected_index]["incident_id"]
)


print(
    "\nSelected Incident Features:"
)

print(
    selected_incident
)


individual_shap_values = shap_values


print(
    "\nSHAP explanation generated successfully!"
)


# --------------------------------------------------
# STEP 9: CREATE INDIVIDUAL EXPLANATION
# --------------------------------------------------

if isinstance(
    individual_shap_values,
    list
):

    individual_array = (
        individual_shap_values[0]
    )

else:

    individual_array = (
        individual_shap_values
    )


individual_array = abs(
    individual_array
)


if len(individual_array.shape) == 3:

    individual_values = (
        individual_array[0]
        .mean(axis=1)
    )

elif len(individual_array.shape) == 2:

    individual_values = (
        individual_array[0]
    )

else:

    individual_values = (
        individual_array
    )


individual_explanation = pd.DataFrame({

    "feature":
        feature_columns,

    "feature_value":
        selected_incident.iloc[0].values,

    "shap_value":
        individual_values

})


individual_explanation["impact"] = (
    individual_explanation[
        "shap_value"
    ]
    .apply(
        lambda x:
        "Higher Influence"
        if x > 0
        else "Lower Influence"
    )
)


individual_explanation = (
    individual_explanation
    .sort_values(
        by="shap_value",
        ascending=False
    )
)


print(
    "\nIndividual Incident Explanation:"
)

print(
    individual_explanation
)


# --------------------------------------------------
# STEP 10: SAVE INDIVIDUAL EXPLANATION
# --------------------------------------------------

individual_explanation.to_csv(
    "outputs/ml/individual_prediction_explanation.csv",
    index=False
)


print(
    "\nIndividual prediction explanation "
    "saved successfully!"
)

print(
    "Location: "
    "outputs/ml/"
    "individual_prediction_explanation.csv"
)


# --------------------------------------------------
# STEP 11: MODEL CONFIDENCE ANALYSIS
# --------------------------------------------------

print(
    "\n" + "=" * 60
)

print(
    "MODEL CONFIDENCE ANALYSIS"
)

print(
    "=" * 60
)


# --------------------------------------------------
# EXACT FEATURES USED DURING TRAINING
# --------------------------------------------------

model_features = [
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


X_model = df[
    model_features
].copy()


print(
    "\nOriginal model features selected:"
)

print(
    model_features
)


# --------------------------------------------------
# STEP 12: REPRODUCE TRAINING ENCODING
# --------------------------------------------------

categorical_columns = X_model.select_dtypes(
    include=["object", "string"]
).columns


print(
    "\nEncoding categorical features..."
)


for column in categorical_columns:

    encoder = LabelEncoder()

    encoder.fit(
        df[column]
    )

    X_model[column] = (
        encoder.transform(
            X_model[column]
        )
    )

    print(
        column,
        "encoded successfully"
    )


print(
    "\nAll categorical features encoded successfully!"
)


print(
    "\nModel input shape:",
    X_model.shape
)


# --------------------------------------------------
# STEP 13: MODEL PREDICTIONS
# --------------------------------------------------

prediction_probabilities = (
    model.predict_proba(
        X_model
    )
)


predictions = (
    model.predict(
        X_model
    )


)


# Convert numerical predictions
# back to Low / Medium / High

predicted_risk_levels = (
    target_encoder.inverse_transform(
        predictions
    )
)


# --------------------------------------------------
# STEP 14: MODEL CONFIDENCE
# --------------------------------------------------

confidence_scores = (
    prediction_probabilities
    .max(axis=1)
    * 100
)


confidence_df = pd.DataFrame({

    "incident_id":
        df["incident_id"],

    "predicted_risk_level":
        predicted_risk_levels,

    "model_confidence_percent":
        confidence_scores.round(2)

})


# --------------------------------------------------
# DISPLAY MODEL CONFIDENCE
# --------------------------------------------------

print(
    "\nModel Classes:"
)

print(
    target_encoder.classes_
)


print(
    "\nSample Model Predictions:"
)

print(
    confidence_df.head(10)
)


print(
    "\nAverage Model Confidence:"
)

print(
    f"{confidence_df['model_confidence_percent'].mean():.2f}%"
)


print(
    "\nMinimum Model Confidence:"
)

print(
    f"{confidence_df['model_confidence_percent'].min():.2f}%"
)


print(
    "\nMaximum Model Confidence:"
)

print(
    f"{confidence_df['model_confidence_percent'].max():.2f}%"
)


# --------------------------------------------------
# STEP 15: CONFIDENCE CATEGORIES
# --------------------------------------------------

def confidence_category(score):

    if score >= 90:

        return "Very High Confidence"

    elif score >= 75:

        return "High Confidence"

    elif score >= 60:

        return "Medium Confidence"

    else:

        return "Low Confidence"


confidence_df[
    "confidence_category"
] = (
    confidence_df[
        "model_confidence_percent"
    ]
    .apply(
        confidence_category
    )
)


print(
    "\nConfidence Category Distribution:"
)

print(
    confidence_df[
        "confidence_category"
    ].value_counts()
)


# --------------------------------------------------
# STEP 16: SAVE MODEL CONFIDENCE
# --------------------------------------------------

confidence_output = (
    "outputs/ml/model_confidence.csv"
)


confidence_df.to_csv(
    confidence_output,
    index=False
)


print(
    "\nModel confidence results "
    "saved successfully!"
)

print(
    "Location: "
    f"{confidence_output}"
)


# --------------------------------------------------
# STEP 17: LOW-CONFIDENCE INCIDENTS
# --------------------------------------------------

low_confidence_incidents = (
    confidence_df[
        confidence_df[
            "model_confidence_percent"
        ] < 60
    ]
)


print(
    "\n" + "=" * 60
)

print(
    "LOW-CONFIDENCE PREDICTIONS"
)

print(
    "=" * 60
)


print(
    "\nTotal Low-Confidence Incidents:"
)

print(
    len(
        low_confidence_incidents
    )
)


print(
    "\nSample Low-Confidence Incidents:"
)

print(
    low_confidence_incidents.head(10)
)


# --------------------------------------------------
# FINAL STATUS
# --------------------------------------------------

print(
    "\n" + "=" * 60
)

print(
    "SHAP AND MODEL CONFIDENCE ANALYSIS COMPLETED"
)

print(
    "=" * 60
)