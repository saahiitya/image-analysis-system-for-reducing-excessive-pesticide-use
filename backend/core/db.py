import sqlite3
from typing import List, Tuple, Optional

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_type TEXT NOT NULL,
    image_path TEXT NOT NULL,
    farm_size REAL NOT NULL,
    location TEXT,
    weather_conditions TEXT,
    disease_detected TEXT NOT NULL,
    severity_assessment TEXT NOT NULL,
    recommended_pesticides TEXT,
    total_amount_needed TEXT,
    cost_estimate TEXT,
    scan_timestamp TEXT NOT NULL
);
"""

class Database:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def init(self) -> None:
        conn = self._conn()
        try:
            conn.execute(SCHEMA_SQL)
            conn.commit()
        finally:
            conn.close()

    def insert_scan(
        self,
        crop_type: str,
        image_path: str,
        farm_size: float,
        location: Optional[str],
        weather_conditions: Optional[str],
        disease_detected: str,
        severity_assessment: str,
        recommended_pesticides: str,
        total_amount_needed: str,
        cost_estimate: str,
        scan_timestamp: str,
    ) -> None:
        conn = self._conn()
        try:
            conn.execute(
                """
                INSERT INTO scans (
                    crop_type, image_path, farm_size, location, weather_conditions,
                    disease_detected, severity_assessment, recommended_pesticides,
                    total_amount_needed, cost_estimate, scan_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    crop_type,
                    image_path,
                    farm_size,
                    location,
                    weather_conditions,
                    disease_detected,
                    severity_assessment,
                    recommended_pesticides,
                    total_amount_needed,
                    cost_estimate,
                    scan_timestamp,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def get_scans(self, limit: int = 100) -> List[Tuple]:
        conn = self._conn()
        try:
            cur = conn.execute(
                "SELECT id, crop_type, image_path, farm_size, location, weather_conditions, disease_detected, severity_assessment, recommended_pesticides, total_amount_needed, cost_estimate, scan_timestamp FROM scans ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            return cur.fetchall()
        finally:
            conn.close()
