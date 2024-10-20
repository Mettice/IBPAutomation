# continuous_monitor.py

import schedule
import time
from main import main as run_ibpa


def monitor_ibpa():
    print("Running IBPA system...")
    results = run_ibpa()
    # Analyze results here
    print("IBPA run complete. Results:", results)


# Run the IBPA system every day at midnight
schedule.every().day.at("00:00").do(monitor_ibpa)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)