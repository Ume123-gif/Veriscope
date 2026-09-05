import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

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
y = features["fraud_type"]

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

def get_xgb_predictions():

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)

    fraud_probability = 1 - y_proba[:, 2]

    return y_pred, fraud_probability, model

def predict_transactions(transactions):

    model.fit(X_train, y_train)

    transaction_features = transactions[feature_columns]

    predictions = model.predict(transaction_features)
    probabilities = model.predict_proba(transaction_features)

    normal_class = label_encoder.transform(["normal"])[0]

    fraud_probabilities = 1 - probabilities[:, normal_class]

    predicted_classes = label_encoder.inverse_transform(predictions)

    results = []

    for i in range(len(transactions)):

        results.append({
            "transaction_id": transactions.iloc[i]["transaction_id"],
            "predicted_class": predicted_classes[i],
            "fraud_probability": float(fraud_probabilities[i]),
            "model": model
        })

    return results

if __name__ == "__main__":
    y_pred, fraud_probability, model = get_xgb_predictions()

    print("Model training complete!")

    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    ))