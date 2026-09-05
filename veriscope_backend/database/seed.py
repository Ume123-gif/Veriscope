import pandas as pd
from pathlib import Path

from database.db import SessionLocal, Transaction

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"

transactions = pd.read_csv(DATA_DIR / "transactions.csv")

db = SessionLocal()

try:
    for _, row in transactions.iterrows():
        transaction = Transaction(
            transaction_id=row["transaction_id"],
            account_id=row["account_id"],
            transaction_amount=float(row["transaction_amount"]),
            transaction_time=pd.to_datetime(row["transaction_time"]).to_pydatetime()
        )

        db.add(transaction)

    db.commit()

    print(f"Inserted {len(transactions)} transactions successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()