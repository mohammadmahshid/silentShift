import pandas as pd

# Load data
df = pd.read_csv("data/user_activity.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract useful information
df["day"] = df["timestamp"].dt.day
df["hour"] = df["timestamp"].dt.hour

# Split baseline and current behavior
baseline_data = df[df["day"] <= 15]
current_data = df[df["day"] > 15]

# --------------------------------
# 1. FILE ACTIVITY BASELINE
# --------------------------------

baseline_files = baseline_data.groupby("user_id")[
    "files_accessed"
].mean()

current_files = current_data.groupby("user_id")[
    "files_accessed"
].mean()

# --------------------------------
# 2. LOGIN TIME BASELINE
# --------------------------------

baseline_hour = baseline_data.groupby("user_id")[
    "hour"
].mean()

current_hour = current_data.groupby("user_id")[
    "hour"
].mean()

# --------------------------------
# 3. LOCATION BASELINE
# --------------------------------

baseline_location = baseline_data.groupby("user_id")[
    "location"
].agg(lambda x: x.mode()[0])

current_location = current_data.groupby("user_id")[
    "location"
].agg(lambda x: x.mode()[0])

# --------------------------------
# CREATE RESULTS
# --------------------------------

results = []

for user in baseline_files.index:

    # FILE SCORE
    file_ratio = (
        current_files[user] /
        baseline_files[user]
    )

    if file_ratio >= 5:
        file_score = 3
    elif file_ratio >= 2:
        file_score = 2
    elif file_ratio >= 1.5:
        file_score = 1
    else:
        file_score = 0

    # LOCATION SCORE
    if current_location[user] != baseline_location[user]:
        location_score = 2
    else:
        location_score = 0

    # TIME SCORE
    hour_difference = abs(
        current_hour[user] -
        baseline_hour[user]
    )

    if hour_difference >= 5:
        time_score = 2
    elif hour_difference >= 2:
        time_score = 1
    else:
        time_score = 0

    # TOTAL SCORE
    total_score = (
        file_score +
        location_score +
        time_score
    )

    results.append([
        user,
        round(file_ratio, 2),
        baseline_location[user],
        current_location[user],
        round(hour_difference, 2),
        file_score,
        location_score,
        time_score,
        total_score
    ])


result_df = pd.DataFrame(
    results,
    columns=[
        "user_id",
        "file_ratio",
        "normal_location",
        "current_location",
        "time_difference",
        "file_score",
        "location_score",
        "time_score",
        "total_score"
    ]
)

print("\n===== MULTI-SIGNAL ANALYSIS =====\n")

print(result_df.to_string(index=False))


print("\n===== RISK LEVEL =====\n")

for _, row in result_df.iterrows():

    score = row["total_score"]

    if score >= 5:
        risk = "🔴 HIGH"
    elif score >= 3:
        risk = "🟡 MEDIUM"
    else:
        risk = "🟢 LOW"

    print(
        f"{row['user_id']} → "
        f"{risk} "
        f"(score: {score})"
    )