import os
import pandas as pd

# ==================================================
# CYBERSHIELD ANALYTICS
# RISK MONITORING AND EARLY WARNING SYSTEM
# ==================================================

print("=" * 60)
print("CYBERSHIELD ANALYTICS - RISK MONITORING")
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
# STEP 2: DISPLAY RISK SCORE INFORMATION
# --------------------------------------------------

print("\nRisk Score Summary:")
print(
    df["risk_score"].describe()
)

print("\nRisk Level Distribution:")
print(
    df["risk_level"].value_counts()
)

# --------------------------------------------------
# STEP 3: CREATE RISK MONITORING CATEGORIES
# --------------------------------------------------

def monitor_risk(score):
    if score >= 80:
        return "Critical"
    elif score >= 67:
        return "High"
    elif score >= 34:
        return "Medium"
    else:
        return "Low"


df["monitored_risk_level"] = df[
    "risk_score"
].apply(
    monitor_risk
)

print("\n" + "=" * 60)
print("RISK MONITORING RESULTS")
print("=" * 60)

print("\nMonitored Risk Level Distribution:")
print(
    df["monitored_risk_level"].value_counts()
)

# --------------------------------------------------
# STEP 4: CREATE RISK CHANGE INDICATOR
# --------------------------------------------------

df = df.sort_values(
    by="incident_id"
).reset_index(
    drop=True
)

df["previous_risk_score"] = df[
    "risk_score"
].shift(1)

df["risk_change"] = (
    df["risk_score"]
    - df["previous_risk_score"]
).round(2)

df["risk_change_status"] = df[
    "risk_change"
].apply(
    lambda x: "No Previous Record"
    if pd.isna(x)
    else "Risk Increased"
    if x > 0
    else "Risk Decreased"
    if x < 0
    else "No Change"
)

print("\nRisk Change Status:")
print(
    df["risk_change_status"].value_counts()
)

# --------------------------------------------------
# STEP 5: CREATE EARLY WARNING SYSTEM
# --------------------------------------------------

def generate_warning(row):
    warnings = []

    # Critical risk warning
    if row["risk_score"] >= 80:
        warnings.append("Critical Risk Score")

    # High risk warning
    elif row["risk_score"] >= 67:
        warnings.append("High Risk Score")

    # Large risk increase warning
    if (
        not pd.isna(row["risk_change"])
        and row["risk_change"] >= 20
    ):
        warnings.append("Sudden Risk Increase")

    # High financial loss warning
    if row["financial_loss_score"] >= 80:
        warnings.append("High Financial Loss")

    # High affected users warning
    if row["affected_users_score"] >= 80:
        warnings.append(
            "Large Number of Affected Users"
        )

    # Long resolution time warning
    if row["resolution_time_score"] >= 80:
        warnings.append("Long Resolution Time")

    if warnings:
        return ", ".join(warnings)

    return "No Immediate Warning"


df["early_warning"] = df.apply(
    generate_warning,
    axis=1
)

print("\n" + "=" * 60)
print("EARLY WARNING SYSTEM RESULTS")
print("=" * 60)

print("\nEarly Warning Distribution:")
print(
    df["early_warning"].value_counts().head(15)
)

warning_incidents = df[
    df["early_warning"] != "No Immediate Warning"
]

print("\nTotal Incidents Requiring Attention:")
print(len(warning_incidents))

print("\nSample Warning Incidents:")

print(
    warning_incidents[
        [
            "incident_id",
            "risk_score",
            "monitored_risk_level",
            "risk_change",
            "early_warning"
        ]
    ].head(10)
)

# --------------------------------------------------
# STEP 6: CURRENT vs HISTORICAL INCIDENT COMPARISON
# --------------------------------------------------

print("\n" + "=" * 60)
print("CURRENT vs HISTORICAL INCIDENT COMPARISON")
print("=" * 60)

# Historical averages
historical_avg_risk = df["risk_score"].mean()

historical_avg_loss = (
    df["financial_loss_million"].mean()
)

historical_avg_users = (
    df["affected_users"].mean()
)

historical_avg_resolution = (
    df["resolution_time_hours"].mean()
)

print("\nHistorical Dataset Averages:")
print(
    f"Average Risk Score: "
    f"{historical_avg_risk:.2f}"
)

print(
    f"Average Financial Loss: "
    f"${historical_avg_loss:.2f} Million"
)

print(
    f"Average Affected Users: "
    f"{historical_avg_users:,.0f}"
)

print(
    f"Average Resolution Time: "
    f"{historical_avg_resolution:.2f} Hours"
)

