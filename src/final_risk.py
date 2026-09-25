import pandas as pd

# Load previous results
risk_df = pd.read_csv("data/risk_results.csv")
context_df = pd.read_csv("data/context_results.csv")

# Combine risk + context
final_df = risk_df.merge(
    context_df,
    on="user_id",
    how="left"
)

# --------------------------------
# Adjust risk based on context
# --------------------------------

def adjust_risk(row):

    score = row["risk_score"]

    # Legitimate change reduces risk
    if row["context_status"] == "LEGITIMATE_CHANGE":

        score = score * 0.5

    return round(score)


final_df["final_risk_score"] = final_df.apply(
    adjust_risk,
    axis=1
)

# --------------------------------
# Final risk level
# --------------------------------

def get_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


final_df["final_risk_level"] = (
    final_df["final_risk_score"]
    .apply(get_risk_level)
)

# --------------------------------
# Save
# --------------------------------

final_df.to_csv(
    "data/final_results.csv",
    index=False
)

print("\n===== FINAL SILENT SHIFT RESULTS =====\n")

print(
    final_df[
        [
            "user_id",
            "risk_score",
            "context_status",
            "final_risk_score",
            "final_risk_level"
        ]
    ].to_string(index=False)
)

print("\nResults saved to:")
print("data/final_results.csv")
