import pandas as pd
import random
from datetime import datetime, timedelta

# ==========================================
# CONFIGURATION
# ==========================================

NUM_USERS = 1000
NUM_EVENTS = 30000
DAYS = 30

random.seed(42)

# ==========================================
# AVAILABLE BEHAVIOURS
# ==========================================

actions = [
    "login",
    "file_access",
    "file_download",
    "file_upload",
    "email_access",
    "database_access"
]

locations = [
    "Bengaluru",
    "Mysuru",
    "Mangaluru",
    "Chennai",
    "Hyderabad"
]

# ==========================================
# CREATE USERS
# ==========================================

users = []

for i in range(1, NUM_USERS + 1):

    user_id = f"U{i:04d}"

    # Most users are normal
    behaviour = "normal"

    # Some users have legitimate changes
    if i <= 50:
        behaviour = "legitimate_change"

    # Some users demonstrate silent shift
    elif i <= 75:
        behaviour = "silent_shift"

    users.append({
        "user_id": user_id,
        "behaviour": behaviour
    })

# ==========================================
# GENERATE EVENTS
# ==========================================

events = []

start_date = datetime(2026, 8, 1)

# 30 events per user = 30,000 events
events_per_user = NUM_EVENTS // NUM_USERS

for user in users:

    user_id = user["user_id"]
    behaviour = user["behaviour"]

    # Give every user a normal location
    normal_location = random.choice(locations)

    # Give every user a normal working hour
    normal_start = random.randint(7, 10)
    normal_end = random.randint(16, 19)

    for event_number in range(events_per_user):

        day = event_number

        # ==========================================
        # NORMAL BEHAVIOUR
        # ==========================================

        hour = random.randint(normal_start, normal_end)
        location = normal_location

        action = random.choices(
            actions,
            weights=[
                20,   # login
                35,   # file access
                15,   # download
                10,   # upload
                10,   # email
                10    # database
            ]
        )[0]

        files_accessed = random.randint(1, 10)

        # ==========================================
        # LEGITIMATE CHANGE
        # ==========================================

        if behaviour == "legitimate_change" and day >= 15:

            # New project increases activity
            hour = random.randint(8, 19)

            location = random.choice([
                normal_location,
                "Mysuru"
            ])

            files_accessed = random.randint(5, 25)

            action = random.choices(
                actions,
                weights=[
                    10,
                    30,
                    25,
                    15,
                    10,
                    10
                ]
            )[0]

        # ==========================================
        # SILENT SHIFT
        # ==========================================

        elif behaviour == "silent_shift" and day >= 10:

            # Gradually increase suspicious behaviour
            shift_strength = day - 9

            files_accessed = random.randint(
                5 + shift_strength * 3,
                15 + shift_strength * 8
            )

            # Increasingly unusual working hours
            hour = random.randint(
                max(0, normal_start - shift_strength // 2),
                min(23, normal_end + shift_strength // 2)
            )

            # Gradually introduce unusual location
            if day >= 20:
                location = random.choice([
                    normal_location,
                    "Mysuru",
                    "Chennai"
                ])

            # More downloads as behaviour changes
            action = random.choices(
                actions,
                weights=[
                    5,
                    20,
                    40,
                    15,
                    5,
                    15
                ]
            )[0]

        # ==========================================
        # TIMESTAMP
        # ==========================================

        timestamp = start_date + timedelta(
            days=day,
            hours=hour,
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        events.append([
            user_id,
            behaviour,
            timestamp,
            action,
            location,
            files_accessed
        ])

# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    events,
    columns=[
        "user_id",
        "behaviour",
        "timestamp",
        "action",
        "location",
        "files_accessed"
    ]
)

# Sort chronologically
df = df.sort_values("timestamp")

# ==========================================
# SAVE DATA
# ==========================================

df.to_csv(
    "data/user_activity.csv",
    index=False
)

print("\n===================================")
print("SILENT SHIFT DATASET GENERATED")
print("===================================\n")

print("Users:", df["user_id"].nunique())
print("Events:", len(df))
print("Days:", DAYS)

print("\nEvents per user:")
print(df["user_id"].value_counts().describe())

print("\nAction distribution:")
print(df["action"].value_counts())

print("\nLocation distribution:")
print(df["location"].value_counts())

print("\nSaved to:")
print("data/user_activity.csv")