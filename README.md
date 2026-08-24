# Krissaco — Latest Transactions Microservice

A backend microservice built with **FastAPI** and **PostgreSQL** that exposes the latest recorded business transactions in reverse chronological order. UI is out of scope for this phase — this covers database schema and REST API only.

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic

## Database

- **Database name:** `Krissaco`
- **Table:** `transaction`

Column            | Type                      | Notes
------------------|---------------------------|--------------------------------------------------------------------------------------------------------
TranscationID     | UUID                      | Primary key, system-generated
TransactionDate   | Date                      | Cannot be a future date
TransactionType   | Enum                      | Revenue, Expense
TransactionHead   | Enum                      | Coffee Beans, Chicory, Roasting, Grinding, Blending, Packaging, Transport, Promotion, Commission, Audit, Licenses, Other Operational Expenses
Amount            | Numeric(12,2)             | Must be greater than 0
Vendor            | Varchar(150)              | Mandatory
Description       | Varchar(255)              | Mandatory, max 255 characters
Remarks           | Varchar(255)              | Optional
CreatedAt         | Timestamp with time zone  | System-generated

## API

### `GET /transaction`

Returns the latest transactions, most recent first.

**Query Parameters**

| Param | Type | Default | Notes |
|---|---|---|---|
| `limit` | int | 10 | Number of records to return (1–100) |

**Behavior**

- Returns up to `limit` transactions, ordered by `CreatedAt` descending.
- If fewer records exist than `limit`, returns whatever is available along with the actual `count` — not treated as an error.
- If no transactions exist at all, `count` is `0` and a `message` field is included explaining there's no data. The `message` field is otherwise omitted from the response entirely.

**Example — records found**
```json
{
  "count": 5,
  "transactions": [
    {
      "TranscationID": "3b03e65c-0ba3-4e9d-814f-fadf4044bab0",
      "TransactionDate": "2026-08-23",
      "TransactionType": "Revenue",
      "TransactionHead": "Coffee Beans",
      "Amount": "22661.25",
      "Vendor": "Delta Foods",
      "Description": "Purchase of raw coffee beans",
      "Remarks": null,
      "CreatedAt": "2026-08-24T14:46:33.083463+05:30"
    }
  ]
}
```

**Example — no records**
```json
{
  "count": 0,
  "message": "No transactions have been recorded yet.",
  "transactions": []
}
```

## Setup

### 1. Create the database
In `psql`:
```sql
CREATE DATABASE "Krissaco";
```

### 2. Configure environment
```bash
cp .env.example .env
```
Edit `.env` with your actual PostgreSQL password:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/Krissaco
```

### 3. Set up the virtual environment
```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash on Windows
pip install -r requirements.txt
```

### 4. Run the API
```bash
uvicorn app.main:app --reload
```
The table and enum types are created automatically on first run.

### 5. (Optional) Seed demo data
Inserts 20 randomized demo transactions:
```bash
python seed.py
```

### 6. Test
```
GET http://127.0.0.1:8000/transaction
GET http://127.0.0.1:8000/transaction?limit=5
```
Interactive docs available at `http://127.0.0.1:8000/docs`.

## Project Structure
```
transaction_service/
├── app/
│   ├── __init__.py
│   ├── database.py     # DB connection & session setup
│   ├── models.py        # SQLAlchemy model, enums, constraints
│   ├── schemas.py        # Pydantic request/response schemas
│   └── main.py            # FastAPI app & route
├── seed.py                 # Demo data seeding script
├── requirements.txt
├── .env.example
└── README.md
```

## Status

- ✅ Database schema
- ✅ `GET /transaction` API
- ⬜ UI (planned for a later phase)
