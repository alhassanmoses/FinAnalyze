import json
import bson.json_util as json_util
from auth.schema import NewUser, User
from dependencies.sharedutils.db import db

from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from dependencies.settings import settings
from auth.database import get_by_id, create_user, authenticate_user
from dependencies.sharedutils.jsonencoder import JSONEncoder

user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[Depends()], # TODO: implement a token checker for the headers
    responses={404: {"description": "Resource Not found"}},
)


Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.post(
    "/sign_up",
    summary="Create a user account.",
)
async def sign_up(request: Request, new_user: NewUser):
    users = request.app.db.users

    user = await create_user(new_user, users)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json.loads(JSONEncoder().encode(user)),
    )


# content=json.loads(json_util.dumps(user))


@user_router.post("/token", summary="Create a User token.")
async def sign_up(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    users = request.app.db.users

    auth_user = await authenticate_user(form_data.username, form_data.password, users)

    if not auth_user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Incorrect username or password provided.",
        )

    return json.loads(JSONEncoder().encode(auth_user))


# @user_router.post("/token", summary="Create a User token.")
# async def sign_up(token: str = Depends(Oauth2_scheme)):
#     pass
