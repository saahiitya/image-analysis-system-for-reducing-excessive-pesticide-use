import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, request, jsonify
import requests
import json

# SQLite database file
DB = "farmer_data.db"

# OpenWeather API key from environment variable
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise RuntimeError("Set OPENWEATHER_API_KEY environment variable first.")

# Initialize Flask app
app = Flask(__name__)

# Helper to get SQLite connection
def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

# Helper to get current UTC time in ISO format
def iso_now():
    return datetime.now(timezone.utc).isoformat()

# Route to save farmer location and fetch weather
@app.route("/save", methods=["POST"])
def save_location_and_weather():
    data = request.get_json(force=True)
    lat = data.get("lat")
    lon = data.get("lon")
    farmer_id = data.get("farmer_id")

    if lat is None or lon is None:
        return jsonify({"error": "lat and lon required"}), 400

    con = get_db()
    cur = con.cursor()
    ts = iso_now()

    # Save location
    cur.execute(
        "INSERT INTO locations (farmer_id, latitude, longitude, timestamp) VALUES (?,?,?,?)",
        (farmer_id, float(lat), float(lon), ts)
    )
    loc_id = cur.lastrowid

    # Fetch weather from OpenWeather
    base = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    wresp = requests.get(base, params=params, timeout=10).json()

    weather = {
        "temp": wresp.get("main", {}).get("temp"),
        "feels_like": wresp.get("main", {}).get("feels_like"),
        "pressure": wresp.get("main", {}).get("pressure"),
        "humidity": wresp.get("main", {}).get("humidity"),
        "wind_speed": wresp.get("wind", {}).get("speed"),
        "description": wresp.get("weather", [{}])[0].get("description"),
        "raw_json": json.dumps(wresp)
    }

    # Save weather in database
    cur.execute(
        """INSERT INTO weather
           (location_id, temp, feels_like, pressure, humidity, wind_speed, description, raw_json, timestamp)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (loc_id, weather["temp"], weather["feels_like"], weather["pressure"],
         weather["humidity"], weather["wind_speed"], weather["description"],
         weather["raw_json"], iso_now())
    )

    con.commit()
    con.close()

    return jsonify({"location_id": loc_id, "weather": weather}), 201

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
