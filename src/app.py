from datetime import datetime
import json
import os
from flask import Flask, render_template
import pytz

from main import WeightGurus

app = Flask(__name__)
DEFAULT_TIMEZONE = "America/New_York"


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

        # Get latest weight entry
        operation = json.loads(WeightGurus(username, password).get_latest())

        weight_data.append({
            "alias": alias,
            "weight": operation["weight"] / 10,  # Convert to lbs
            "timestamp": format_timestamp(operation["entryTimestamp"]),
        })

    return render_template("index.html", primary_user=weight_data[0], other_users=weight_data[1:])


if __name__ == "__main__":
    app.run(debug=True)
