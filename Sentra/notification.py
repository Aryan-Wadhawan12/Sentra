import time
from datetime import datetime
from plyer import notification
import requests
import os
import sys

# --- Pushover credentials ---
PUSHOVER_USER_KEY = "uwoh5udzdqw7puu7gja88n8kqhk6gd"
PUSHOVER_APP_TOKEN = "a2hffrstb4kahwrdnvkf9hof87xah5"

# --- Cross-platform path handling ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # When compiled with PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

log_file = resource_path("stranger1_log.csv")
last_seen_line = 0
last_notified_window = None

# --- Notification block-based logic ---
def get_5_min_window():
    now = datetime.now()
    return f"{now.hour}:{(now.minute // 5) * 5:02d}"

def send_pushover_notification(message, title="Stranger Alert"):
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": title
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ iPhone notification sent.")
    else:
        print("❌ Error:", response.text)

def send_windows_notification(message):
    notification.notify(
        title="Stranger Alert",
        message=message,
        app_name="Security Monitor",
        timeout=10
    )

# --- Main loop ---
while True:
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            lines = file.readlines()
            new_lines = lines[last_seen_line:]

            for line in new_lines:
                if "Stranger" in line:
                    current_window = get_5_min_window()
                    if current_window != last_notified_window:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        msg = f"Stranger detected at {timestamp}"
                        send_windows_notification(msg)
                        send_pushover_notification(msg)
                        last_notified_window = current_window

            last_seen_line = len(lines)
    else:
        print("Waiting for log file...")

    time.sleep(2)
