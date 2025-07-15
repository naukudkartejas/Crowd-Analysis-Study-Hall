import mysql.connector
import pandas as pd
import os
import sys

# Paths setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
CSV_FILE = os.path.join(DATA_DIR, "studyhall_cleaned.csv")

print(f"Base directory: {BASE_DIR}")
print(f"Data directory: {DATA_DIR}")
print(f"CSV file path: {CSV_FILE}")

# Ensure data directory exists
try:
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"✅ Data directory ensured: {DATA_DIR}")
except Exception as e:
    print(f"❌ Failed to create data directory: {e}")
    sys.exit(1)

# Connect to MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="remb6uk",  # Replace with your password
        database="studyhall"
    )
    print("✅ Connected to MySQL database")
except mysql.connector.Error as err:
    print(f"❌ MySQL connection error: {err}")
    sys.exit(1)

def export_cleaned_csv():
    try:
        print("Fetching data from database...")
        df = pd.read_sql("SELECT * FROM studyhall_visits ORDER BY roll_no, timestamp", conn)
        print(f"Rows fetched: {len(df)}")
    except Exception as e:
        print(f"❌ Error fetching data from DB: {e}")
        return

    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except Exception as e:
        print(f"❌ Error converting timestamps: {e}")
        return

    # Generate session IDs
    try:
        df['session_id'] = df.groupby('roll_no').cumcount() // 2 + 1
    except Exception as e:
        print(f"❌ Error generating session IDs: {e}")
        return

    try:
        df_in = df[df['action'] == 'IN'].copy()
        df_out = df[df['action'] == 'OUT'].copy()
        print(f"IN entries: {len(df_in)}, OUT entries: {len(df_out)}")
    except Exception as e:
        print(f"❌ Error splitting IN/OUT entries: {e}")
        return

    try:
        session_df = pd.merge(
            df_in, df_out,
            on=['roll_no', 'session_id'],
            suffixes=('_in', '_out')
        )
        print(f"Merged sessions count: {len(session_df)}")
    except Exception as e:
        print(f"❌ Error merging IN/OUT sessions: {e}")
        return

    try:
        session_df['duration_minutes'] = (
            session_df['timestamp_out'] - session_df['timestamp_in']
        ).dt.total_seconds() / 60
    except Exception as e:
        print(f"❌ Error calculating duration: {e}")
        return

    try:
        session_df['day'] = session_df['timestamp_in'].dt.date
        session_df['hour_in'] = session_df['timestamp_in'].dt.hour
        session_df['weekday'] = session_df['timestamp_in'].dt.day_name()
    except Exception as e:
        print(f"❌ Error creating additional time fields: {e}")
        return

    try:
        final_df = session_df[[
            'roll_no',
            'name_in',
            'timestamp_in',
            'timestamp_out',
            'duration_minutes',
            'day',
            'hour_in',
            'weekday',
            'session_id'
        ]].rename(columns={'name_in': 'name'})

        print("\nPreview of final dataframe:")
        print(final_df.head())
    except Exception as e:
        print(f"❌ Error preparing final dataframe: {e}")
        return

    try:
        final_df.to_csv(CSV_FILE, index=False)
        print(f"\n✅ Successfully wrote CSV file at: {CSV_FILE}")
    except Exception as e:
        print(f"❌ Failed to write CSV file: {e}")

if __name__ == "__main__":
    export_cleaned_csv()
