import pandas as pd

transactions = pd.read_csv("Data/transactions.csv")

# Extracting hour and day of the week from transaction time 
transactions["transaction_time"] = pd.to_datetime(
    transactions["transaction_time"]
)
transactions["hour"] = transactions["transaction_time"].dt.hour
transactions["day_of_week"] = transactions["transaction_time"].dt.dayofweek

transactions = transactions.sort_values("transaction_time")

# Transactions in the last 1 hour
velocity = (
    transactions
    .groupby("account_id")
    .rolling("1h", on="transaction_time")["transaction_id"]
    .count()
)
velocity = velocity.reset_index()
velocity = velocity.rename(columns={
    "transaction_id": "transactions_last_1h"
})
transactions = transactions.merge(
    velocity,
    on=["account_id", "transaction_time"],
    how="left"
)
transactions["transactions_last_1h"] -= 1
transactions["transactions_last_1h"] = transactions["transactions_last_1h"].astype(int)

# Transactions in the last 24 hours
daily_velocity = (
    transactions
    .groupby("account_id")
    .rolling("24h", on="transaction_time")["transaction_id"]
    .count()
)
daily_velocity = daily_velocity.reset_index()
daily_velocity = daily_velocity.rename(columns={
    "transaction_id": "transactions_last_24h"
})
transactions = transactions.merge(
    daily_velocity,
    on=["account_id", "transaction_time"],
    how="left"
)
transactions["transactions_last_24h"] -= 1
transactions["transactions_last_24h"] = transactions["transactions_last_24h"].astype(int)

# Amount Deviation
transactions["historical_median_amount"] = (
    transactions
    .groupby("account_id")["transaction_amount"]
    .transform(lambda x: x.shift(1))
    .expanding()
    .median()
)
transactions["has_amount_history"] = (
    transactions["historical_median_amount"].notna().astype(int)
)
transactions["amount_deviation"] = (
    transactions["transaction_amount"] / transactions["historical_median_amount"]
)
transactions["amount_deviation"] = (
    transactions["amount_deviation"].fillna(1.0)
)

# Accounts per Device
transactions["accounts_per_device"] = (
    transactions
    .groupby("device_id")["account_id"]
    .transform("nunique")
)

# Accounts per IP address
transactions["accounts_per_ip"] = (
    transactions
    .groupby("ip_address")["account_id"]
    .transform("nunique")
)

# Accounts per Card
transactions["accounts_per_card"] = (
    transactions
    .groupby("card_fingerprint")["account_id"]
    .transform("nunique")
)

# New Account
transactions["is_new_account"] = (
    transactions["account_age_days"] <= 30
).astype(int)

# Unusual Hour
transactions["transaction_time"] = (
    (transactions["hour"] < 6) |
    (transactions["hour"] >= 23)
).astype(int)

# Amount vs Global Median
global_median_amount = transactions["transaction_amount"].median()
transactions["amount_vs_global_median"] = (
    transactions["transaction_amount"] / global_median_amount
)

# Refund Risk
transactions["refund_risk"] = (
    transactions["refund_rate"] >= 0.50
).astype(int)

# Device Sharing Ratio
device_transaction_count = (
    transactions
    .groupby("device_id")["transaction_id"]
    .transform("count")
)
transactions["device_sharing_ratio"] = (
    transactions["accounts_per_device"] / 
    device_transaction_count
)

# IP Sharing Ratio
ip_transaction_count = (
    transactions
    .groupby("ip_address")["transaction_id"]
    .transform("count")
)
transactions["ip_sharing_ratio"] = (
    transactions["accounts_per_ip"] /
    ip_transaction_count
)

# Merging ground truth for complete model dataset
ground_truth = pd.read_csv("Data/ground_truth.csv")
features = pd.merge(transactions, ground_truth, on="transaction_id", how="left")
features = features.drop(columns=["account_id_y"])
features = features.rename(columns={"account_id_x": "account_id"})

# Saving all the features 
features.to_csv("Data/features.csv", index=False)
print("Features saved successfully!")
