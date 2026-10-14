import requests
import pandas as pd

url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 31.7683,
    "longitude": 35.2137,
    "start_date": "2026-02-01",
    "end_date": "2026-07-31",
    "daily": [
        "temperature_2m_mean",
        "precipitation_sum"
    ],
    "hourly": [
        "relative_humidity_2m"
    ],
    "timezone": "Asia/Jerusalem"
}

# Send request to API
response = requests.get(url, params=params)

print(response.status_code)

# Convert API response from JSON
data = response.json()

# Create daily weather dataframe
weather_df = pd.DataFrame(data["daily"])

weather_df = weather_df.rename(columns={
    "time": "date",
    "temperature_2m_mean": "outside_temperature_c",
    "precipitation_sum": "precipitation_mm"
})

weather_df["date"] = pd.to_datetime(weather_df["date"])

# Create hourly humidity dataframe
humidity_df = pd.DataFrame(data["hourly"])

humidity_df["time"] = pd.to_datetime(humidity_df["time"])

# Create a date-only column
humidity_df["date"] = humidity_df["time"].dt.normalize()

# Average the 24 hourly humidity readings into one daily value
daily_humidity = (
    humidity_df
    .groupby("date")["relative_humidity_2m"]
    .mean()
)

daily_humidity = daily_humidity.reset_index()

weather_df = weather_df.merge(
    daily_humidity,
    on="date",
    how="left"
)

growth_df = pd.read_csv("growsight_generated_batches.csv")

growth_df["date"] = pd.to_datetime(growth_df["date"])

combined_df = growth_df.merge(
    weather_df,
    on="date",
    how="left"
)


combined_df = combined_df.rename(columns={
    "relative_humidity_2m": "outside_humidity_percent"
})

combined_df.to_csv(
    "growsight_with_weather.csv",
    index=False
)

combined_df["loss_rate_percent"] = (
    combined_df["plants_lost"] / combined_df["plants_planted"]
) * 100

print(
    combined_df[
        ["batch_id", "loss_rate_percent", "outside_temperature_c",
         "outside_humidity_percent", "precipitation_mm"]
    ].head()
)


print(combined_df.head())

print(daily_humidity.head())
print(weather_df.head())
print(combined_df.isnull().sum())