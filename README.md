# Krissaco Transaction API

A FastAPI + PostgreSQL microservice for recording business transactions and retrieving the latest transactions and date-range statements.

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Validation:** Pydantic

## Scope

This project provides the **REST API only**. Database and table creation/management is **out of scope** for the application and is owned by a DBA. The API only performs data manipulation (read/write) against a schema that already exists.

## Project Structure

```
app/
├── main.py                          # app entrypoint, wires everything together
├── core/
│   ├── config.py                     # settings/env management
│   ├── database.py                   # DB connection, Base, get_db
│   └── exceptions.py                 # custom exception (KrissacoException)
├── common/
│   ├── models/transaction.py          # the Transaction table definition (ORM mapping only -- does not create it)
│   └── schemas/transaction.py         # shared Pydantic request/response schemas
└── features/
    ├── record_transaction/             # POST /transaction
    ├── latest_transactions/            # GET /transaction
    └── statement/                      # GET /statement
tests/                                # mirrors features/ structure
krissaco.sql                          # DDL script -- run manually by a DBA, not by the app
requirements.txt
.env.example
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/transaction` | Latest N transactions, most recent first (`?limit=`) |
| `POST` | `/transaction` | Record a new transaction. Returns the created record, including the generated `TransactionID`, with `201 Created`. |
| `GET` | `/statement` | Transactions + revenue/expense totals in a date range (`?start_date=&end_date=`) |

**Dates use `DD-MM-YYYY` format** throughout the API (not ISO).

Interactive docs available at `http://127.0.0.1:8000/docs` once running.

### Validation rules

#### `POST /transaction`

| Field | Rule |
|---|---|
| `TransactionDate` | Required. Format `DD-MM-YYYY`. Cannot be a future date. |
| `TransactionType` | Required. Must be exactly `Revenue` or `Expense`. |
| `TransactionHead` | Required. Must be one of: `Coffee Beans`, `Chicory`, `Roasting`, `Grinding`, `Blending`, `Packaging`, `Transport`, `Promotion`, `Commission`, `Audit`, `Licenses`, `Other Operational Expenses`. |
| `Amount` | Required. Must be greater than `0`. |
| `Vendor` | Required. 2–150 characters. |
| `Description` | Required. 3–255 characters. |
| `Remarks` | Optional. Up to 255 characters. |

Any violation returns `422 Unprocessable Entity` with details on which field failed. On success, returns `201 Created` with the full saved record, including the generated `TransactionID`.

#### `GET /transaction`

| Param | Rule |
|---|---|
| `limit` | Optional query param. Integer, `1`–`100`. Defaults to `10` if omitted. |

Returns `200 OK` with `count` and `transactions`. If fewer records exist than `limit`, returns whatever is available with the actual `count` — not treated as an error. If no transactions exist at all, returns `count: 0` and an empty `transactions` array.

#### `GET /statement`

| Param | Rule |
|---|---|
| `start_date` | Required query param. Format `DD-MM-YYYY`. |
| `end_date` | Required query param. Format `DD-MM-YYYY`. Must be strictly later than `start_date` (a single-day range where `start_date == end_date` is currently rejected). |

