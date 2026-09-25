import pandas as pd

df = pd.read_csv("data/user_activity.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["day"] = df["timestamp"].dt.day

baseline = df[df["day"] <= 15].groupby("user_id").agg(
    average_files=("files_accessed", "mean"),
    baseline_events=("user_id", "count"),
)
detection = df[df["day"] > 15].groupby("user_id").agg(
    current_average_files=("files_accessed", "mean"),
    current_events=("user_id", "count"),
)
comparison = baseline.join(detection)
comparison["file_deviation"] = comparison["current_average_files"] / comparison["average_files"].clip(lower=0.01)

print("\n===== BEHAVIORAL DEVIATION (DAYS 16-30 VS DAYS 1-15) =====\n")
print(comparison.head(30).to_string())