import pydantic

from typing import Optional
from decimal import Decimal
from bson import ObjectId
from enum import Enum
from bson.decimal128 import Decimal128
from pydantic import Field
from fastapi import Body

from core_service.base import Base
from auth.schema import User as auth_user


class TransactionTypeEnum(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionStatusEnum(str, Enum):
    PENDING = "pending"
    SUCCESS = "outgoing"
    FAILED = "failed"
    NOT_FOUND = "not_found"


class TransactionBase(Base):
    transaction_type: TransactionTypeEnum
    status: TransactionStatusEnum = Body(TransactionStatusEnum.PENDING.value)
    amount: Decimal = Body(..., embed=True, media_type="application/json")
    currency: str = Body(
        "$",
        max_length=1,
    )
    display_amount: str = Body(
        None, description="Transaction amount in a string formatted form.", embed=True
    )

    @pydantic.validator("display_amount", pre=True, always=True)
    def default_ts_display_amount(cls, v, *, values, **kwargs):
        try:
            str(values["amount"])
        except:
            raise ValueError("Value is not a valid decimal")
        return v or f"{values.get('currency', '$')}{str(values['amount'])}"

    # Previous Decimal validation implementation before I went with the convertor class approach
    # @pydantic.validator("amount", pre=True, always=True)
    # def default_ts_amount(cls, v, *, values, **kwargs):
    #     if type(v) != str:
    #         raise RequestValidationError(
    #             body="Invalid amount provided, the amount field strictly requires a string type."
    #         )
    #     return v or Decimal128(v)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "64f418856b25680d5292fa50",
                "transaction_type": "credit",
                "status": "pending",
                "amount": "2500.89",
                "currency": "$",
                "display_amount": "$2500.89",
                "created": "2023-09-02T16:58:44.329000",
                "last_modified": "2023-09-02T16:58:59.230000",
                "user_id": "64f418aeff9dc97eeef2ea08",
            },
            "title": "Transaction Base Model",
            "description": "A __model__ representing a __Transaction Record__ insatance.",
        }


class CreateTransaction(TransactionBase):
    pass


class User(auth_user):
    id: ObjectId = Body(..., alias="_id")


class Transaction(TransactionBase):
    amount: Decimal128
    user: User
    id: ObjectId = Body(..., alias="_id")

    class Config:
        schema_extra = {
            "example": {
                "_id": "7779836983",
                "transaction_type": "credit",
                "status": "pending",
                "amount": "2500.89",
                "currency": "$",
                "display_amount": "$2500.89",
                "created": "2023-09-02T16:58:44.329000",
                "last_modified": "2023-09-02T16:58:59.230000",
                "user": {
                    "_id": "7779836983AMW",
                    "firstname": "Moses",
                    "lastname": "Alhassan",
                    "othernames": "Wuniche",
                    "email": "alhassanmoses.amw@gmail.com",
                    "username": "moseswuniche",
                    "fullname": "Moses Wuniche Alhassan",
                    "created": "2023-09-03T15:54:21.367000",
                    "last_modified": "2023-09-03T15:54:21.367000",
                },
                "title": "Transaction Model",
                "description": "A __model__ representing a __Transaction Record__ insatance.",
            }
        }


class TransactionGetResponse(TransactionBase):
    amount: str
    transaction_type: str
    status: str

    @pydantic.validator("amount", pre=True, always=True)
    def default_ts_amount(cls, v, *, values, **kwargs):
        return v or Decimal(values["amount"].to_decimal())

    class Config:
        schema_extra = {
            "example": {
                "_id": "64f418b6ff9dc97eeef2ea09",
                "transaction_type": "credit",
                "status": "pending",
                "amount": "2500.89",
                "currency": "$",
                "display_amount": "$2500.89",
                "created": "2023-09-02T16:58:44.329000",
                "last_modified": "2023-09-02T16:58:59.230000",
                "user_id": "64f418beff9dc97eeef2ea0b",
            },
            "title": "Transaction Response Model",
            "description": "A __model__ representing a __Transaction Record__ Response schema.",
        }


class TransactionUpdate(Base):
    """
    Users should not be able to update everything about
    a Transaction record, given it contains sensitive data
    """

    status: TransactionStatusEnum
    transaction_type: TransactionTypeEnum
    display_amount: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "transaction_type": "credit",
                "status": "pending",
                "display_amount": "$89.47",
            },
            "title": "Transaction Update Request Model",
            "description": "A __model__ representing a __Transaction Record__ update request schema.",
        }
