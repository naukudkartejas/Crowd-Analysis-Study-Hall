# refresh_scheduler.py

import subprocess
import time
import datetime

def log_message(msg):
    with open("D:\\CROWD-ANALYSIS-Project\\scripts\\refresh_log.txt", "a") as log:
        log.write(f"[{datetime.datetime.now()}] {msg}\n")

def run_powershell_script():
    log_message("Starting Power BI refresh.")
    try:
        subprocess.run([
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-File", "D:\\CROWD-ANALYSIS-Project\\scripts\\refresh_powerbi.ps1"
        ], check=True)
        log_message("Power BI refresh completed successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"Power BI refresh FAILED! Error: {e}")

def main():
    while True:
        run_powershell_script()
        log_message("Waiting 24 hours for next refresh...\n")
        time.sleep(86400)  # 24 hours

if __name__ == "__main__":
    main()
