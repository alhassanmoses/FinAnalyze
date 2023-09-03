from dependencies.settings import settings
from dependencies.sharedutils.api_messages import gettext
from dependencies.sharedutils.db import get_base_query

from typing import Dict
from jose import jwt
from bson import ObjectId
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from motor.core import AgnosticDatabase
from auth.schema import NewUser


pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_access_token():
    pass


def verify_access_token(token: str):
    payload: Dict[str, any] = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
    )
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=gettext("COULD_NOT_VALIDATE"),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    try:
        user_id = verify_access_token(token)
        request.app.current_user_id = user_id

        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=gettext("TOKEN_EXPIRED")
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=gettext("COULD_NOT_VALIDATE"),
        )


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM
    )

    return encoded_jwt


async def authenticate_user(username, password, db: AgnosticDatabase):
    user = await db.find_one({"username": username})

    if not user or not pwd_context.verify(password, user["password"]):
        return False

    del user["password"]
    return user


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_user(user_data, db: AgnosticDatabase):
    # Hash the password before storing it, per security requirements.
    user_data.password: str = get_password_hash(user_data.password)

    # Check if the username already exists
    existing_user = await db.users.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail=gettext("USERNAME_EXIST"))

    # Store the user in the database

    new_user = await db.users.insert_one(
        {
            **user_data.dict(),
            "password": user_data.password,
            **get_base_query(is_insert=True),
        }
    )

    user = await NewUser.get_by_id(str(new_user.inserted_id), "users", db)
    del user["password"]
    return user
