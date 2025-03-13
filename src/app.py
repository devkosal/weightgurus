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
    operation = json.loads(WeightGurus(
        os.environ["USERNAME"],
        os.environ["PASSWORD"],
    ).get_latest())
    return render_template(
        "index.html",
        weight=operation["weight"] / 10,
        timestamp=format_timestamp(operation["entryTimestamp"]),
        user_alias=os.environ.get("USER_ALIAS", "User"),
    )


if __name__ == "__main__":
    app.run(debug=True)
