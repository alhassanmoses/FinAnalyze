from auth.schema import NewUser

from fastapi import APIRouter
from passlib.context import CryptContext

user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[Depends()], # TODO: implement a token checker for the headers
    responses={404: {"description": "Resource Not found"}},
)

@user_router.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@user_router.get("/sign_up", summary="Create a user account.")
def sign_up(new_user: NewUser):
    new_user.password = get_password_hash(new_user.password)
    # user = put_user_in_db(new_user, db)
    return {"name": "You shall not pass"}
