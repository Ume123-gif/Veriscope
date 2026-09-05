import pandas as pd
from pathlib import Path

from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

DATA_DIR = Path(__file__).resolve().parent.parent/"Data"

features = pd.read_csv(DATA_DIR/"features.csv")

feature_columns = [
    "transaction_amount",
    "account_age_days",
    "refund_rate",
    "hour",
    "day_of_week",
    "transactions_last_1h",
    "transactions_last_24h",
    "has_amount_history",
    "amount_deviation",
    "accounts_per_device",
    "accounts_per_ip",
    "accounts_per_card",
    "is_new_account",
    "amount_vs_global_median",
    "refund_risk",
    "device_sharing_ratio",
    "ip_sharing_ratio"
]

X = features[feature_columns]

model = IsolationForest(
    n_estimators=300,
    contamination=0.117,
    random_state=42,
    n_jobs=-1
)

def get_isolation_predictions():
    model.fit(X)

    predictions = model.predict(X)
    raw_scores = model.decision_function(X)

    anomaly_score = 1 - (
        (raw_scores - raw_scores.min()) 
        / (raw_scores.max() - raw_scores.min())
    )

    return predictions, anomaly_score, model

if __name__ == "__main__":
    predictions, anomaly_score, model = get_isolation_prediction()
    print("Model training complete!")

    actual_fraud = features["is_fraud"]
    predicted_anomaly = (predictions == -1).astype(int)

    print(classification_report(
        actual_fraud,
        predicted_anomaly,
        target_names=["Normal", "Fraud"]
    ))

