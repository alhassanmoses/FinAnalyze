import datetime
import pydantic

from typing import Optional
from pydantic import EmailStr, Field
from bson import ObjectId
from core_service.base import Base
from fastapi import Body


class UserBase(Base):
    firstname: str = Body(..., min_length=2, max_length=80)
    lastname: Optional[str] = Body(..., max_length=80)
    othernames: Optional[str] = Body(..., max_length=80)
    email: Optional[EmailStr]
    username: str = Body(..., max_length=80)
    fullname: Optional[str] = Body(None, max_length=200)

    @pydantic.validator("fullname", pre=True, always=True)
    def default_ts_fullname(cls, v, *, values, **kwargs):
        return v or f"{values['firstname']} {values['othernames']} {values['lastname']}"


class NewUser(UserBase):
    password: str = Body(..., min_length=6, max_length=64)


class User(UserBase):
    id: ObjectId = Field(..., alias="_id")
