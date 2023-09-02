import pydantic

from typing import Optional
from pydantic import EmailStr, Field, SecretStr
from core_service.base import Base
from fastapi import Body


class UserBase(Base):
    firstname: str = Body(..., min_length=2, max_length=80)
    lastname: Optional[str] = Body(None, max_length=80)
    othernames: Optional[str] = Body(None, max_length=80)
    email: Optional[EmailStr]
    username: str = Body(..., max_length=80)
    fullname: Optional[str] = Body(None, max_length=200)

    @pydantic.validator("fullname", pre=True, always=True)
    def default_ts_fullname(cls, v, *, values, **kwargs):
        return v or f"{values['firstname']} {values['othernames']} {values['lastname']}"


class NewUser(UserBase):
    password: SecretStr = Body(..., min_length=6, max_length=64, exclude=True)


class User(UserBase):
    id: str = Field(..., alias="_id")


class TokenReturn(UserBase):
    id: str = Field(..., alias="_id")
    access_token: str
    token_type: str
