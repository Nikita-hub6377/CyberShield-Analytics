import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the processed dataset
df = pd.read_csv("data/processed/cybersecurity_processed.csv")

print("=" * 60)
print("CYBERSHIELD ANALYTICS - RANDOM FOREST RISK PREDICTION")
print("=" * 60)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)

# --------------------------------------------------
# STEP 1: Select features and target
# --------------------------------------------------

# Columns used as input for the machine learning model
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

# Target column to predict
y = df["risk_level"].copy()

print("\nInput Features:")
print(feature_columns)

print("\nTarget:")
print("risk_level")

# --------------------------------------------------
# STEP 2: Encode categorical columns
# --------------------------------------------------

categorical_columns = X.select_dtypes(include=["object", "string"]).columns

print("\nEncoding categorical columns:")

for column in categorical_columns:
    encoder = LabelEncoder()
    X[column] = encoder.fit_transform(X[column])
    print(column, "encoded successfully")

# Encode the target column
target_encoder = LabelEncoder()
y = target_encoder.fit_transform(y)

print("\nRisk level encoding:")
for label, number in zip(
    target_encoder.classes_,
    target_encoder.transform(target_encoder.classes_)
):
    print(label, "=", number)

# --------------------------------------------------
# STEP 3: Split the dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nDataset split completed successfully!")

print("\nTraining Data:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("\nTesting Data:")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)
# --------------------------------------------------
# STEP 4: Train the Random Forest Model
# --------------------------------------------------

from sklearn.ensemble import RandomForestClassifier

# Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

print("\n" + "=" * 60)
print("RANDOM FOREST MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nModel Details:")
print("Algorithm: Random Forest Classifier")
print("Number of Trees: 100")
print("Training Records:", len(X_train))
print("Testing Records:", len(X_test))
# --------------------------------------------------
# STEP 5: Test and Evaluate the Model
# --------------------------------------------------

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Make predictions on the testing data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL EVALUATION RESULTS")
print("=" * 60)

print("\nModel Accuracy:")
print(f"{accuracy * 100:.2f}%")

# Classification report
print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=target_encoder.classes_
    )
)

# Confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
# --------------------------------------------------
# STEP 6: Save the Trained Model
# --------------------------------------------------

import os
import joblib

# Create models folder if it does not exist
os.makedirs("models", exist_ok=True)

# Save the trained Random Forest model
joblib.dump(model, "models/random_forest_model.pkl")

# Save the target encoder
joblib.dump(target_encoder, "models/risk_level_encoder.pkl")

print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY!")
print("=" * 60)

print("Random Forest Model: models/random_forest_model.pkl")
print("Risk Level Encoder: models/risk_level_encoder.pkl")
# --------------------------------------------------
# STEP 7: Save Predictions for Dashboard
# --------------------------------------------------

# Create a copy of the test data
results = df.loc[X_test.index, [
    "incident_id",
    "country",
    "year",
    "attack_type",
    "target_industry",
    "financial_loss_million",
    "affected_users",
    "risk_score",
    "risk_level"
]].copy()

# Add actual and predicted risk levels
results["actual_risk_level"] = target_encoder.inverse_transform(y_test)
results["predicted_risk_level"] = target_encoder.inverse_transform(y_pred)

# Save prediction results
os.makedirs("outputs/ml", exist_ok=True)

results.to_csv(
    "outputs/ml/random_forest_predictions.csv",
    index=False
)

print("\nPredictions saved successfully!")
print("Location: outputs/ml/random_forest_predictions.csv")

# Show first 10 predictions
print("\nSample Predictions:")
print(
    results[
        [
            "incident_id",
            "risk_score",
            "actual_risk_level",
            "predicted_risk_level"
        ]
    ].head(10)
)
# --------------------------------------------------
# STEP 16: INCIDENT PRIORITIZATION
# --------------------------------------------------

# Create priority based on risk score
def assign_priority(score):
    if score >= 80:
        return "Critical"
    elif score >= 67:
        return "High"
    elif score >= 34:
        return "Medium"
    else:
        return "Low"


# Add priority column
results["priority"] = results["risk_score"].apply(assign_priority)

