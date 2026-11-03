import json
import sys
import urllib.request
from datetime import datetime


URL = "https://devops-midterm-project.vercel.app/api/health"
LOG_FILE = "uptime_status.log"


def check_health():
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    healthy = False

    try:
        with urllib.request.urlopen(URL, timeout=10) as response:
            data = json.load(response)

            if response.status == 200 and data.get("status") == "healthy":
                message = "SUCCESS: App is healthy."
                healthy = True
            else:
                message = "ERROR: App is not healthy."

    except Exception as error:
        message = f"ERROR: {error}"

    log_message = f"[{time}] {message}\n"
    print(log_message, end="")

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_message)

    return healthy


if __name__ == "__main__":
    if check_health():
        sys.exit(0)
    else:
        sys.exit(1)