Invalid format or an invalid range returns `400 Bad Request` with a message describing the problem. On success, returns `200 OK` with `count`, `total_revenue`, `total_expense`, `net`, and the list of matching `transactions`.

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder-name>
```

### 2. Create and activate a virtual environment

**PowerShell:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

If you hit an execution policy error, run this once first, then retry activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Git Bash:**
```bash
python -m venv venv
source venv/Scripts/activate
```

You should see `(venv)` at the start of your terminal prompt once active.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the database and table

The application does **not** create these automatically. Use `krissaco.sql` with either tool below.

#### Option A — SQL Shell (psql)

Open psql and connect (press Enter to accept each default until prompted for your password):

```
Server [localhost]: (Enter)
Database [postgres]: (Enter)
Port [5432]: (Enter)
Username [postgres]: (Enter)
Password: <your postgres password>
```

Create the database (skip if it already exists):

```sql
CREATE DATABASE "Krissaco";
```

Switch into it:

```sql
\c "Krissaco"
```

Run the DDL script:

```sql
\i 'path/to/krissaco.sql'
```
(Use forward slashes in the path, even on Windows.)

Confirm it worked:

```sql
\dt
\d "transaction"
```

Exit:

```sql
\q
```

#### Option B — pgAdmin

1. Open pgAdmin and connect to your local server
2. Right-click **Databases** → **Create** → **Database...** → name it `Krissaco` → **Save** (skip if it already exists)
3. Right-click the **Krissaco** database → **Query Tool**
4. In the Query Tool toolbar, click **Open File** and select `krissaco.sql`
5. Click **Execute/Run** (▶ or F5)
6. Confirm: expand **Krissaco → Schemas → public → Tables** — `transaction` should be listed

### 5. Configure environment variables

Copy the example file and rename it:

```bash
cp .env.example .env
```

(On Windows PowerShell: `copy .env.example .env`)

Open `.env` and set your real PostgreSQL password:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/Krissaco
```

`.env` is git-ignored — never commit real credentials.

### 6. Run the API

```bash
uvicorn app.main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

The app connects to the existing table — it does not create or alter it.

### 7. Test it

Open in your browser:
```
http://127.0.0.1:8000/docs
```

Or via curl:
```bash
curl http://127.0.0.1:8000/transaction
```

Expected response with no data yet:
```json
{"count": 0, "transactions": []}
```

Example `POST /transaction` request:
```json
{
  "TransactionDate": "25-08-2026",
  "TransactionType": "Expense",
  "TransactionHead": "Roasting",
  "Amount": 1200.50,
  "Vendor": "Acme Traders",
  "Description": "Roasting batch payment",
  "Remarks": "Paid via UPI"
}
```

Example `201 Created` response (note `TransactionID` is included, per REST convention):
```json
{
  "TransactionID": "59fe9bfd-2095-4072-b94e-114fc1eb85bf",
  "TransactionDate": "25-08-2026",
  "TransactionType": "Expense",
  "TransactionHead": "Roasting",
  "Amount": "1200.50",
  "Vendor": "Acme Traders",
  "Description": "Roasting batch payment",
  "Remarks": "Paid via UPI",
  "CreatedAt": "2026-08-27T12:15:31.656387+05:30"
}
```

### 8. (Optional) Load sample test data

`post_test_data.py` sends 30 randomized transactions through the running API (via `POST /transaction`), useful for populating test data without bypassing the API layer:

```bash
python post_test_data.py
```

---

## Inspecting the database

#### Via psql

```sql
\c "Krissaco"
\dt
\d "transaction"
SELECT * FROM "transaction" ORDER BY "CreatedAt" DESC;
```

#### Via pgAdmin

1. Expand **Servers → PostgreSQL → Databases → Krissaco → Schemas → public → Tables**
2. Right-click **transaction** → **View/Edit Data** → **All Rows**

## Schema changes

Since the API does not manage the schema, any change to `app/common/models/transaction.py` (new column, changed constraint, new enum value) must be paired with a corresponding update to `krissaco.sql`, applied manually by a DBA (via `ALTER TABLE`, `ALTER TYPE`, etc.). The two are not automatically kept in sync — update both together.

---

## Contributing (multiple teams)

Each feature lives in its own folder under `app/features/<feature_name>/` (`router.py`, `service.py`, `repository.py`, `schema.py`). When adding or changing a feature:

1. Work inside your own `features/<feature_name>/` folder only
2. If a change is needed in `app/common/` (shared model or schema) or the database schema, flag it with the team first — it affects every feature
3. Register your router in `app/main.py`
4. Do not change existing API paths or methods without team agreement — other services depend on this contract
5. Open a Pull Request rather than pushing directly to `main`

## Status

- ✅ Record transaction (`POST /transaction`)
- ✅ Latest transactions (`GET /transaction`)
- ✅ Statement by date range (`GET /statement`)
