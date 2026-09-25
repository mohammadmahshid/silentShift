import numpy as np
import pandas as pd

df = pd.read_csv("data/user_activity.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["day"] = df["timestamp"].dt.day
baseline = df[df["day"] <= 15].groupby("user_id")["files_accessed"].mean()
detection = df[df["day"] > 15]
daily = detection.groupby(["user_id", "day"], as_index=False)["files_accessed"].mean()
daily["baseline_average"] = daily["user_id"].map(baseline)
daily["deviation_ratio"] = daily["files_accessed"] / daily["baseline_average"].clip(lower=0.01)
early = daily[daily["day"] <= 20].groupby("user_id")["files_accessed"].mean()
late = daily[daily["day"] >= 26].groupby("user_id")["files_accessed"].mean()

def calculate_slope(group):
    if len(group) < 2:
        return 0.0
    return float(np.polyfit(group["day"], group["deviation_ratio"], 1)[0])

trend = daily.groupby("user_id").apply(calculate_slope, include_groups=False).rename("trend_slope")
shift_df = pd.DataFrame({"baseline_average": baseline, "early_behavior": early, "late_behavior": late})
shift_df["shift_ratio"] = shift_df["late_behavior"] / shift_df["baseline_average"].clip(lower=0.01)
shift_df["trend_slope"] = trend
shift_df = shift_df.reset_index()
shift_df[["early_behavior", "late_behavior"]] = shift_df[["early_behavior", "late_behavior"]].fillna(0)

def shift_status(row):
    if row["shift_ratio"] >= 3 and row["trend_slope"] > 0.02:
        return "HIGH SHIFT"
    if row["shift_ratio"] >= 1.75 and row["trend_slope"] > 0.01:
        return "MEDIUM SHIFT"
    if row["shift_ratio"] >= 1.35 or row["trend_slope"] > 0.01:
        return "LOW SHIFT"
    return "NORMAL"

shift_df["shift_status"] = shift_df.apply(shift_status, axis=1)
shift_df.to_csv("data/shift_results.csv", index=False)
print("\n===== SILENT SHIFT DETECTION =====\n")
print(shift_df.head(30).to_string(index=False))
print("\nResults saved to: data/shift_results.csv")