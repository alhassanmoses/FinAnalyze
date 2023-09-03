import pydantic

from typing import Optional
from pydantic import EmailStr
from fastapi import Body
from decimal import Decimal
from bson import ObjectId, Decimal128

from core_service.base import Base


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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Decimal128: Decimal}
        schema_extra = {
            "example": {
                "firstname": "Moses",
                "lastname": "Alhassan",
                "othernames": "Wuniche",
                "email": "alhassanmoses.amw@gmail.com",
                "username": "moseswuniche",
                "fullname": "Moses Wuniche Alhassan",
                "created": "2023-09-03T15:54:21.367000",
                "last_modified": "2023-09-03T15:54:21.367000",
            },
            "title": "UserMode",
            "description": "A __model__ representing a user DB __instance__.",
        }


class NewUser(UserBase):
    password: str = Body(..., min_length=6, max_length=64, exclude=True)


class User(UserBase):
    id: str = Body(..., alias="_id")


class TokenReturn(UserBase):
    id: str = Body(..., alias="_id")
    access_token: str
    token_type: str
