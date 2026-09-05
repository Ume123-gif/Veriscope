from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
import sys
import json

from database.db import (
    SessionLocal,
    Transaction,
    RiskAnalysis,
    AuditLog
)

sys.path.append(str(Path(__file__).resolve().parent.parent))

from risk_agent import RiskAgent

app = FastAPI(
    title="Veriscope API",
    description="Real-time transaction fraud risk intelligence engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = RiskAgent()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Veriscope"
    }

@app.get("/metrics")
def get_metrics():

    import pandas as pd

    ground_truth_path = (
        Path(__file__).resolve().parent.parent
        / "Data"
        / "ground_truth.csv"
    )
    ground_truth = pd.read_csv(ground_truth_path)

    total_transactions = len(ground_truth)
    fraud_cases = int(ground_truth["is_fraud"].sum())
    fraud_ring_cases = int(
        ground_truth["is_fraud_ring"].sum()
    )
    behavioral_anomalies = int(
        ground_truth["is_behavioral_anomaly"].sum()
    )
    normal_transactions = int(
        (ground_truth["is_fraud"] == 0).sum()
    )

    return {
        "total_transactions": total_transactions,
        "fraud_cases": fraud_cases,
        "fraud_ring_cases": fraud_ring_cases,
        "behavioral_anomalies": behavioral_anomalies,
        "normal_transactions": normal_transactions
    }

@app.get("/audit-trail")
def get_audit_trail(limit: int = 20):

    db: Session = SessionLocal()

    try:
        logs = (
            db.query(AuditLog)
            .order_by(AuditLog.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "transaction_id": log.transaction_id,
                "action": log.action,
                "decision": log.decision,
                "risk_score": log.risk_score,
                "timestamp": log.timestamp
            }
            for log in logs
        ]

    finally:
        db.close()

@app.get("/transactions/{transaction_id}/risk")
def analyze_transaction(transaction_id: str):

    db: Session = SessionLocal()

    try:

        # Run complete risk intelligence engine
        result = agent.analyze_transaction(transaction_id)

        # Store risk analysis

        existing_analysis = (
            db.query(RiskAnalysis)
            .filter(
                RiskAnalysis.transaction_id == transaction_id
            )
            .first()
        )
        if existing_analysis:
            analysis = existing_analysis
            analysis.predicted_class = result["predicted_class"]
            analysis.xgb_score = result["xgb_score"]
            analysis.anomaly_score = result["anomaly_score"]
            analysis.graph_score = result["graph_score"]
            analysis.risk_score = result["risk_score"]
            analysis.risk_score_percent = result["risk_score_percent"]
            analysis.risk_level = result["risk_level"]
            analysis.decision = result["decision"]
            analysis.community_id = result.get("community_id")
            analysis.shap_reasons = json.dumps(
                result.get("shap_reasons", [])
            )

        else:
            analysis = RiskAnalysis(
                transaction_id=transaction_id,
                predicted_class=result["predicted_class"],
                xgb_score=result["xgb_score"],
                anomaly_score=result["anomaly_score"],
                graph_score=result["graph_score"],
                risk_score=result["risk_score"],
                risk_score_percent=result["risk_score_percent"],
                risk_level=result["risk_level"],
                decision=result["decision"],
                community_id=result.get("community_id"),
                shap_reasons=json.dumps(
                    result.get("shap_reasons", [])
                )
            )
            db.add(analysis)

        # Store audit event
        audit = AuditLog(
            transaction_id=transaction_id,
            action="RISK_ANALYSIS",
            decision=result["decision"],
            risk_score=result["risk_score"]
        )
        db.add(audit)

        # Commit
        db.commit()

        return result

    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        db.close()