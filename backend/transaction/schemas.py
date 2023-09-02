import pydantic

from datetime import datetime
from decimal import Decimal
from bson import ObjectId
from enum import Enum
from bson.decimal128 import Decimal128
from pydantic import Field

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
    status: TransactionStatusEnum = Field(TransactionStatusEnum.PENDING.value)
    amount: Decimal
    current: str = Field(
        "$",
        max_length=1,
    )
    amount_in_string: str = Field(
        None, description="Transaction amount in a string formatted form."
    )

    @pydantic.validator("amount_in_string", pre=True, always=True)
    def default_ts_amount_in_string(cls, v, *, values, **kwargs):
        return v or f"{values['current']}{str(values['amount'])}"

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
                "_id": "7779836983",
                "transaction_type": "credit",
                "status": "pending",
                "amount": "2000",
                "current": "$",
                "amount_in_string": "$2000",
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
                    "created": "2023-09-02T16:58:24.129000",
                    "last_modified": "2023-09-02T16:58:24.130000",
                },
            },
            "title": "Transaction Model",
            "description": "A __model__ representing a __Transaction Record__ insatance.",
        }


class CreateTransaction(TransactionBase):
    pass


class User(auth_user):
    id: ObjectId = Field(..., alias="_id")


class Transaction(TransactionBase):
    amount: Decimal128
    user: User
    id: ObjectId = Field(..., alias="_id")


class TransactionResponse(TransactionBase):
    amount: str
    user: auth_user
    id: str = Field(..., alias="_id")
