import pandas as pd
from sklearn.ensemble import IsolationForest

# --------------------------------
# LOAD DATA
# --------------------------------

df = pd.read_csv("data/user_activity.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

# --------------------------------
# CREATE FEATURES
# --------------------------------

df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day

# Convert location into numbers
df["location_code"] = df["location"].astype("category").cat.codes

# Convert action into numbers
df["action_code"] = df["action"].astype("category").cat.codes

features = [
    "hour",
    "location_code",
    "action_code",
    "files_accessed"
]

baseline_data = df[df["day"] <= 15]
detection_data = df[df["day"] > 15].copy()
X = baseline_data[features]

# --------------------------------
# CREATE MODEL
# --------------------------------

model = IsolationForest(
    contamination=0.10,
    random_state=42
)

# Train model
model.fit(X)

# --------------------------------
# PREDICT ANOMALIES
# --------------------------------

detection_data["anomaly"] = model.predict(detection_data[features])

# -1 = anomaly
#  1 = normal

detection_data["anomaly_score"] = model.decision_function(detection_data[features])

# --------------------------------
# DISPLAY RESULTS
# --------------------------------

print("\n===== ML ANOMALY DETECTION =====\n")

print(
    detection_data[
        [
            "user_id",
            "timestamp",
            "action",
            "location",
            "files_accessed",
            "anomaly",
            "anomaly_score"
        ]
    ].head(20).to_string(index=False)
)

# Count anomalies
print("\n===== ANOMALY COUNT =====\n")

print(
    detection_data["anomaly"]
    .value_counts()
)

# Save results
detection_data.to_csv(
    "data/anomaly_results.csv",
    index=False
)

print("\nAnomaly results saved!")