from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from . import models, schemas
from .database import engine, get_db, Base

# Creates the transaction table (and enum types) if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Latest Transactions Microservice")


@app.get(
    "/transaction",
    response_model=schemas.LatestTransactionsResponse,
    response_model_exclude_none=True,
)
def get_latest_transactions(
    limit: int = Query(10, gt=0, le=100, description="Number of latest transactions to return"),
    db: Session = Depends(get_db),
):
    """Returns the latest N transactions, most recent first (N controlled by ?limit=).
    If fewer records exist than the requested limit, returns whatever is available
    with the matching count -- this is not treated as an error.
    A 'message' field is only included in the response when count == 0."""
    txns = (
        db.query(models.Transaction)
        .order_by(desc(models.Transaction.CreatedAt))
        .limit(limit)
        .all()
    )

    if not txns:
        return schemas.LatestTransactionsResponse(
            count=0,
            message="No transactions have been recorded yet.",
            transactions=[],
        )

    return schemas.LatestTransactionsResponse(
        count=len(txns),
        transactions=txns,
    )