from sklearn.metrics import precision_score
import pandas as pd
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# Load GrowSight data
data = pd.read_csv("growsight_generated_batches.csv")


# Convert date into a real date
data["date"] = pd.to_datetime(data["date"])

# Create month column (not currently used by the model)
data["month"] = data["date"].dt.month


# Calculate loss rate
data["loss_rate"] = (
    data["plants_lost"] * 100.0 / data["plants_planted"]
)


# Create target:
# 1 = High Risk
# 0 = Not High Risk
data["high_risk"] = (data["loss_rate"] >= 10).astype(int)


# Features the models are allowed to use
X = data[[
    "temperature_c",
    "water_liters",
    "species_id",
    "zone_id"
]]


# Treat species and zone as categories
X = pd.get_dummies(
    X,
    columns=["species_id", "zone_id"],
    dtype=int
)


# What we want to predict
y = data["high_risk"]


# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -------------------------
# LOGISTIC REGRESSION
# -------------------------

model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
risk_probabilities = model.predict_proba(X_test)[:, 1]
threshold_predictions = (risk_probabilities >= 0.40).astype(int)
print("40% Threshold:")
print(confusion_matrix(y_test, threshold_predictions))
print("40% Threshold Precision:", precision_score(y_test, threshold_predictions))

print("Logistic Regression:")
print(confusion_matrix(y_test, predictions))


# -------------------------
# RANDOM FOREST
# -------------------------

forest_model = RandomForestClassifier(
    class_weight="balanced",
    random_state=42
)

forest_model.fit(X_train, y_train)

forest_predictions = forest_model.predict(X_test)

print("Random Forest:")
print(confusion_matrix(y_test, forest_predictions))
print("Logistic Regression:")
print(confusion_matrix(y_test, predictions))
print("Logistic Recall:", recall_score(y_test, predictions))
print("Random Forest Recall:", recall_score(y_test, forest_predictions))
print("Logistic Precision:", precision_score(y_test, predictions))
print("\nLOGISTIC REGRESSION REPORT")
print(classification_report(y_test, predictions))

print("\nRANDOM FOREST REPORT")
print(classification_report(y_test, forest_predictions))

print("\nLOGISTIC REGRESSION - 40% THRESHOLD REPORT")
print(classification_report(y_test, threshold_predictions))