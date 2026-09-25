import pandas as pd

EXPECTED_COLUMNS = {"user_id", "timestamp", "action", "location", "files_accessed"}
df = pd.read_csv("data/user_activity.csv")
missing = EXPECTED_COLUMNS.difference(df.columns)
if missing:
	raise ValueError(f"Missing expected columns: {sorted(missing)}")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")

print("\nDataset validation\n------------------")
print(f"Users: {df['user_id'].nunique()}")
print(f"Events: {len(df)}")
print(f"Days: {df['timestamp'].dt.date.nunique()}")
print(f"Events per user: {df.groupby('user_id').size().mean():.1f} average")
print(f"Events per day: {df.groupby(df['timestamp'].dt.date).size().mean():.1f} average")
print("\nAction distribution:\n" + df["action"].value_counts().to_string())
print("\nLocation distribution:\n" + df["location"].value_counts().to_string())
if "behaviour" in df.columns or "behavior" in df.columns:
	category_column = "behaviour" if "behaviour" in df.columns else "behavior"
	print("\nUsers by behavior category:\n" + df.groupby(category_column)["user_id"].nunique().to_string())
print("\nFirst 10 events:\n" + df.head(10).to_string(index=False))