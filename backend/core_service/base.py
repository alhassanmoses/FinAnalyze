import pydantic
import logging

from bson import ObjectId
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

from motor.core import AgnosticDatabase
from fastapi.encoders import jsonable_encoder
from fastapi import Body, status, HTTPException

from core_service.exceptions import InvalidId as invID
from bson.errors import InvalidId
from dependencies.sharedutils.api_messages import gettext


class ObjectIdField(ObjectId):
    __origin__ = pydantic.typing.Literal
    __args__ = (str,)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(v)
        except InvalidId:
            raise ValueError(gettext("INVALID_OBJECT_ID"))

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Base(BaseModel):
    last_modified: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of last modification"
    )
    created: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of last modification"
    )

    deleted: Optional[datetime] = None

    @validator("created", pre=True, always=True)
    def set_created(cls, v):
        return datetime.utcnow()

    @validator("deleted", pre=True, always=True)
    def set_deleted(cls, v):
        return None

    @validator("last_modified", pre=True, always=True)
    def set_last_modified(cls, v):
        return datetime.utcnow()

    @staticmethod
    async def get_by_id(id: any, collection: str, db: AgnosticDatabase):
        try:
            entity = await db[collection].find_one({"_id": ObjectId(str(id))})
            if entity is not None:
                return entity
            return None
        except InvalidId as e:
            logging.error(f"Failed to retrieve {collection} entity with id: {id}.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=gettext("INVALID_ID_PROVIDED").format(id, collection),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=gettext("FAILED_TO_RETRIEVE_RECORD"),
            )

    class Config:
        allow_population_by_field_name = True

    def to_dict(self) -> any:
        return jsonable_encoder(self, exclude=["created", "last_modified", "deleted"])

    def dict(self, *args, **kwargs):
        # Exclude created and last_modified fields from request payload (POST/PUT)
        if "exclude" in kwargs:
            vals_to_exclude = {
                1,
                "created",
                2,
                "last_modified",
                3,
                "deleted",
            }
            kwargs["exclude"].update(vals_to_exclude)
        else:
            kwargs["exclude"] = {
                1,
                "created",
                2,
                "last_modified",
                3,
                "deleted",
            }

        return super().dict(*args, **kwargs)
