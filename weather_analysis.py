import pandas as pd

df = pd.read_csv("growsight_with_weather.csv")

df["loss_rate_percent"] = (
    df["plants_lost"] / df["plants_planted"]
) * 100

weather_correlation = df[
    [
        "loss_rate_percent",
        "outside_temperature_c",
        "outside_humidity_percent",
        "precipitation_mm"
    ]
].corr()

print(weather_correlation["loss_rate_percent"])