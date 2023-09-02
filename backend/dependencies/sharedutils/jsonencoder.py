import json
from datetime import datetime, date
from bson import ObjectId

from bson import json_util


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
        return json.JSONEncoder.default(self, o)


def jsonHelper(data: any) -> dict:
    """A helper to quickly serialize objects with ObjectID fields

    Args:
        data (any): Any serializable object

    Returns:
        dict[any, any]: A json seriablized instance of the provided object
    """
    return json.loads(JSONEncoder().encode(data))


# TODO: Look into why this converted returned an object for all default type objects.
# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         try:
#             return json_util.default(o)
#         except TypeError:
#             return str(o)
