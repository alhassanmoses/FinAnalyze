import pydantic
from bson import ObjectId, Decimal128
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from motor.core import AgnosticDatabase
from fastapi.encoders import jsonable_encoder

from core_service.exceptions import InvalidId


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
            raise ValueError("Invalid ObjectId provided")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Base(BaseModel):
    created: datetime = Field(datetime.utcnow())
    last_modified: datetime = datetime.utcnow()

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
                "created": "2023-09-02T16:58:24.129000",
                "last_modified": "2023-09-02T16:58:24.130000",
            },
            "title": "UserMode",
            "description": "A __model__ representing a user DB __instance__.",
        }

    @staticmethod
    async def get_by_id(id: any, collection: str, db: AgnosticDatabase):
        entity = await db[collection].find_one({"_id": ObjectId(str(id))})
        if entity is not None:
            return entity
        return None

    def to_dict(self) -> any:
        # # Convert Decimal128 fields to Decimal in the dictionary
        # for field_name in data:
        #     if isinstance(data[field_name], Decimal128):
        #         data[field_name] = Decimal(data[field_name].to_decimal())

        # return data
        return jsonable_encoder(self)
