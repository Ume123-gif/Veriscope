class DecisionEngine:

    def decide(self, risk_score, risk_level, graph_score, anomaly_score):
        if risk_score >= 0.85:
            decision = "BLOCK"
        elif risk_score >= 0.70:
            decision = "HOLD"
        elif risk_score >= 0.50:
            decision = "REVIEW"
        else:
            decision = "ALLOW"

        return {
            "decision": decision,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "graph_score": graph_score,
            "anomaly_score": anomaly_score
        }

if __name__ == "__main__":
    engine = DecisionEngine()

    result = engine.decide(
        risk_score=0.805,
        risk_level="HIGH",
        graph_score=0.8,
        anomaly_score=0.7
    )

    print(result)