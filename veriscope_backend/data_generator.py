import random
import uuid
from pathlib import Path
import numpy as np
import pandas as pd
from faker import Faker
from datetime import timedelta

#Reproducibility

SEED = 42

random.seed(SEED)
np.random.seed(SEED)

fake = Faker()
fake.seed_instance(SEED)

#Data Configuration

NUM_ACCOUNTS = 1000
TRANSACTIONS_PER_ACCOUNT = 10

NUM_DEVICES = 850
NUM_IP_ADDRESSES = 800
NUM_CARDS = 950

NUM_FRAUD_RINGS = 10
MIN_RING_SIZE = 4
MAX_RING_SIZE = 10

NUM_BEHAVORIAL_ANOMALIES = 50
NUM_VELOCITY_ACCOUNTS = 50
VELOCITY_PROBABILITY = 0.20

OUTPUT_DIR = Path("Data")

#ID Generator
def generate_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

#Account Generation

def generate_accounts(num_accounts):
    accounts = []
    current_time = pd.Timestamp.now()

    for _ in range(num_accounts):
        account_id = generate_id("ACC")

        created_at = fake.date_time_between(
            start_date="-5y",
            end_date="now"
        )

        created_at = pd.Timestamp(created_at)

        account_age_days = max(0, (current_time - created_at).days)

        accounts.append({
            "account_id": account_id,
            "created_at": created_at,
            "account_age_days": account_age_days
        })

    return pd.DataFrame(accounts)

#Infrastructure Pools

def generate_device_pool(num_devices):
    return [
       generate_id("DEV")
        for _ in range(num_devices)
    ]

def generate_ip_pool(num_ips):
    return [
        fake.ipv4()
        for _ in range(num_ips)
    ]

def generate_card_pool(num_cards):
    return [
        generate_id("CARD")
        for _ in range(num_cards)
    ]

#Normal Infrastructure Assignment

def assign_normal_infrastructure(accounts, devices, ips, cards):
    account_ids = accounts["account_id"].tolist()
    assignments = {}

    for account_id in account_ids:
        device = random.choice(devices)
        ip_address = random.choice(ips)
        card = random.choice(cards)

        assignments[account_id] = {
            "device_id": device,
            "ip_address": ip_address,
            "card_fingerprint": card
        }

    return assignments

#Fraud Ring Generation

def generate_fraud_rings(account_ids, num_rings, min_size, max_size):

    available_accounts = account_ids.copy()
    fraud_rings = []
    account_to_ring = {}

    for ring_number in range(1, num_rings + 1):
        if len(available_accounts) < min_size:
            break
        ring_size = random.randint(min_size, min(max_size, len(available_accounts)))
        members = random.sample(available_accounts, ring_size)
        ring_id = f"RING_{ring_number:03d}"
        fraud_rings.append({
            "ring_id": ring_id,
            "members": members
        })

        for account_id in members:
            account_to_ring[account_id] = ring_id
            available_accounts.remove(account_id)

    return fraud_rings, account_to_ring

#Inject Fraud Ring Infrastructure

def inject_fraud_ring_infrastructure(fraud_rings, assignments, devices, ips, cards):
    ring_metadata = []

    for index, ring in enumerate(fraud_rings):
        ring_id = ring["ring_id"]
        members = ring["members"]

        ring_types = ["device_ring", "ip_ring", "card_ring", "multi_attribute_ring"]
        ring_type = ring_types[index % len(ring_types)]

        shared_device = f"RING_DEVICE_{index + 1:03d}"
        shared_ip = f"10.250.{index + 1}.1"
        shared_card = f"RING_CARD_{index + 1:03d}"

        for account_id in members:
            if ring_type in [
                "device_ring", "multi_attribute_ring"
            ]:
                assignments[account_id]["device_id"] = shared_device
            if ring_type in [
                "ip_ring", "multi_attribute_ring"
            ]:
                assignments[account_id]["ip_address"] = shared_ip
            if ring_type in [
                "card_ring", "multi_attribute_ring"
            ]:
                assignments[account_id]["card_fingerprint"] = shared_card

        ring_metadata.append({
            "ring_id": ring_id,
            "ring_type": ring_type,
            "ring_size": len(members)
        })

    return pd.DataFrame(ring_metadata)

