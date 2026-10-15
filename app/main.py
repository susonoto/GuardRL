import os
from datetime import datetime, timezone
from itertools import count
from fastapi import FastAPI, HTTPException
from app.schemas import LogEvent, Decision
from app.detector import AnomalyDetector, event_features
from app.policy import FeedbackPolicy
from app.store import append_jsonl, read_jsonl, read_json, write_json

app = FastAPI(title="GuardRL", description="Human-approved log anomaly response prototype")
detector = AnomalyDetector()
policy = FeedbackPolicy()
alert_ids = count(1)
alerts: dict[int, dict] = {}

def utc_now():
    return datetime.now(timezone.utc).isoformat()

@app.get("/")
def root():
    return {"name": "GuardRL", "mode": "simulation_only", "approval_required": True}

@app.post("/logs")
def ingest(event: LogEvent):
    record = event.model_dump(mode="json")
    previous = read_jsonl("events.jsonl")
    ip_counts = {}
    for item in previous[-5000:]:
        ip_counts[item.get("src_ip")] = ip_counts.get(item.get("src_ip"), 0) + 1
    features = event_features(record, ip_counts)
    score = detector.score(features)
    recommendation = policy.recommend(score)
    alert_id = next(alert_ids)
    alert = {
        "alert_id": alert_id, "created_at": utc_now(), "event": record,
        "anomaly_score": round(score, 4), "recommendation": recommendation,
        "status": "pending_review" if recommendation == "propose_block" else "open",
        "decision": None
    }
    alerts[alert_id] = alert
    append_jsonl("events.jsonl", record)
    append_jsonl("alerts.jsonl", alert)
    return alert

@app.get("/alerts")
def list_alerts():
    return list(alerts.values())

@app.get("/alerts/{alert_id}")
def get_alert(alert_id: int):
    if alert_id not in alerts:
        raise HTTPException(404, "Alert not found")
    return alerts[alert_id]

@app.post("/alerts/{alert_id}/decision")
def decide(alert_id: int, decision: Decision):
    if alert_id not in alerts:
        raise HTTPException(404, "Alert not found")
    alert = alerts[alert_id]
    if alert["decision"] is not None:
        raise HTTPException(409, "This alert already has a decision")
    if alert["recommendation"] != "propose_block":
        raise HTTPException(400, "Only proposed-block alerts can be approved/rejected for blocking")
    ip = str(alert["event"]["src_ip"])
    alert["decision"] = {
        "employee_id": decision.employee_id,
        "decision": decision.decision,
        "reason": decision.reason,
        "ticket_id": decision.ticket_id,
        "decided_at": utc_now()
    }
    alert["status"] = "approved" if decision.decision == "approve" else "rejected"
    policy.feedback(alert["anomaly_score"], decision.decision)
    if decision.decision == "approve":
        # Deliberately simulated. Do not wire to a real firewall without auth,
        # RBAC, expiry, allowlists, rollback, and change-control review.
        blocks = read_json("blocks.json", [])
        if not any(b["ip"] == ip for b in blocks):
            blocks.append({"ip": ip, "approved_by": decision.employee_id,
                           "reason": decision.reason, "ticket_id": decision.ticket_id,
                           "created_at": utc_now(), "mode": "simulation_only"})
            write_json("blocks.json", blocks)
    append_jsonl("audit.jsonl", {"alert_id": alert_id, "ip": ip, **alert["decision"]})
    return {"alert": alert, "policy_feedback": policy.snapshot(),
            "block_action": "simulated_block_recorded" if decision.decision == "approve" else "no_block"}

@app.get("/blocks")
def blocks():
    return read_json("blocks.json", [])

@app.get("/audit")
def audit():
    return read_jsonl("audit.jsonl")

@app.get("/policy")
def policy_status():
    return policy.snapshot()
