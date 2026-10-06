CyberShield Analytics

ML-driven Cyber Threat Intelligence and Risk Prediction System

CyberShield Analytics is a machine learning-based cybersecurity analytics system designed to analyze historical cybersecurity incidents, predict incident risk levels, detect unusual attack patterns, forecast cybersecurity trends, and provide actionable security insights.

The system combines data preprocessing, machine learning, anomaly detection, time-series forecasting, explainable AI, risk monitoring, and interactive visualization to support cybersecurity risk assessment and early warning.

Project Objectives

* Analyze historical cybersecurity incidents and identify important patterns.
* Predict the risk level of cybersecurity incidents using Machine Learning.
* Detect unusual or suspicious incidents using anomaly detection.
* Forecast future cybersecurity incident trends.
* Calculate a risk score based on financial loss, affected users, and incident resolution time.
* Prioritize incidents according to their risk and severity.
* Identify similar historical incidents for comparison.
* Explain machine learning predictions using SHAP.
* Provide early warning for high-risk incidents.
* Support cybersecurity analysts in making informed decisions.
* Present analytical results through an interactive Power BI dashboard.

Key Features

1. Historical Incident Analysis

Analyzes cybersecurity incidents based on:

* Country
* Year
* Attack Type
* Target Industry
* Financial Loss
* Affected Users
* Attack Source
* Security Vulnerability Type
* Defense Mechanism
* Incident Resolution Time

2. Risk Score Calculation

A 0–100 risk score is calculated using:

Risk Score = 50% Financial Loss + 30% Affected Users + 20% Resolution Time

Risk levels are classified as:

| Risk Score | Risk Level |
| ---------- | ---------- |
| 0–33       | Low        |
| 34–66      | Medium     |
| 67–100     | High       |

3. Random Forest Risk Prediction

A Random Forest Classifier is used to predict the risk level of cybersecurity incidents.

The model uses incident characteristics such as attack type, target industry, financial loss, affected users, attack source, vulnerability type, defense mechanism, and resolution time.

4. Isolation Forest Anomaly Detection

Isolation Forest is used to identify unusual cybersecurity incidents based on numerical risk-related characteristics.

The system classifies incidents as:

* Normal
* Anomaly

5. Cybersecurity Trend Forecasting

ARIMA time-series forecasting is used to analyze historical yearly incident counts and estimate future cybersecurity incident trends when suitable time-series data is available.

6. Explainable AI

SHAP (SHapley Additive exPlanations) is used to explain the contribution of important features to machine learning predictions.

This helps make the model's results easier to understand and interpret.

7. Risk Monitoring and Early Warning

The system monitors incident risk and provides early warnings for potentially critical situations.

Monitoring conditions include:

* Risk score ≥ 80
* High-risk incidents
* Significant risk changes
* Individual incidents with very high risk scores

8. Incident Prioritization

Incidents are prioritized according to their risk level and severity so that high-risk incidents can receive attention first.

Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Statsmodels
* SHAP
* Matplotlib
* Seaborn
* MySQL
* Jupyter Notebook
* Power BI
* Git & GitHub

 Machine Learning Algorithms

| Algorithm        | Purpose                         |
| ---------------- | ------------------------------- |
| Random Forest    | Risk level prediction           |
| Isolation Forest | Anomaly detection               |
| ARIMA            | Cybersecurity trend forecasting |
| SHAP             | Prediction explanation          |

 Dataset

The project uses the Global Cybersecurity Threats 2015–2024** dataset obtained from Kaggle.

The dataset contains 3,000 cybersecurity incidents covering the period from 2015 to 2024.

The dataset contains information related to countries, attack types, industries, financial losses, affected users, attack sources, vulnerabilities, defense mechanisms, and incident resolution times.

 Data Processing Pipeline


Raw Dataset
     ↓
Data Cleaning
     ↓
Feature Engineering
     ↓
Risk Score Calculation
     ↓
Risk Level Classification
     ↓
MySQL Database
     ↓
Machine Learning Models
     ↓
Risk Prediction
     ↓
Anomaly Detection
     ↓
Trend Forecasting
     ↓
SHAP Explanation
     ↓
Risk Monitoring & Early Warning
     ↓
Power BI Dashboard


Project Structure


CyberShield-Analytics/
│
├── Data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
│
├── Documentation/
│
├── Excel/
│
├── Notebooks/
│
├── Powerbi/
│
├── SQL/
│
├── models/
│
├── outputs/
│   └── ml/
│
├── src/
│   ├── clean_data.py
│   ├── feature_engineering.py
│   ├── import_to_mysql.py
│   ├── train_random_forest.py
│   ├── detect_anomalies.py
│   ├── explain_predictions.py
│   ├── similar_incidents.py
│   └── risk_monitoring.py
│
├── .gitignore
└── README.md
```

Database

MySQL is used to store and manage the processed cybersecurity incident data.

The project uses the database:



The main incident table contains the processed incident information along with calculated risk scores and risk levels.

Project Workflow

1. Collect cybersecurity incident data.
2. Clean and validate the dataset.
3. Perform exploratory data analysis.
4. Engineer risk-related features.
5. Calculate incident risk scores.
6. Classify incidents into risk levels.
7. Store processed data in MySQL.
8. Train the Random Forest risk prediction model.
9. Detect unusual incidents using Isolation Forest.
10. Forecast incident trends using ARIMA.
11. Explain model predictions using SHAP.
12. Prioritize high-risk incidents.
13. Monitor risk changes and generate early warnings.
14. Visualize results through Power BI.

Expected Outcome

CyberShield Analytics provides a centralized analytical approach for cybersecurity incident assessment. It combines historical analysis, machine learning prediction, anomaly detection, forecasting, explainable AI, and risk monitoring to help identify potentially high-risk incidents and support faster security decision-making.

Future Scope

Future improvements may include:

* Real-time cybersecurity data integration.
* Automated threat intelligence feeds.
* Real-time alert notifications.
* Integration with SIEM platforms.
* Advanced deep learning models.
* Automated model retraining.
* More detailed attack severity prediction.
* Real-time risk monitoring dashboards.
* Integration with additional cybersecurity datasets.

 Academic Project

Project: CyberShield Analytics
Title: ML-driven Cyber Threat Intelligence and Risk Prediction System
Type: B.Tech Final-Year Project

---

*This project is developed for academic and educational purposes.*

