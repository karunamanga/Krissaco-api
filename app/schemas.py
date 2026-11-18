import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from .models import TransactionType, TransactionHead


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


class LatestTransactionsResponse(BaseModel):
    count: int
    message: Optional[str] = None
    transactions: List[TransactionOut]