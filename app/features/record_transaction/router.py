from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.common.models.transaction import Transaction
from app.common.schemas.transaction import TransactionCreate, TransactionOut

router = APIRouter()


@router.post(
    "/transaction",
    response_model=TransactionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Record a new transaction",
)
def create_transaction(
    request: TransactionCreate,
    db: Session = Depends(get_db),
):
    transaction = Transaction(
        TransactionDate=request.TransactionDate,
        TransactionType=request.TransactionType,
        TransactionHead=request.TransactionHead,
        Vendor=request.Vendor,
        Amount=request.Amount,
        Description=request.Description,
        Remarks=request.Remarks,
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction