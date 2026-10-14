import pandas as pd
from scipy.stats import ttest_ind

df = pd.read_csv("growsight_generated_batches.csv")

# Calculate plant loss rate
df["loss_rate"] = (
    df["plants_lost"] / df["plants_planted"]
) * 100

# Create the two groups we want to compare
hot = df[df["temperature_c"] >= 35]["loss_rate"]

normal = df[
    (df["temperature_c"] >= 20) &
    (df["temperature_c"] < 30)
]["loss_rate"]

# Show basic group information
print("Hot batches:", len(hot))
print("Normal batches:", len(normal))

print("Hot average loss:", hot.mean())
print("Normal average loss:", normal.mean())

# Welch's independent t-test
t_stat, p_value = ttest_ind(
    hot,
    normal,
    equal_var=False
)

print("T-statistic:", t_stat)
print("P-value:", p_value)