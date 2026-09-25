import pandas as pd

# Load activity data
df = pd.read_csv("data/user_activity.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["day"] = df["timestamp"].dt.day

if "behaviour" in df.columns:
    user_behaviour = df.groupby("user_id")["behaviour"].first()
else:
    user_behaviour = pd.Series(dtype=str)

results = []
for user in df["user_id"].unique():
    if user_behaviour.get(user, "") == "legitimate_change":
        context_status = "LEGITIMATE_CHANGE"
        reason = "New project assignment recorded in synthetic context"
    else:
        context_status = "NO_KNOWN_CHANGE"
        reason = "No legitimate context recorded"

    results.append([
        user,
        context_status,
        reason
    ])


context_df = pd.DataFrame(
    results,
    columns=[
        "user_id",
        "context_status",
        "context_reason"
    ]
)

# Save
context_df.to_csv(
    "data/context_results.csv",
    index=False
)

print("\n===== CONTEXT ANALYSIS =====\n")

print(
    context_df.to_string(index=False)
)

print("\nResults saved to:")
print("data/context_results.csv")