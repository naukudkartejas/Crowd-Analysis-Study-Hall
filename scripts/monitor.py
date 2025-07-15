import mysql.connector
from datetime import datetime
import os
import sys

# Get current script directory and data path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# Connect to DB
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="remb6uk",  # Your actual password
    database="studyhall"
)
cursor = conn.cursor()

def check_in(roll_no, name):
    cursor.execute("INSERT INTO studyhall_visits (roll_no, name, action) VALUES (%s, %s, 'IN')", (roll_no, name))
    conn.commit()
    print(f"{name} ({roll_no}) checked in.")

def check_out(roll_no):
    cursor.execute("SELECT name FROM studyhall_visits WHERE roll_no = %s ORDER BY timestamp DESC LIMIT 1", (roll_no,))
    result = cursor.fetchone()
    name = result[0] if result else "Unknown"
    cursor.execute("INSERT INTO studyhall_visits (roll_no, name, action) VALUES (%s, %s, 'OUT')", (roll_no, name))
    conn.commit()
    print(f"{name} ({roll_no}) checked out.")

def current_status():
    cursor.execute("""
        SELECT v.roll_no, v.name, v.timestamp
        FROM studyhall_visits v
        INNER JOIN (
            SELECT roll_no, MAX(timestamp) AS latest_time
            FROM studyhall_visits
            GROUP BY roll_no
        ) AS latest
        ON v.roll_no = latest.roll_no AND v.timestamp = latest.latest_time
        WHERE v.action = 'IN'
    """)
    rows = cursor.fetchall()
    print("\nCurrent People in Study Hall:")
    for row in rows:
        print(f"- {row[1]} ({row[0]}) - Last seen: {row[2]}")

def export_cleaned_csv():
    # Run the cleaning/export script externally
    print("Launching export_clean.py to generate cleaned CSV...")
    os.system(f"{sys.executable} {os.path.join(BASE_DIR, 'export_clean.py')}")

def main():
    while True:
        print("\n--- Study Hall Menu ---")
        print("1. Check In")
        print("2. Check Out")
        print("3. Show Current Status")
        print("4. Export Cleaned CSV for Power BI")
        print("5. Exit")

        choice = input("Choose option: ")

        if choice == '1':
            roll = input("Enter roll number: ")
            name = input("Enter name: ")
            check_in(roll, name)
        elif choice == '2':
            roll = input("Enter roll number: ")
            check_out(roll)
        elif choice == '3':
            current_status()
        elif choice == '4':
            export_cleaned_csv()
        elif choice == '5':
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
