from decimal import Decimal
from typing import List

from pydantic import BaseModel

from app.common.schemas.transaction import TransactionOut


class StatementResponse(BaseModel):
    count: int
    total_revenue: Decimal
    total_expense: Decimal
    net: Decimal
    transactions: List[TransactionOut]