# Sort incidents from highest to lowest risk
results = results.sort_values(
    by="risk_score",
    ascending=False
)

# Save prioritized incidents
results.to_csv(
    "outputs/ml/prioritized_incidents.csv",
    index=False
)

print("\n" + "=" * 60)
print("INCIDENT PRIORITIZATION COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nPriority Distribution:")
print(results["priority"].value_counts())

print("\nTop 10 Highest Priority Incidents:")
print(
    results[
        [
            "incident_id",
            "attack_type",
            "risk_score",
            "predicted_risk_level",
            "priority"
        ]
    ].head(10)
)

print("\nPrioritized incidents saved successfully!")
print("Location: outputs/ml/prioritized_incidents.csv")
# --------------------------------------------------
# STEP 17: MODEL CONFIDENCE
# --------------------------------------------------

# Get prediction probabilities from Random Forest
prediction_probabilities = model.predict_proba(X_test)

# Get the highest probability for each prediction
results["model_confidence"] = (
    prediction_probabilities.max(axis=1) * 100
).round(2)

# Assign confidence categories
def assign_confidence_level(confidence):
    if confidence >= 80:
        return "High"
    elif confidence >= 60:
        return "Medium"
    else:
        return "Low"


results["confidence_level"] = results["model_confidence"].apply(
    assign_confidence_level
)

# Save results with confidence information
results.to_csv(
    "outputs/ml/risk_predictions_with_confidence.csv",
    index=False
)

print("\n" + "=" * 60)
print("MODEL CONFIDENCE CALCULATED SUCCESSFULLY!")
print("=" * 60)

print("\nConfidence Level Distribution:")
print(results["confidence_level"].value_counts())

print("\nSample Results with Confidence:")
print(
    results[
        [
            "incident_id",
            "predicted_risk_level",
            "model_confidence",
            "confidence_level"
        ]
    ].head(10)
)

print("\nResults saved successfully!")
print("Location: outputs/ml/risk_predictions_with_confidence.csv")
# --------------------------------------------------
# STEP 18: WHAT-IF RISK SIMULATION
# --------------------------------------------------

def simulate_risk(
    country,
    year,
    attack_type,
    target_industry,
    financial_loss_million,
    affected_users,
    attack_source,
    vulnerability_type,
    defense_mechanism,
    resolution_time_hours
):
    # Create a new incident
    new_incident = pd.DataFrame([{
        "country": country,
        "year": year,
        "attack_type": attack_type,
        "target_industry": target_industry,
        "financial_loss_million": financial_loss_million,
        "affected_users": affected_users,
        "attack_source": attack_source,
        "vulnerability_type": vulnerability_type,
        "defense_mechanism": defense_mechanism,
        "resolution_time_hours": resolution_time_hours
    }])

    # Encode categorical columns
    for column in categorical_columns:
        encoder = LabelEncoder()
        encoder.fit(df[column])
        new_incident[column] = encoder.transform(
            new_incident[column]
        )

    # Make prediction
    prediction = model.predict(new_incident)[0]

    # Get confidence
    confidence = model.predict_proba(
        new_incident
    ).max() * 100

    # Convert prediction back to risk label
    predicted_risk = target_encoder.inverse_transform(
        [prediction]
    )[0]

    return predicted_risk, round(confidence, 2)


# --------------------------------------------------
# SAMPLE WHAT-IF SIMULATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("WHAT-IF RISK SIMULATION")
print("=" * 60)

predicted_risk, confidence = simulate_risk(
    country="India",
    year=2024,
    attack_type="Ransomware",
    target_industry="Banking",
    financial_loss_million=90,
    affected_users=900000,
    attack_source="Hacker Group",
    vulnerability_type="Unpatched Software",
    defense_mechanism="Firewall",
    resolution_time_hours=65
)

print("\nSimulated Incident:")
print("Country: India")
print("Attack Type: Ransomware")
print("Target Industry: Banking")
print("Financial Loss: 90 Million")
print("Affected Users: 900000")
print("Resolution Time: 65 Hours")

print("\nWHAT-IF RESULT:")
print("Predicted Risk Level:", predicted_risk)
print("Model Confidence:", confidence, "%")