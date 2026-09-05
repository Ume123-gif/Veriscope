import pandas as pd
from pathlib import Path

from ml.xgboost_model import predict_transactions
from ml.xgboost_model import label_encoder, feature_columns
from ml.explainability import get_shap_reasons
from ml.isolation_forest import get_isolation_predictions
from graph.ring_detection import get_graph_risk
from decision_engine import DecisionEngine

DATA_DIR = Path(__file__).resolve().parent / "Data"

class RiskAgent:

    def __init__(self):
        self.decision_engine = DecisionEngine()

    def assess(self, xgb_score, anomaly_score, graph_score):

        risk_score = (
            xgb_score * 0.50
            + anomaly_score * 0.20
            + graph_score * 0.30
        )

        if risk_score >= 0.75:
            risk_level = "HIGH"
        elif risk_score >= 0.50:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "risk_score": round(risk_score, 4),
            "risk_score_percent": round(risk_score * 100, 2),
            "risk_level": risk_level,
            "xgb_score": round(xgb_score, 4),
            "anomaly_score": round(anomaly_score, 4),
            "graph_score": round(graph_score, 4)
        }

    def analyze_transaction(self, transaction_id):

        features = pd.read_csv(DATA_DIR/"features.csv")

        transaction = features[features["transaction_id"] == transaction_id]
        if transaction.empty:
            raise ValueError(
                f"Transaction {transaction_id} not found."
            )
        transaction_index = transaction.index[0]
        transaction_row = transaction.iloc[0]

        # XGBoost
        xgb_result = predict_transactions(transaction)[0]
        xgb_score = xgb_result["fraud_probability"]

        # SHAP explanation
        shap_result = get_shap_reasons(
            model=xgb_result["model"],
            X=transaction[feature_columns],
            label_encoder=label_encoder,
            feature_columns=feature_columns,
            top_n=5
        )
        xgb_result.pop("model")

        # Isolation Forest
        _, anomaly_scores, _ = get_isolation_predictions()
        anomaly_score = float(
            anomaly_scores[transaction_index]
        )

        # Graph
        graph_risk = get_graph_risk()
        account_id = transaction_row["account_id"]
        graph_row = graph_risk[
            graph_risk["account_id"] == account_id
        ]
        if graph_row.empty:
            graph_score = 0.0
            community_id = None
        else:
            graph_score = float(
                graph_row.iloc[0]["graph_ring_score"]
            )
            community_id = int(
                graph_row.iloc[0]["community_id"]
            )

        # Risk Agent
        risk_result = self.assess(
            xgb_score=xgb_score,
            anomaly_score=anomaly_score,
            graph_score=graph_score
        )

        # Decision Engine
        decision_result = self.decision_engine.decide(
            risk_score=risk_result["risk_score"],
            risk_level=risk_result["risk_level"],
            graph_score=graph_score,
            anomaly_score=anomaly_score
        )

        return {
            "transaction_id": transaction_id,
            "account_id": account_id,
            "predicted_class": xgb_result["predicted_class"],
            "xgb_score": risk_result["xgb_score"],
            "shap_reasons": shap_result[0]["reasons"],
            "anomaly_score": risk_result["anomaly_score"],
            "graph_score": risk_result["graph_score"],
            "community_id": community_id,
            "risk_score": risk_result["risk_score"],
            "risk_score_percent": risk_result["risk_score_percent"],
            "risk_level": risk_result["risk_level"],
            "decision": decision_result["decision"]
        }
