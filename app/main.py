from fastapi import FastAPI

<<<<<<< HEAD
from . import routes
from .database import engine, Base

# Creates the transaction table (and enum types) if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Latest Transactions Microservice")

app.include_router(routes.router)
=======
from app.features.latest_transactions import router as latest_transactions_router
from app.features.record_transaction import router as record_transaction_router
from app.features.statement import router as statement_router

app = FastAPI(title="Krissaco Transaction API")

app.include_router(latest_transactions_router.router)
app.include_router(record_transaction_router.router)
app.include_router(statement_router.router)
>>>>>>> origin/main
