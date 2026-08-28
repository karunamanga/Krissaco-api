-- Krissaco Transaction API -- Database Setup
-- To be run by a DBA. The application does NOT create or manage this
-- schema at runtime -- table creation is intentionally outside the
-- scope of the API project.

-- Run once, connected to the target database (e.g. "Krissaco"):

-- Required for gen_random_uuid() used as the primary key default
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE "transactionTypeEnum" AS ENUM ('Revenue', 'Expense');

CREATE TYPE "transactionHeadEnum" AS ENUM (
    'Coffee Beans',
    'Chicory',
    'Roasting',
    'Grinding',
    'Blending',
    'Packaging',
    'Transport',
    'Promotion',
    'Commission',
    'Audit',
    'Licenses',
    'Other Operational Expenses'
);

CREATE TABLE "transaction" (
    "TransactionID"   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "TransactionDate" DATE NOT NULL,
    "TransactionType" "transactionTypeEnum" NOT NULL,
    "TransactionHead" "transactionHeadEnum" NOT NULL,
    "Amount"          NUMERIC(12, 2) NOT NULL,
    "Vendor"          VARCHAR(150) NOT NULL,
    "Description"     VARCHAR(255) NOT NULL,
    "Remarks"         VARCHAR(255),
    "CreatedAt"       TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_amount_positive CHECK ("Amount" > 0),
    CONSTRAINT ck_date_not_future CHECK ("TransactionDate" <= CURRENT_DATE),
    CONSTRAINT ck_vendor_min_length CHECK (char_length("Vendor") >= 2),
    CONSTRAINT ck_description_min_length CHECK (char_length("Description") >= 3),
    CONSTRAINT ck_description_max_length CHECK (char_length("Description") <= 255)
);

-- Recommended indexes for the query patterns used by the API
CREATE INDEX idx_transaction_created_at ON "transaction" ("CreatedAt" DESC);
CREATE INDEX idx_transaction_date ON "transaction" ("TransactionDate");