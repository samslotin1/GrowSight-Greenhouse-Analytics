import pandas as pd
import numpy as np
from datetime import date, timedelta

np.random.seed(42)

existing_batches = pd.DataFrame({
    "batch_id": [101, 102, 103],
    "date": ["2026-07-01", "2026-07-07", "2026-07-04"],
    "species_id": [1, 2, 3],
    "zone_id": [1, 1, 2]
})

existing_batches["date"] = pd.to_datetime(existing_batches["date"])
print(existing_batches)

start_date = pd.Timestamp("2026-02-01")
end_date = pd.Timestamp("2026-07-31")

generated_dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

new_batch_ids = np.arange(1001, 1151)
print(generated_dates.min(), generated_dates.max())
print(new_batch_ids[0], new_batch_ids[-1])
print(len(new_batch_ids))

generated_df = pd.DataFrame({
    "batch_id": new_batch_ids,
    "date": np.random.choice(generated_dates, size=len(new_batch_ids)),
    "species_id": np.random.choice([1, 2, 3], size=len(new_batch_ids)),
    "zone_id": np.random.choice([1, 2, 3], size=len(new_batch_ids))
})

generated_df = generated_df.sort_values("date").reset_index(drop=True)

print(generated_df.head())
print(generated_df.tail())
print(generated_df.shape)

generated_df["plants_planted"] = np.random.randint(
    70,
    151,
    size=len(generated_df)

)

month_base_temperatures = {
    2: 18,
    3: 21,
    4: 24,
    5: 27,
    6: 30,
    7: 33
}

generated_df["temperature_c"] = (
    generated_df["date"].dt.month
    .map(month_base_temperatures)
    + np.random.normal(0, 2.5, len(generated_df))
).round(1)

print(
    generated_df[
        ["date", "plants_planted", "temperature_c"]
    ].head(10)
)

print(
    generated_df.groupby(
        generated_df["date"].dt.month
    )["temperature_c"].mean()
)

base_water = np.random.randint(
    45,
    86,
    size=len(generated_df)
)

heat_adjustment = np.maximum(
    generated_df["temperature_c"] - 24,
    0
) * 2.2

generated_df["water_liters"] = (
    base_water + heat_adjustment
).round().astype(int)

generated_df["ph_level"] = (
    np.random.normal(
        6.2,
        0.35,
        size=len(generated_df)
    )
).clip(5.2, 7.2).round(2)

ec_base = generated_df["species_id"].map({
    1: 2.3,
    2: 2.1,
    3: 2.5
})

generated_df["ec_level"] = (
    ec_base
    + np.random.normal(
        0,
        0.35,
        size=len(generated_df)
    )
).clip(1.2, 3.5).round(2)

print(
    generated_df[
        ["temperature_c", "water_liters"]
    ].head(10)
)


print(
    generated_df[
        ["temperature_c", "water_liters"]
    ].head(10)
)

print(
    generated_df.groupby(
        generated_df["date"].dt.month
    )["water_liters"].mean()
)

base_loss_rate = np.random.uniform(
    0.03,
    0.08,
    size=len(generated_df)
)

heat_stress = np.maximum(
    generated_df["temperature_c"] - 32,
    0
) * 0.015

pepper_risk = np.where(
    generated_df["species_id"] == 3,
    0.03,
    0
)

ph_stress = np.where(
    (generated_df["ph_level"] < 5.8) | (generated_df["ph_level"] > 6.8),
    0.02,
    0
)

ec_stress = np.where(
    (generated_df["ec_level"] < 1.6) | (generated_df["ec_level"] > 3.0),
    0.04,
    0
)



random_noise = np.random.normal(
    0,
    0.015,
    size=len(generated_df)
)

generated_df["loss_rate"] = (
    base_loss_rate
    + heat_stress
    + pepper_risk
    + ph_stress
    + ec_stress
    + random_noise
).clip(0.01, 0.35)

generated_df["plants_lost"] = (
    generated_df["plants_planted"]
    * generated_df["loss_rate"]
).round().astype(int)

generated_df["ph_status"] = np.where(
    (generated_df["ph_level"] < 5.8) | (generated_df["ph_level"] > 6.8),
    "Stressed",
    "Normal"
)

generated_df["ec_status"] = np.where(
    (generated_df["ec_level"] < 1.6) | (generated_df["ec_level"] > 3.0),
    "Stressed",
    "Normal"
)

print(
    generated_df.groupby("ph_status")["loss_rate"].mean()
)

print(
    generated_df.groupby("ec_status")["loss_rate"].mean()
)


print(
    generated_df[
        [
            "species_id",
            "temperature_c",
            "plants_planted",
            "plants_lost",
            "loss_rate"
        ]
    ].head(10)
)

print(
    generated_df.groupby("species_id")["loss_rate"].mean()
)

print(generated_df.isna().sum())

print(
    generated_df["batch_id"].duplicated().sum()
)

print(
    (generated_df["plants_lost"] > generated_df["plants_planted"]).sum()
)

print(
    generated_df[
        [
            "plants_planted",
            "plants_lost",
            "water_liters",
            "temperature_c"
        ]
    ].describe()
)


export_df = generated_df[
    [
        "batch_id",
        "date",
        "species_id",
        "zone_id",
        "plants_planted",
        "plants_lost",
        "water_liters",
        "temperature_c",
        "ph_level",
        "ec_level"
    ]
].copy()

export_df.to_csv(
    "growsight_generated_batches.csv",
    index=False
)

print(export_df.head())
print(export_df.shape)