#Generate Transactions

def generate_transactions(accounts, assignments, account_to_ring, num_transactions):
    transactions = []
    anomaly_accounts = set(random.sample(accounts["account_id"].tolist(), min(NUM_BEHAVORIAL_ANOMALIES, len(accounts))))
    velocity_accounts = set(random.sample(accounts["account_id"].tolist(), min(NUM_VELOCITY_ACCOUNTS, len(accounts))))

    for _, account in accounts.iterrows():
        account_id = account["account_id"]
        infrastructure = assignments[account_id]
        is_ring_account = account_id in account_to_ring 
        is_anomaly_account = account_id in anomaly_accounts 
        is_velocity_account = account_id in velocity_accounts

        last_transaction_time = None
        for _ in range(num_transactions):

            #Base Transation behaviour
            if is_ring_account:
                amount = np.random.lognormal(mean=7.8, sigma=0.9)
                refund_rate = np.random.uniform(0.15, 0.55)
            else:
                amount = np.random.lognormal(mean=7.0, sigma=0.65)
                refund_rate = np.random.uniform(0.01, 0.18)

            #Behavioral Anomaly injection
            if is_anomaly_account:
                anomaly_type = random.choice([
                    "large_amount", "high_refund_rate", "young_account_high_amount"
                ])  
                if anomaly_type == "large_amount":
                    amount *= random.uniform(5, 10)
                elif anomaly_type == "high_refund_rate":
                    refund_rate = random.uniform(0.60, 0.95)
                elif anomaly_type == "young_account_high_amount":
                    amount *= random.uniform(4, 10)

            #Transaction Timestamp

            if is_velocity_account and random.random() < VELOCITY_PROBABILITY:
                if last_transaction_time:
                    transaction_time = last_transaction_time + timedelta(minutes=random.randint(1, 15), seconds=random.randint(0, 60))
                else:
                    transaction_time = fake.date_time_between(start_date="-90d", end_date="now")
            else:
                if last_transaction_time:
                    transaction_time = last_transaction_time + timedelta(days=random.randint(1, 10, hours=random.randint(0, 23), minutes=random.randint(0, 59)))
                else:
                    transaction_time = fake.date_time_between(start_date="-90d", end_date="now")

            transaction_time = pd.Timestamp(transaction_time)
            last_transaction_time = transaction_time

            #Transaction Record
            transactions.append({
                "transaction_id": generate_id("TXN"),
                "account_id": account_id,
                "device_id": infrastructure["device_id"],
                "ip_address": infrastructure["ip_address"],
                "card_fingerprint": infrastructure["card_fingerprint"],
                "transaction_amount": round(max(amount, 1), 2),
                "transaction_time": transaction_time,
                "account_age_days": account["account_age_days"],
                "refund_rate": round(refund_rate, 4)
            })

    return pd.DataFrame(transactions), anomaly_accounts
                                
#Create Ground Truth (Not to be given as input to ML models!)

def create_ground_truth(transactions, account_to_ring, anomaly_accounts):
    ground_truth = transactions[["transaction_id", "account_id"]].copy()
    ground_truth["is_fraud_ring"] = (
        ground_truth["account_id"].isin(account_to_ring)
    )
    ground_truth["is_behavioral_anomaly"] = (
        ground_truth["account_id"].isin(anomaly_accounts)
    )  
    ground_truth["is_fraud"] = (
        ground_truth["is_fraud_ring"] | ground_truth["is_behavioral_anomaly"]
    )
    ground_truth["fraud_type"] = "normal"
    ground_truth.loc[ground_truth["is_fraud_ring"], "fraud_type"] = "fraud_ring"  
    ground_truth.loc[(ground_truth["is_behavioral_anomaly"] & ~ground_truth["is_fraud_ring"]), "fraud_type"] = "behavioral_anomaly"
    ground_truth.loc[(ground_truth["is_fraud_ring"] & ground_truth["is_behavioral_anomaly"]), "fraud_type"] = "ring_and_anomaly"
    ground_truth["fraud_ring_id"] = (ground_truth["account_id"].map(account_to_ring))   
    return ground_truth 

