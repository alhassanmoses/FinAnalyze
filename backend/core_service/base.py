import pydantic
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime

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
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "firstname": "Moses",
                "lastname": "Alhassan",
                "othernames": "Wuniche",
                "email": "alhassanmoses.amw@gmail.com",
                "username": "moseswuniche",
                "fullname": "Moses Wuniche Alhassan",
            },
            "title": "UserMode",
            "description": "A __model__ representing a user DB __instance__.",
        }
