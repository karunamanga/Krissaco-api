import enum
import uuid

from sqlalchemy import (
    Column,
    String,
    Numeric,
    Date,
    DateTime,
    Enum as SAEnum,
    CheckConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class TransactionType(str, enum.Enum):
    REVENUE = "Revenue"
    EXPENSE = "Expense"


class TransactionHead(str, enum.Enum):
    COFFEE_BEANS = "Coffee Beans"
    CHICORY = "Chicory"
    ROASTING = "Roasting"
    GRINDING = "Grinding"
    BLENDING = "Blending"
    PACKAGING = "Packaging"
    TRANSPORT = "Transport"
    PROMOTION = "Promotion"
    COMMISSION = "Commission"
    AUDIT = "Audit"
    LICENSES = "Licenses"
    OTHER_OPERATIONAL_EXPENSES = "Other Operational Expenses"


class Transaction(Base):
    __tablename__ = "transaction"

    # system generated
    TransactionID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # user input
    TransactionDate = Column(Date, nullable=False)
    TransactionType = Column(
        SAEnum(TransactionType, name="transactionTypeEnum"), nullable=False
    )
    TransactionHead = Column(
        SAEnum(TransactionHead, name="transactionHeadEnum"), nullable=False
    )
    Amount = Column(Numeric(12, 2), nullable=False)
    Vendor = Column(String(150), nullable=False)
    Description = Column(String(255), nullable=False)
    Remarks = Column(String(255), nullable=True)  # optional

    # system generated
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint('"Amount" > 0', name="ck_amount_positive"),
        CheckConstraint('"TransactionDate" <= CURRENT_DATE', name="ck_date_not_future"),
        CheckConstraint('char_length("Vendor") >= 2', name="ck_vendor_min_length"),
        CheckConstraint('char_length("Description") >= 3', name="ck_description_min_length"),
        CheckConstraint('char_length("Description") <= 255', name="ck_description_max_length"),
    )
