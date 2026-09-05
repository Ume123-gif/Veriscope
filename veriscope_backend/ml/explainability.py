import pandas as pd
import shap
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"

features = pd.read_csv(DATA_DIR / "features.csv")

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
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

def get_shap_reasons(model, X, label_encoder, feature_columns, top_n=5):

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    predictions = model.predict(X)

    explanations = []

    for i in range(len(X)):
        predicted_class = int(predictions[i])
        class_name = label_encoder.inverse_transform([predicted_class])[0]
        values = shap_values[i, :, predicted_class]

        explanation = pd.DataFrame({
            "feature": feature_columns,
            "shap_value": values
        })

        explanation["abs_shap"] = (
            explanation["shap_value"].abs()
        )

        explanation = (
            explanation
            .sort_values("abs_shap", ascending=False)
            .head(top_n)
        )

        reasons = []

        for _, row in explanation.iterrows():
            if class_name == "normal":
                direction = "decreases" if row["shap_value"] > 0 else "increases"
            else:
                direction = "increases" if row["shap_value"] > 0 else "decreases"
            reasons.append({
                "feature": row["feature"],
                "shap_value": round(
                    float(row["shap_value"]), 4
                ),
                "direction": direction
            })

        explanations.append({
            "predicted_class": class_name,
            "reasons": reasons
        })

    return explanations


if __name__ == "__main__":

    model.fit(X_train, y_train)

    explanations = get_shap_reasons(
        model,
        X_test.head(5),
        label_encoder,
        feature_columns
    )

    for i, explanation in enumerate(explanations):
        print("\nTransaction:", i)
        print(
            "Predicted class:",
            explanation["predicted_class"]
        )
        print("Top reasons:")
        for reason in explanation["reasons"]:
            print(reason)