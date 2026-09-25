from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EXPECTED_OUTPUTS = {
    "anomaly_results.csv": 15000,
    "user_anomaly_results.csv": 15000,
    "shift_results.csv": 1000,
    "risk_results.csv": 1000,
    "context_results.csv": 1000,
    "final_results.csv": 1000,
    "sequence_results.csv": 15000,
    "final_engine_results.csv": 1000,
}

activity = pd.read_csv(DATA / "user_activity.csv")
activity["timestamp"] = pd.to_datetime(activity["timestamp"], errors="raise")
print("\nDataset validation\n------------------")
print(f"Users: {activity['user_id'].nunique()}")
print(f"Events: {len(activity)}")
print(f"Days: {activity['timestamp'].dt.date.nunique()}")

for filename, expected_rows in EXPECTED_OUTPUTS.items():
    path = DATA / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing result file: {path}")
    rows = len(pd.read_csv(path))
    if rows != expected_rows:
        raise ValueError(f"{filename}: expected {expected_rows} rows, found {rows}")
    print(f"OK: {filename} ({rows} rows)")

final = pd.read_csv(DATA / "final_engine_results.csv")
levels = set(final["final_risk_level"])
required_levels = {"HIGH", "MEDIUM", "LOW"}
if not required_levels.issubset(levels):
    raise ValueError(f"Missing risk levels: {sorted(required_levels - levels)}")
print("Risk levels:", final["final_risk_level"].value_counts().to_dict())
print("Pipeline validation passed.")
