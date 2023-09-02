from fastapi import APIRouter

transaction_router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
    # dependencies=[Depends()], # TODO: implement a token checker for the headers
    responses={404: {"description": "Not found"}},
)
