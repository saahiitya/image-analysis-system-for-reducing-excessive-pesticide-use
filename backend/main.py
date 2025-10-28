from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import shutil
import uuid

from .core.model import analyze_image_and_metadata
from .core.db import Database
from .core.pesticide import compute_pesticide_plan, get_pesticide_catalog

APP_ENV_PORT = int(os.getenv("PORT", "8000"))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/workspace/backend/uploads")
DB_PATH = os.getenv("DB_PATH", "/workspace/backend/data/app.db")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

db = Database(DB_PATH)
app = FastAPI(title="CropGuard AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRecord(BaseModel):
    id: int
    crop_type: str
    image_path: str
    farm_size: float
    location: Optional[str]
    weather_conditions: Optional[str]
    disease_detected: str
    severity_assessment: str
    recommended_pesticides: List[str]
    total_amount_needed: str
    cost_estimate: str
    scan_timestamp: str

@app.on_event("startup")
def on_startup():
    db.init()

@app.get("/")
def root():
    return {"status": "ok", "service": "CropGuard AI Backend"}

@app.get("/api/catalog")
def catalog():
    return get_pesticide_catalog()

@app.get("/api/scan-history", response_model=List[ScanRecord])
def scan_history():
    rows = db.get_scans(limit=100)
    return [
        ScanRecord(
            id=row[0],
            crop_type=row[1],
            image_path=row[2],
            farm_size=row[3],
            location=row[4],
            weather_conditions=row[5],
            disease_detected=row[6],
            severity_assessment=row[7],
            recommended_pesticides=row[8].split("|") if row[8] else [],
            total_amount_needed=row[9],
            cost_estimate=row[10],
            scan_timestamp=row[11],
        ) for row in rows
    ]

@app.post("/api/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    crop_type: str = Form(...),
    farm_size: float = Form(...),
    location: Optional[str] = Form(None),
    weather_conditions: Optional[str] = Form(None),
):
    # Save upload
    file_ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
    saved_name = f"{uuid.uuid4().hex}{file_ext}"
    save_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run model analysis (stub) -> returns disease, severity, infected_area_fraction
    model_result = analyze_image_and_metadata(
        image_path=save_path,
        crop_type=crop_type,
        location=location,
        weather_conditions=weather_conditions,
    )

    # Compute pesticide plan and dosage/cost
    plan = compute_pesticide_plan(
        crop_type=crop_type,
        disease=model_result["disease_detected"],
        severity=model_result["severity_assessment"],
        farm_size_ha=float(farm_size),
        weather_conditions=weather_conditions,
    )

    # Persist
    db.insert_scan(
        crop_type=crop_type,
        image_path=save_path,
        farm_size=float(farm_size),
        location=location,
        weather_conditions=weather_conditions,
        disease_detected=model_result["disease_detected"],
        severity_assessment=model_result["severity_assessment"],
        recommended_pesticides="|".join(plan["recommended_treatment"]["primary_pesticides"]),
        total_amount_needed=plan["recommended_treatment"]["dosage_calculation"]["total_amount_needed"],
        cost_estimate=plan["recommended_treatment"]["dosage_calculation"]["cost_estimate"],
        scan_timestamp=datetime.utcnow().isoformat() + "Z",
    )

    return JSONResponse(
        {
            "recommendations": {
                "disease_detected": model_result["disease_detected"],
                "severity_assessment": model_result["severity_assessment"],
                "recommended_treatment": plan["recommended_treatment"],
            }
        }
    )


@app.get("/api/stats")
def stats():
    rows = db.get_scans(limit=10000)
    total_scans = len(rows)
    if total_scans == 0:
        return {
            "total_scans": 0,
            "healthy_percent": 0.0,
            "active_treatments": 0,
            "liters_recommended": 0.0,
            "cost_total_rupees": 0.0,
            "liters_saved": 0.0,
            "cost_saved_rupees": 0.0,
            "reduction_percent": 0.0,
        }

    def _to_float_cost(s: str) -> float:
        try:
            return float(s.replace("₹", "").strip())
        except Exception:
            return 0.0

    def _to_float_liters(s: str) -> float:
        try:
            return float(s.replace("L", "").strip())
        except Exception:
            return 0.0

    low_count = 0
    active_treatments = 0
    liters_total = 0.0
    cost_total = 0.0
    liters_saved_total = 0.0
    cost_saved_total = 0.0
    baseline_total = 0.0

    for row in rows:
        _, crop_type, _image_path, farm_size, _location, weather_conditions, disease, severity, _reco, total_amount, cost_estimate, _ts = row

        # Recommended plan (recompute to get numeric values reliably)
        reco = compute_pesticide_plan(
            crop_type=crop_type,
            disease=disease,
            severity=severity,
            farm_size_ha=float(farm_size),
            weather_conditions=weather_conditions,
        )
        liters = _to_float_liters(reco["recommended_treatment"]["dosage_calculation"]["total_amount_needed"])
        cost_rupees = _to_float_cost(reco["recommended_treatment"]["dosage_calculation"]["cost_estimate"])

        # Baseline plan: assume farmer would spray "high" severity without weather adjustment
        baseline = compute_pesticide_plan(
            crop_type=crop_type,
            disease=disease,
            severity="high",
            farm_size_ha=float(farm_size),
            weather_conditions=None,
        )
        baseline_liters = _to_float_liters(baseline["recommended_treatment"]["dosage_calculation"]["total_amount_needed"])
        baseline_cost = _to_float_cost(baseline["recommended_treatment"]["dosage_calculation"]["cost_estimate"])

        liters_total += liters
        cost_total += cost_rupees
        baseline_total += baseline_liters

        saved_liters = max(baseline_liters - liters, 0.0)
        saved_cost = max(baseline_cost - cost_rupees, 0.0)
        liters_saved_total += saved_liters
        cost_saved_total += saved_cost

        if severity == "low":
            low_count += 1
        if severity in ("moderate", "high"):
            active_treatments += 1

    healthy_percent = round((low_count / total_scans) * 100.0, 1)
    reduction_percent = round((liters_saved_total / baseline_total) * 100.0, 1) if baseline_total > 0 else 0.0

    return {
        "total_scans": total_scans,
        "healthy_percent": healthy_percent,
        "active_treatments": active_treatments,
        "liters_recommended": round(liters_total, 2),
        "cost_total_rupees": round(cost_total, 2),
        "liters_saved": round(liters_saved_total, 2),
        "cost_saved_rupees": round(cost_saved_total, 2),
        "reduction_percent": reduction_percent,
    }
