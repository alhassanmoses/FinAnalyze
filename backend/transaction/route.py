from fastapi import APIRouter

transaction_router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[Depends()], # TODO: implement a token checker for the headers
    responses={404: {"description": "Resource Not found"}},
)
