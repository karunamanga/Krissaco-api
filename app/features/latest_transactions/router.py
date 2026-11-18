from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.common.models.transaction import Transaction
from app.common.schemas.transaction import LatestTransactionsResponse
from app.core.database import get_db

router = APIRouter()


@router.get(
    "/transaction",
    response_model=LatestTransactionsResponse,
    response_model_exclude_none=True,
)
def get_latest_transactions(
    limit: int = Query(10, gt=0, le=100, description="Number of latest transactions to return"),
    db: Session = Depends(get_db),
):
    """Returns the latest N transactions, most recent first (N controlled by ?limit=)."""
    txns = (
        db.query(Transaction)
        .order_by(desc(Transaction.CreatedAt))
        .limit(limit)
        .all()
    )

    if not txns:
        return LatestTransactionsResponse(
            count=0,
            transactions=[],
        )

    return LatestTransactionsResponse(
        count=len(txns),
        transactions=txns,
    )