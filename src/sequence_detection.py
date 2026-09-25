import pandas as pd

# Load activity data
df = pd.read_csv("data/user_activity.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour

# Sort events by user and time
df = df.sort_values(
    ["user_id", "timestamp"]
)

baseline = df[df["day"] <= 15].groupby("user_id").agg(
    baseline_files=("files_accessed", "mean"),
    normal_hour=("hour", "mean"),
    normal_location=("location", lambda values: values.mode().iloc[0]),
)
detection = df[df["day"] > 15].copy()
detection = detection.merge(baseline, left_on="user_id", right_index=True, how="left")
detection["previous_timestamp"] = detection.groupby("user_id")["timestamp"].shift(1)
detection["previous_files"] = detection.groupby("user_id")["files_accessed"].shift(1)
detection["minutes_since_previous"] = (detection["timestamp"] - detection["previous_timestamp"]).dt.total_seconds() / 60
detection["high_file_signal"] = detection["files_accessed"] >= (detection["baseline_files"] * 2.5).clip(lower=12)
detection["location_signal"] = detection["location"] != detection["normal_location"]
detection["time_signal"] = (detection["hour"] - detection["normal_hour"]).abs() >= 3
detection["download_signal"] = detection["action"].eq("file_download")
detection["close_sequence_signal"] = detection["minutes_since_previous"].le(30) & detection["previous_files"].ge((detection["baseline_files"] * 2).clip(lower=10))
detection["sequence_score"] = (
    detection["high_file_signal"].astype(int) * 3
    + detection["download_signal"].astype(int) * 2
    + detection["location_signal"].astype(int) * 2
    + detection["time_signal"].astype(int) * 2
    + detection["close_sequence_signal"].astype(int) * 2
)
detection["sequence_risk"] = pd.cut(
    detection["sequence_score"], bins=[-1, 2, 5, 99], labels=["LOW", "MEDIUM", "HIGH"]
).astype(str)
detection["reasons"] = ""
reason_columns = [
    ("high_file_signal", "Unusually high file access"),
    ("download_signal", "File download detected"),
    ("location_signal", "Unusual location"),
    ("time_signal", "Unusual activity time"),
    ("close_sequence_signal", "Suspicious actions occurred close together"),
]
for signal, reason in reason_columns:
    detection.loc[detection[signal], "reasons"] = detection.loc[detection[signal], "reasons"] + reason + "; "
result_df = detection[["user_id", "timestamp", "action", "location", "files_accessed", "sequence_score", "sequence_risk", "reasons"]]

# Save results
result_df.to_csv("data/sequence_results.csv", index=False)

print("\n===== EVENT SEQUENCE ANALYSIS =====\n")

# Show only suspicious events
suspicious = result_df[
    result_df["sequence_risk"] != "LOW"
]

print(
    suspicious.head(30).to_string(
        index=False
    )
)

print("\nResults saved to:")
print("data/sequence_results.csv")