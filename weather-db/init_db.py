import sqlite3

DB = "farmer_data.db"

schema = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    temp REAL,
    feels_like REAL,
    pressure INTEGER,
    humidity INTEGER,
    wind_speed REAL,
    description TEXT,
    raw_json TEXT,
    timestamp TEXT NOT NULL,
    FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE CASCADE
);
"""

def init():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executescript(schema)
    con.commit()
    con.close()
    print("Initialized DB:", DB)

if __name__ == "__main__":
    init()