# Compare each incident with historical averages
df["risk_vs_historical"] = (
    df["risk_score"]
    - historical_avg_risk
)

df["loss_vs_historical"] = (
    df["financial_loss_million"]
    - historical_avg_loss
)

df["users_vs_historical"] = (
    df["affected_users"]
    - historical_avg_users
)

df["resolution_vs_historical"] = (
    df["resolution_time_hours"]
    - historical_avg_resolution
)


def comparison_status(value):
    if value > 0:
        return "Above Historical Average"
    elif value < 0:
        return "Below Historical Average"
    else:
        return "Equal to Historical Average"


df["risk_comparison"] = df[
    "risk_vs_historical"
].apply(
    comparison_status
)

print("\nRisk Comparison:")
print(
    df["risk_comparison"].value_counts()
)

# Display high-risk incidents
comparison = df[
    df["risk_score"] >= 67
][
    [
        "incident_id",
        "risk_score",
        "risk_comparison",
        "financial_loss_million",
        "affected_users",
        "resolution_time_hours"
    ]
]

print(
    "\nHigh-Risk Incidents Compared "
    "With Historical Data:"
)

print(
    comparison.head(10)
)

print("\nTotal High-Risk Incidents:")
print(len(comparison))

# --------------------------------------------------
# STEP 7: WHAT-IF RISK SIMULATION
# --------------------------------------------------

def calculate_risk_score(
    financial_loss,
    affected_users,
    resolution_time
):
    """
    Calculate risk score using the project's
    existing risk scoring formula.
    """

    max_loss = (
        df["financial_loss_million"].max()
    )

    max_users = (
        df["affected_users"].max()
    )

    max_resolution = (
        df["resolution_time_hours"].max()
    )

    financial_score = (
        financial_loss / max_loss
    ) * 100

    users_score = (
        affected_users / max_users
    ) * 100

    resolution_score = (
        resolution_time / max_resolution
    ) * 100

    risk_score = (
        0.50 * financial_score
        + 0.30 * users_score
        + 0.20 * resolution_score
    )

    return round(risk_score, 2)


print("\n" + "=" * 60)
print("WHAT-IF RISK SIMULATION")
print("=" * 60)

# Select one incident for simulation
simulation_incident = df.iloc[0]

original_loss = simulation_incident[
    "financial_loss_million"
]

original_users = simulation_incident[
    "affected_users"
]

original_resolution = simulation_incident[
    "resolution_time_hours"
]

original_risk = simulation_incident[
    "risk_score"
]

# Simulate increased impact
simulated_loss = original_loss * 1.20

simulated_users = (
    original_users * 1.20
)

simulated_resolution = (
    original_resolution * 1.20
)

simulated_risk = calculate_risk_score(
    simulated_loss,
    simulated_users,
    simulated_resolution
)

print("\nOriginal Incident:")
print(
    f"Financial Loss: "
    f"${original_loss:.2f} Million"
)

print(
    f"Affected Users: "
    f"{original_users:,.0f}"
)

print(
    f"Resolution Time: "
    f"{original_resolution:.2f} Hours"
)

print(
    f"Risk Score: "
    f"{original_risk:.2f}"
)

print("\nWhat-If Scenario:")

print(
    f"Financial Loss: "
    f"${simulated_loss:.2f} Million"
)

print(
    f"Affected Users: "
    f"{simulated_users:,.0f}"
)

print(
    f"Resolution Time: "
    f"{simulated_resolution:.2f} Hours"
)

print(
    f"New Risk Score: "
    f"{simulated_risk:.2f}"
)

risk_change = (
    simulated_risk - original_risk
)

print(
    f"\nRisk Score Change: "
    f"{risk_change:+.2f}"
)

if simulated_risk >= 80:
    print("New Risk Level: CRITICAL")

elif simulated_risk >= 67:
    print("New Risk Level: HIGH")

elif simulated_risk >= 34:
    print("New Risk Level: MEDIUM")

else:
    print("New Risk Level: LOW")

print("=" * 60)

# --------------------------------------------------
# STEP 8: SAVE RISK MONITORING RESULTS
# --------------------------------------------------

output_path = (
    "data/processed/"
    "risk_monitoring_results.csv"
)

df.to_csv(
    output_path,
    index=False
)

print("\nRisk monitoring results saved successfully!")

print(
    f"Output File: {output_path}"
)

print("\n" + "=" * 60)
print("RISK MONITORING MODULE COMPLETED")
print("=" * 60)