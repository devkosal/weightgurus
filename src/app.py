from datetime import datetime
import json
import os
from flask import Flask, render_template
from fire import Fire
import pytz

from main import WeightGurus

app = Flask(__name__)
DEFAULT_TIMEZONE = "America/New_York"
DEFAULT_LOOKBACK_DAYS = 14


def format_timestamp(timestamp):
    """Convert ISO 8601 UTC timestamp to Eastern Time (ET)"""
    utc_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))  # Convert to UTC datetime
    tz = pytz.timezone(os.environ.get("TIMEZONE", DEFAULT_TIMEZONE))  # Set to default Timezone
    et_dt = utc_dt.astimezone(tz)  # Convert to ET
    return et_dt.strftime("%A, %B %d, %Y at %I:%M %p")  # Example: "Thursday, March 13, 2025 at 01:44 PM"


@app.route("/")
def home():
    users_json = os.environ.get("USERS_JSON", "[]")  # Get JSON string from env
    users = json.loads(users_json)  # Parse it into a Python list

    if not users:
        return "No users configured.", 500

    weight_data = []

    for user in users:
        username, password, alias = user["username"], user["password"], user["alias"]

        try:
            wr = WeightGurus(username, password)
            operation = wr.get_latest(daily_lookback_days=DEFAULT_LOOKBACK_DAYS)
        except Exception as e:
            print(f"error getting {alias}'s data: {e}")
            continue

        weight_data.append({
            "alias": alias,
            "weight": operation["weight"] / 10,  # Convert to lbs
            "timestamp": format_timestamp(operation["entryTimestamp"]),
        })

    if not weight_data:
        return "No weight successfully data found for the configured users.", 500

    return render_template("index.html", primary_user=weight_data[0], other_users=weight_data[1:])


def app_run(
    debug: bool = True,
    host: str = "127.0.0.1",
    port: int = 5000,
):
    app.run(debug=debug, host=host, port=port)


if __name__ == "__main__":
    Fire(app_run)
