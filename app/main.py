from fastapi import FastAPI

from app.features.latest_transactions import router as latest_transactions_router
from app.features.record_transaction import router as record_transaction_router
from app.features.statement import router as statement_router
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Krissaco Transaction API")

app.include_router(latest_transactions_router.router)
app.include_router(record_transaction_router.router)
app.include_router(statement_router.router)