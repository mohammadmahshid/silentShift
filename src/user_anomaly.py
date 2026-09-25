import pandas as pd
from sklearn.ensemble import IsolationForest

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("data/user_activity.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour
df["location_code"] = pd.Categorical(df["location"]).codes
df["action_code"] = pd.Categorical(df["action"]).codes

# -----------------------------
# STORE RESULTS
# -----------------------------

results = []

# -----------------------------
# TRAIN ONE MODEL PER USER
# -----------------------------

for user, user_data in df.groupby("user_id", sort=False):

    baseline = user_data[user_data["day"] <= 15]

    current = user_data[user_data["day"] > 15]

    # Features used by ML
    features = [
        "hour",
        "files_accessed",
        "location_code",
        "action_code"
    ]

    # If not enough baseline data, skip
    if len(baseline) < 5 or current.empty:
        continue

    X_train = baseline[features]

    # -----------------------------
    # CREATE USER-SPECIFIC MODEL
    # -----------------------------

    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )

    model.fit(X_train)

    # Predict current behavior
    predictions = model.predict(
        current[features]
    )

    scores = model.decision_function(
        current[features]
    )

    # Store results
    for i, (_, row) in enumerate(current.iterrows()):

        results.append([
            user,
            row["timestamp"],
            row["action"],
            row["location"],
            row["files_accessed"],
            predictions[i],
            scores[i]
        ])


# -----------------------------
# CREATE RESULT DATAFRAME
# -----------------------------

result_df = pd.DataFrame(
    results,
    columns=[
        "user_id",
        "timestamp",
        "action",
        "location",
        "files_accessed",
        "anomaly",
        "anomaly_score"
    ]
)

# -----------------------------
# SAVE RESULTS
# -----------------------------

result_df.to_csv(
    "data/user_anomaly_results.csv",
    index=False
)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------

print("\n===== USER-SPECIFIC ANOMALIES =====\n")

print(
    result_df.head(30).to_string(index=False)
)

print("\n===== ANOMALIES PER USER =====\n")

print(
    result_df[result_df["anomaly"] == -1]
    .groupby("user_id")
    .size()
)

print("\nResults saved to:")
print("data/user_anomaly_results.csv")