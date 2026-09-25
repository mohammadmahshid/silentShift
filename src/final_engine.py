import pandas as pd


# ==========================================
# LOAD RESULTS
# ==========================================

risk_df = pd.read_csv("data/risk_results.csv")
context_df = pd.read_csv("data/context_results.csv")
sequence_df = pd.read_csv("data/sequence_results.csv")


# ==========================================
# COUNT HIGH-RISK SEQUENCES PER USER
# ==========================================

sequence_counts = (
    sequence_df[
        sequence_df["sequence_risk"] == "HIGH"
    ]
    .groupby("user_id")
    .size()
    .reset_index(name="high_sequence_count")
)


# ==========================================
# COMBINE DATA
# ==========================================

final_df = risk_df.merge(
    context_df,
    on="user_id",
    how="left"
)

final_df = final_df.merge(
    sequence_counts,
    on="user_id",
    how="left"
)

final_df["high_sequence_count"] = (
    final_df["high_sequence_count"]
    .fillna(0)
)


# ==========================================
# SEQUENCE SCORE
# ==========================================

def sequence_score(count):

    if count >= 5:
        return 20

    elif count >= 3:
        return 15

    elif count >= 1:
        return 10

    else:
        return 0


final_df["sequence_score"] = (
    final_df["high_sequence_count"]
    .apply(sequence_score)
)


# ==========================================
# ORIGINAL SCORE
# ==========================================

final_df["raw_score"] = (
    final_df["ml_score"]
    + final_df["shift_score"]
    + final_df["trend_score"]
    + final_df["sequence_score"]
)


# ==========================================
# CONTEXT ADJUSTMENT
# ==========================================

def apply_context(row):

    score = row["raw_score"]

    if row["context_status"] == "LEGITIMATE_CHANGE":

        # Reduce risk caused by legitimate changes
        score = score * 0.5

    return round(min(score, 100))


final_df["final_risk_score"] = (
    final_df.apply(
        apply_context,
        axis=1
    )
)


# ==========================================
# FINAL RISK LEVEL
# ==========================================

def risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


final_df["final_risk_level"] = (
    final_df["final_risk_score"]
    .apply(risk_level)
)


# ==========================================
# GENERATE EXPLANATION
# ==========================================

def generate_explanation(row):

    reasons = []

    if row["anomaly_count"] >= 5:

        reasons.append(
            f"{int(row['anomaly_count'])} anomalous events detected"
        )

    elif row["anomaly_count"] > 0:

        reasons.append(
            f"{int(row['anomaly_count'])} anomalous event(s) detected"
        )


    if row["shift_ratio"] >= 5:

        reasons.append(
            f"File activity reached "
            f"{row['shift_ratio']:.1f}x baseline"
        )

    elif row["shift_ratio"] >= 2:

        reasons.append(
            f"File activity increased "
            f"{row['shift_ratio']:.1f}x above baseline"
        )


    if row["trend_slope"] > 0.3:

        reasons.append(
            "Behavioral deviation is increasing over time"
        )

    elif row["trend_slope"] > 0:

        reasons.append(
            "Gradual behavioral change detected"
        )


    if row["high_sequence_count"] > 0:

        reasons.append(
            f"{int(row['high_sequence_count'])} "
            f"high-risk activity sequence(s)"
        )


    if row["context_status"] == "LEGITIMATE_CHANGE":

        reasons.append(
            f"Legitimate context: "
            f"{row['context_reason']}"
        )

    else:

        reasons.append(
            "No known legitimate context recorded"
        )


    if not reasons:

        reasons.append(
            "Behavior remains close to established baseline"
        )


    return " | ".join(reasons)


final_df["explanation"] = (
    final_df.apply(
        generate_explanation,
        axis=1
    )
)


# ==========================================
# SAVE FINAL RESULTS
# ==========================================

final_df.to_csv(
    "data/final_engine_results.csv",
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n")
print("=" * 70)
print("          SILENT SHIFT — FINAL RISK ENGINE")
print("=" * 70)

print()

display_columns = [
    "user_id",
    "final_risk_score",
    "final_risk_level",
    "explanation"
]

print(
    final_df[
        display_columns
    ].to_string(index=False)
)

print()
print("=" * 70)

print("\nResults saved to:")
print("data/final_engine_results.csv")