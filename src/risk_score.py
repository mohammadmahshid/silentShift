import pandas as pd

# Load our previous results
shift_df = pd.read_csv("data/shift_results.csv")
anomaly_df = pd.read_csv("data/user_anomaly_results.csv")

# Count anomalous events for each user
anomaly_counts = (
    anomaly_df[anomaly_df["anomaly"] == -1]
    .groupby("user_id")
    .size()
    .reset_index(name="anomaly_count")
)

# Merge with shift results
risk_df = shift_df.merge(
    anomaly_counts,
    on="user_id",
    how="left"
)

# Users with no anomalies get 0
risk_df["anomaly_count"] = (
    risk_df["anomaly_count"].fillna(0)
)

# -----------------------------
# 1. ML ANOMALY SCORE
# -----------------------------

def anomaly_score(count):
    if count >= 8:
        return 30
    elif count >= 5:
        return 20
    elif count >= 2:
        return 10
    else:
        return 0


risk_df["ml_score"] = (
    risk_df["anomaly_count"]
    .apply(anomaly_score)
)

# -----------------------------
# 2. BEHAVIOR SHIFT SCORE
# -----------------------------

def shift_score(ratio):
    if ratio >= 10:
        return 40
    elif ratio >= 5:
        return 30
    elif ratio >= 2:
        return 20
    elif ratio >= 1.5:
        return 10
    else:
        return 0


risk_df["shift_score"] = (
    risk_df["shift_ratio"]
    .apply(shift_score)
)

# -----------------------------
# 3. TREND SCORE
# -----------------------------

def trend_score(slope):
    if slope >= 1:
        return 20
    elif slope >= 0.3:
        return 15
    elif slope > 0:
        return 5
    else:
        return 0


risk_df["trend_score"] = (
    risk_df["trend_slope"]
    .apply(trend_score)
)

# -----------------------------
# FINAL RISK SCORE
# -----------------------------

risk_df["risk_score"] = (
    risk_df["ml_score"]
    + risk_df["shift_score"]
    + risk_df["trend_score"]
)

# Maximum = 90, so cap at 100
risk_df["risk_score"] = (
    risk_df["risk_score"].clip(upper=100)
)

# -----------------------------
# RISK LEVEL
# -----------------------------

def risk_level(score):
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


risk_df["risk_level"] = (
    risk_df["risk_score"]
    .apply(risk_level)
)

# -----------------------------
# SAVE RESULTS
# -----------------------------

risk_df.to_csv(
    "data/risk_results.csv",
    index=False
)

print("\n===== SILENT SHIFT RISK SCORES =====\n")

print(
    risk_df[
        [
            "user_id",
            "anomaly_count",
            "shift_ratio",
            "trend_slope",
            "risk_score",
            "risk_level"
        ]
    ].to_string(index=False)
)

print("\nResults saved to:")
print("data/risk_results.csv")
