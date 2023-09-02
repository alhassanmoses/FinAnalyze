import os
import logging

from dependencies.settings import settings

from core_service.routes import router

from fastapi import (
    APIRouter,
    Body,
    Depends,
    FastAPI,
    Query,
    Path,
    Header,
    status,
    Form,
    HTTPException,
    Request,
    BackgroundTasks,
)
from fastapi.middleware.cors import CORSMiddleware
from dependencies.sharedutils.db import db


logger = logging.getLogger(__name__)

description = """
FinAnalyze API helps user manage and gain insights on their day to day transactions.

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
        app.db = db.get_client()[settings.MONGODB_DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    if db.client:
        db.client.close()


@app.get("/")
async def root():
    return "Home page under construction."
