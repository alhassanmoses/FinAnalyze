from fastapi import APIRouter

user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[Depends()], # TODO: implement a token checker for the headers
    responses={404: {"description": "Not found"}},
)
