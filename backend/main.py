import os
import logging

from dependencies.settings import settings
from dependencies.sharedutils.db import db
from core_service.routes import router

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from motor.core import AgnosticDatabase


logger = logging.getLogger(__name__)

description = """
FinAnalyze API helps user manage and gain insights on their day to day transactions.

## Users
## Transactions

"""
app = FastAPI(
    title="FinAnalyze API",
    description=description,
    version="0.0.1",
    terms_of_service="https://github.com/alhassanmoses/FinAnalyze/blob/main/LICENSE",
    contact=dict(
        name="Moses Wuniche Alhassan",
        url="https://www.linkedin.com/in/moses-wuniche-alhassan-4ab87412b/",
        email="alhassanmoses.amw@gmail.com",
    ),
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/external-api/v1/docs",
)


app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(" "),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    if "MONGODB_URL" in os.environ:
        await db.connect(settings.MONGODB_URL)
        app.db: AgnosticDatabase = db.get_client()[settings.MONGODB_DB_NAME]
        app.current_user_id = None

        # app.db.users.delete_many({})
        # app.db.transactions.delete_many({})
        # app.db.client.close()


@app.on_event("shutdown")
async def shutdown_db_client():
    if db.client:
        db.client.close()


@app.get("/")
async def root():
    return "Home page under construction."
