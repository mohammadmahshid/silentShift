import pandas as pd

# Load final risk results
df = pd.read_csv("data/final_results.csv")

print("\n===== SILENT SHIFT EXPLANATIONS =====\n")

for _, row in df.iterrows():

    user = row["user_id"]
    score = row["final_risk_score"]
    level = row["final_risk_level"]

    print("=" * 50)

    print(f"USER: {user}")
    print(f"RISK SCORE: {score}/100")
    print(f"RISK LEVEL: {level}")

    print("\nWHY WAS THIS USER FLAGGED?")

    reasons = []

    # Anomaly reason
    if row["anomaly_count"] >= 5:
        reasons.append(
            f"Multiple anomalous events detected ({int(row['anomaly_count'])})"
        )

    elif row["anomaly_count"] > 0:
        reasons.append(
            f"{int(row['anomaly_count'])} anomalous event(s) detected"
        )

    # Behavioral shift
    if row["shift_ratio"] >= 5:
        reasons.append(
            f"File activity increased {row['shift_ratio']:.1f}x above baseline"
        )

    elif row["shift_ratio"] >= 2:
        reasons.append(
            f"File activity increased {row['shift_ratio']:.1f}x above baseline"
        )

    elif row["shift_ratio"] >= 1.5:
        reasons.append(
            "File activity increased above normal baseline"
        )

    # Trend
    if row["trend_slope"] > 0.3:
        reasons.append(
            "Behavioral deviation is increasing over time"
        )

    elif row["trend_slope"] > 0:
        reasons.append(
            "A gradual behavioral change was detected"
        )

    # Context
    if row["context_status"] == "LEGITIMATE_CHANGE":
        reasons.append(
            f"Legitimate context: {row['context_reason']}"
        )

    else:
        reasons.append(
            "No known legitimate context recorded"
        )

    # Print reasons
    for reason in reasons:
        print(f"• {reason}")

    print()