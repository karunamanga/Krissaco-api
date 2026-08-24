from fastapi import FastAPI

from . import routes
from .database import engine, Base

# Creates the transaction table (and enum types) if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Latest Transactions Microservice")

app.include_router(routes.router)