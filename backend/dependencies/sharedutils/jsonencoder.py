import json
from datetime import datetime, date
from bson import ObjectId, Decimal128
from decimal import Decimal


class JSONEncoder(json.JSONEncoder):
    """A Helper to fix the error converting ObjectIds from MongoDB when serializing

    Args:
        json (JSONEncoder): A valid Json encoder class
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        # Safely converting monetary amounts to Decimal types to avoid python's approximation of floats
        if isinstance(o, (Decimal128, Decimal)):
            return str(o)
        return json.JSONEncoder.default(self, o)


def jsonHelper(data: any) -> dict:
    """A helper to quickly serialize objects with ObjectID fields

    Args:
        data (any): Any serializable object

    Returns:
        dict[any, any]: A json seriablized instance of the provided object
    """
    return json.loads(JSONEncoder().encode(data))


# TODO: Look into why this convertion returned an object for all default type objects.
# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         try:
#             return json_util.default(o)
#         except TypeError:
#             return str(o)
