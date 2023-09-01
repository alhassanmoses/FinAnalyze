import os

from fastapi import (
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

from pydantic import BaseModel

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
    docs_url="/api-docs",
    redoc_url="/redoc/api-docs",
)

origins = os.environ.get("ORIGIN", "").split()

app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "Home page under construction."
