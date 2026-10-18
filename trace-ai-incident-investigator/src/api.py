import json
import requests
from src.web_research import research_incident
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.metrics_analyzer import detect_metric_anomalies
from src.correlator import build_timeline, correlate_events
from src.investigator import investigate_incident


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "incidents.json"
app = FastAPI(title="TRACE API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173",],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InvestigationRequest(BaseModel):
    incident_id: str

def load_incident():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

@app.get("/")
def home():
    return {"message": "TRACE API is running"}

@app.post("/investigate")
def investigate(request: InvestigationRequest):
    incident = load_incident()
    if incident["incident_id"] != request.incident_id:
        raise HTTPException(status_code=404,detail="Incident not found",)
    anomalies = detect_metric_anomalies(incident["events"])
    timeline = build_timeline(incident["events"])
    correlations = correlate_events(incident["events"])
    investigation = investigate_incident(incident)
    try:
        external_research = research_incident(incident)
        external_research["status"] = ("completed" if external_research.get("sources") else "no_results")
    except (requests.RequestException,RuntimeError,ValueError,) as error:
        external_research = {
            "status": "failed",
            "query": None,
            "sources": [],
            "message": str(error),
        }

    return {
        "incident_id": incident["incident_id"],
        "service": incident["service"],
        "description": incident["description"],
        "technology": incident["technology"],

        "anomalies": anomalies,
        "timeline": timeline,
        "correlations": correlations,
        "hypotheses": investigation["hypotheses"],

        "external_research": external_research,
    }
