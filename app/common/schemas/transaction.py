import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    field_serializer,
)

from app.common.models.transaction import TransactionType, TransactionHead

DATE_FORMAT = "%d-%m-%Y"


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    TransactionID: uuid.UUID
    TransactionDate: date
    TransactionType: TransactionType
    TransactionHead: TransactionHead
    Amount: Decimal
    Vendor: str
    Description: str
    Remarks: Optional[str]
    CreatedAt: datetime

    @field_validator("TransactionDate", mode="before")
    @classmethod
    def parse_date(cls, value):
        """Accepts DD-MM-YYYY strings (e.g. from request input) as well as
        date objects (e.g. coming straight from the DB)."""
        if isinstance(value, str):
            try:
                return datetime.strptime(value, DATE_FORMAT).date()
            except ValueError:
                raise ValueError(f"TransactionDate must be in {DATE_FORMAT} format")
        return value

    @field_validator("TransactionDate")
    @classmethod
    def date_not_in_future(cls, value: date) -> date:
        """Applies to both Revenue and Expense transactions -- mirrors the
        DB-level ck_date_not_future constraint, but rejected early here with
        a clean, readable error instead of a raw IntegrityError."""
        if value > date.today():
            raise ValueError("TransactionDate cannot be a future date")
        return value

    @field_serializer("TransactionDate")
    def serialize_date(self, value: date, _info) -> str:
        return value.strftime(DATE_FORMAT)


class LatestTransactionsResponse(BaseModel):
    count: int
    message: Optional[str] = None
    transactions: List[TransactionOut]