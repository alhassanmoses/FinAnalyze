import logging
from typing import Union
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from auth.data_util import (
    create_user,
    authenticate_user,
    create_access_token,
)
from auth.schema import NewUser, User
from dependencies.sharedutils.jsonencoder import jsonHelper
from dependencies.sharedutils.api_messages import gettext
from motor.motor_asyncio import AsyncIOMotorClient
from dependencies.sharedutils.db import get_database

user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[Depends()], # TODO: implement a token checker for the headers
    responses={status.HTTP_404_NOT_FOUND: {"description": "Resource Not found"}},
)


@user_router.post(
    "/sign_up",
    response_model=User,
    summary="Create a user account.",
)
async def sign_up(new_user: NewUser, db: AsyncIOMotorClient = Depends(get_database)):
    user = await create_user(new_user, db)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonHelper(user))


@user_router.post("/login", summary="Generate a User token.")
async def get_token(
    db: AsyncIOMotorClient = Depends(get_database),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Returns a signed token along with the user's data

    Args:
        request (Request): The request Object injected as a dependency.
        form_data (OAuth2PasswordRequestForm, optional): Username and Password. Defaults to Depends().

    Returns:
        TokenReturn: A json containing the signed token along with the user's details
    """
    # users = request.app.db.users
    users = db.users

    auth_user: Union[bool, User] = await authenticate_user(
        form_data.username, form_data.password, users
    )

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=gettext("INVALID_CREDENTIALS"),
        )

    user_data = jsonHelper(auth_user)

    access_token = create_access_token(
        data={"sub": user_data["_id"]}, expires_delta=timedelta(minutes=60)
    )

    user_data.update({"access_token": access_token, "token_type": "bearer"})

    return user_data  # JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=user_data)
