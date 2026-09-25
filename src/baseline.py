import pandas as pd

# Load dataset
df = pd.read_csv("data/user_activity.csv")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour

# Days 1-15 = user-specific baseline period
BASELINE_END_DAY = 15
baseline_data = df[df["day"] <= BASELINE_END_DAY]
print("\n===== USER BASELINES =====\n")

baseline = baseline_data.groupby("user_id").agg(
    average_files=("files_accessed", "mean"),
    maximum_files=("files_accessed", "max"),
    average_activity_hour=("hour", "mean"),
    event_frequency=("user_id", "count"),
)

print(baseline)

# Most common location for each user
common_location = (
    baseline_data.groupby("user_id")["location"]
    .agg(lambda x: x.mode()[0])
)

print("\n===== NORMAL LOCATIONS =====\n")
print(common_location)

# Most common action
common_action = (
    baseline_data.groupby("user_id")["action"]
    .agg(lambda x: x.mode()[0])
)

print("\n===== COMMON ACTIONS =====\n")
print(common_action)