#Data Validation

def validate_dataset(accounts, transactions, ground_truth):

    print("\n" + "_" * 60)
    print("DATA VALIDATION")
    print("_" * 60)

    print("\nAccounts:")
    print(accounts.shape)

    print("\nTransactions:")
    print(transactions.shape)

    print("\nMissing Values:")
    print(transactions.isnull().sum())

    print("\nDuplicate transaction IDs:")
    print(transactions["transaction_id"].duplicated().sum())

    print("\nFraud distribution:")
    print(ground_truth["fraud_type"].value_counts())

    print("\nFraud percentage:")
    print(round(ground_truth["is_fraud"].mean() * 100, 2), "%")

    print("\nTransaction amount statistics:")
    print(transactions["transaction_amount"].describe())

    print("\nAccount age statistics:")
    print(transactions["account_age_days"].describe())

    print("\nRefund rate statistics:")
    print(transactions["refund_rate"].describe())

    assert transactions["transaction_id"].is_unique
    assert transactions["transaction_amount"].ge(0).all()
    assert transactions["account_age_days"].ge(0).all()
    assert transactions["refund_rate"].between(0, 1).all()

    print("\nValidation checks passed.")

#Save Data

def save_data(accounts, transactions, ground_truth, ring_metadata):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    accounts.to_csv(OUTPUT_DIR/"accounts.csv", index=False)
    transactions.to_csv(OUTPUT_DIR/"transactions.csv", index=False)
    ground_truth.to_csv(OUTPUT_DIR/"ground_truth.csv", index=False)
    ring_metadata.to_csv(OUTPUT_DIR/"fraud_rings.csv", index=False)

    print("\nData saved to:")
    print(OUTPUT_DIR.resolve())


#MAIN PIPELINE

def main():

    print("=" * 60)
    print("VERISCOPE SYNTHETIC DATA GENERATOR")
    print("-" * 60)

    #Generate accounts
    accounts = generate_accounts(NUM_ACCOUNTS)
    print(f"\nGenerated {len(accounts)} accounts.")

    #Generate infrastructure pools
    devices = generate_device_pool(NUM_DEVICES)
    ips = generate_ip_pool(NUM_IP_ADDRESSES) 
    cards = generate_card_pool(NUM_CARDS)
    print(f"Generated {len(devices)} devices.")
    print(f"Generated {len(ips)} IP addresses.")
    print(f"Generated {len(cards)} card fingerprints.")

    #Assign normal infrastructure
    assignments = assign_normal_infrastructure(accounts, devices, ips, cards)

    #Generate fraud rings
    account_ids = accounts["account_id"].to_list()
    fraud_rings, account_to_ring = generate_fraud_rings(account_ids, NUM_FRAUD_RINGS, MIN_RING_SIZE, MAX_RING_SIZE)
    print(f"\nGenerated {len(fraud_rings)} fraud rings.")

    #Inject fraud-ring relationships
    ring_metadata = inject_fraud_ring_infrastructure(fraud_rings, assignments, devices, ips, cards)

    #Generate transactions
    transactions, anomaly_accounts = generate_transactions(accounts, assignments, account_to_ring, TRANSACTIONS_PER_ACCOUNT)
    print(f"Generated {len(transactions)} transactions.")

    #Create labels separately
    ground_truth = create_ground_truth(transactions, account_to_ring, anomaly_accounts)

    #Validate 
    validate_dataset(accounts, transactions, ground_truth)

    #Save
    save_data(accounts, transactions, ground_truth, ring_metadata)

    print("\n" + "-" * 60)
    print("VERISCOPE DATA GENERATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()