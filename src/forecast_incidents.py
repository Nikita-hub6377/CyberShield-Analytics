import os
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


# ==================================================
# CYBERSHIELD ANALYTICS
# ARIMA INCIDENT FORECASTING
# ==================================================

print("=" * 60)
print("CYBERSHIELD ANALYTICS - INCIDENT FORECASTING")
print("=" * 60)


# --------------------------------------------------
# STEP 1: LOAD PROCESSED DATASET
# --------------------------------------------------

input_path = "data/processed/cybersecurity_processed.csv"

df = pd.read_csv(input_path)

print("\nDataset loaded successfully!")
print("Dataset Shape:", df.shape)


# --------------------------------------------------
# STEP 2: PREPARE YEARLY INCIDENT DATA
# --------------------------------------------------

yearly_incidents = (
    df.groupby("year")
      .size()
      .reset_index(name="incident_count")
)

yearly_incidents["year"] = pd.to_datetime(
    yearly_incidents["year"].astype(str)
)

yearly_incidents = yearly_incidents.set_index("year")

yearly_incidents = yearly_incidents.asfreq("YS")

print("\nYearly incident data:")
print(yearly_incidents)


# --------------------------------------------------
# STEP 3: BUILD ARIMA MODEL
# --------------------------------------------------

print("\n" + "=" * 60)
print("BUILDING ARIMA MODEL")
print("=" * 60)

model = ARIMA(
    yearly_incidents["incident_count"],
    order=(1, 1, 1)
)

model_fit = model.fit()

print("\nARIMA model trained successfully!")


# --------------------------------------------------
# STEP 4: FORECAST NEXT 3 YEARS
# --------------------------------------------------

forecast_steps = 3

forecast = model_fit.forecast(
    steps=forecast_steps
)

last_year = yearly_incidents.index[-1].year

forecast_years = [
    last_year + i
    for i in range(1, forecast_steps + 1)
]

forecast_df = pd.DataFrame({
    "year": forecast_years,
    "forecast_incidents": forecast.round(0).astype(int)
})


# --------------------------------------------------
# STEP 5: DISPLAY FORECAST
# --------------------------------------------------

print("\n" + "=" * 60)
print("INCIDENT FORECAST")
print("=" * 60)

print(
    forecast_df.to_string(index=False)
)


# --------------------------------------------------
# STEP 6: SAVE FORECAST
# --------------------------------------------------

output_dir = "outputs/ml"

os.makedirs(
    output_dir,
    exist_ok=True
)

output_path = os.path.join(
    output_dir,
    "incident_forecast.csv"
)

forecast_df.to_csv(
    output_path,
    index=False
)

print("\nForecast saved successfully!")
print("Location:", output_path)

print("\n" + "=" * 60)
print("ARIMA FORECASTING COMPLETED SUCCESSFULLY!")
print("=" * 60)