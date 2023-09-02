from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from core_service.exceptions import InvalidId


class ObjectIdField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        try:
            return ObjectId(str(value))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class Base(BaseModel):
    created: datetime = Field(datetime.utcnow())
    last_modified: datetime = Field(datetime.utcnow())

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
