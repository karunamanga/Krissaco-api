from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.common.models.transaction import Transaction, TransactionType
from app.common.schemas.transaction import DATE_FORMAT
from app.core.database import get_db
from app.core.exceptions import KrissacoException
from app.features.statement.schema import StatementResponse

router = APIRouter()


def _parse(value: str, field_name: str):
    try:
        return datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        raise KrissacoException(f"{field_name} must be in DD-MM-YYYY format")


@router.get(
    "/statement",
    response_model=StatementResponse,
)
def get_statement(
    start_date: str = Query(..., description="Start of range, DD-MM-YYYY"),
    end_date: str = Query(..., description="End of range, DD-MM-YYYY"),
    db: Session = Depends(get_db),
):
    start = _parse(start_date, "start_date")
    end = _parse(end_date, "end_date")

    if end <= start:
        raise KrissacoException("end_date must be later than start_date")

    txns = (
        db.query(Transaction)
        .filter(Transaction.TransactionDate >= start)
        .filter(Transaction.TransactionDate <= end)
        .order_by(desc(Transaction.TransactionDate), desc(Transaction.CreatedAt))
        .all()
    )

    total_revenue = sum(
        (t.Amount for t in txns if t.TransactionType == TransactionType.REVENUE), Decimal("0.00")
    )
    total_expense = sum(
        (t.Amount for t in txns if t.TransactionType == TransactionType.EXPENSE), Decimal("0.00")
    )

    return StatementResponse(
        count=len(txns),
        total_revenue=total_revenue,
        total_expense=total_expense,
        net=total_revenue - total_expense,
        transactions=txns,
    )