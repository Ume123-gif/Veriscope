import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
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

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print("Random Forest training complete!")

y_pred = model.predict(X_test)

print(classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_
))