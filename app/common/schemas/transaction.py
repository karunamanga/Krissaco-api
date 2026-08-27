import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    field_serializer,
)

from app.common.models.transaction import TransactionType, TransactionHead

DATE_FORMAT = "%d-%m-%Y"


class TransactionDateMixin:
    """Shared DD-MM-YYYY parsing/serialization for any schema with a TransactionDate field."""

    @field_validator("TransactionDate", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, DATE_FORMAT).date()
            except ValueError:
                raise ValueError(f"TransactionDate must be in {DATE_FORMAT} format")
        return value

    @field_validator("TransactionDate")
    @classmethod
    def date_not_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("TransactionDate cannot be a future date")
        return value

    @field_serializer("TransactionDate")
    def serialize_date(self, value: date, _info) -> str:
        return value.strftime(DATE_FORMAT)


class TransactionCreate(TransactionDateMixin, BaseModel):
    TransactionDate: date
    TransactionType: TransactionType
    TransactionHead: TransactionHead
    Amount: Decimal = Field(..., gt=0)
    Vendor: str = Field(..., min_length=2, max_length=150)
    Description: str = Field(..., min_length=3, max_length=255)
    Remarks: Optional[str] = Field(None, max_length=255)


class TransactionOut(TransactionDateMixin, BaseModel):
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


class LatestTransactionsResponse(BaseModel):
    count: int
    message: Optional[str] = None
    transactions: List[TransactionOut]