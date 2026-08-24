"""
One-off script to seed the transaction table with 20 demo records.
Run it once after the API has created the table (i.e. after uvicorn
has started at least once), or run it standalone -- it creates the
table itself too.

Usage:
    python seed.py
"""

import random
from datetime import date, timedelta

from app.database import SessionLocal, engine, Base
from app.models import Transaction, TransactionType, TransactionHead

Base.metadata.create_all(bind=engine)

VENDORS = [
    "Acme Traders", "Bluewave Suppliers", "Sunrise Logistics", "Nova Retail",
    "Kiran Enterprises", "Metro Distributors", "Orbit Textiles", "Delta Foods",
    "Skyline Hardware", "Prime Consultants",
]

DESCRIPTIONS = {
    TransactionHead.COFFEE_BEANS: "Purchase of raw coffee beans",
    TransactionHead.CHICORY: "Purchase of chicory blend stock",
    TransactionHead.ROASTING: "Roasting process cost",
    TransactionHead.GRINDING: "Grinding process cost",
    TransactionHead.BLENDING: "Blending process cost",
    TransactionHead.PACKAGING: "Packaging materials and labor",
    TransactionHead.TRANSPORT: "Transport and freight charges",
    TransactionHead.PROMOTION: "Marketing and promotion spend",
    TransactionHead.COMMISSION: "Distributor commission payout",
    TransactionHead.AUDIT: "Annual audit fee",
    TransactionHead.LICENSES: "Regulatory license renewal",
    TransactionHead.OTHER_OPERATIONAL_EXPENSES: "Other operational expense",
}

REMARKS = ["Paid via UPI", "Bank transfer", "Cash payment", None, None]  # some None on purpose


def build_demo_transactions(n: int = 20):
    records = []
    today = date.today()
    for i in range(n):
        head = random.choice(list(TransactionHead))
        txn_type = random.choice(list(TransactionType))

        records.append(
            Transaction(
                TransactionDate=today - timedelta(days=random.randint(0, 15)),
                TransactionType=txn_type,
                TransactionHead=head,
                Amount=round(random.uniform(500, 25000), 2),
                Vendor=random.choice(VENDORS),
                Description=DESCRIPTIONS[head],
                Remarks=random.choice(REMARKS),
            )
        )
    return records


def main():
    db = SessionLocal()
    try:
        existing = db.query(Transaction).count()
        print(f"Existing rows in transaction table: {existing}")

        demo_records = build_demo_transactions(20)
        db.add_all(demo_records)
        db.commit()

        print(f"Inserted {len(demo_records)} demo transactions.")
        print(f"Total rows now: {db.query(Transaction).count()}")
    finally:
        db.close()


if __name__ == "__main__":
    main()