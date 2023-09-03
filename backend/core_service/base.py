import pydantic
import logging

from bson import ObjectId
from pydantic import BaseModel
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
    created: datetime = Body(datetime.utcnow())
    last_modified: datetime = datetime.utcnow()
    _deleted: Optional[datetime]

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

    def to_dict(self) -> any:
        return jsonable_encoder(self)
