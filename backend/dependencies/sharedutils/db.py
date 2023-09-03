from dependencies.settings import settings

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient

from typing import Optional
from datetime import datetime


class Database:
    def __init__(self):
        self.client: Optional[AgnosticClient] = None

    async def connect(self, db_uri: str):
        self.client: AgnosticClient = AsyncIOMotorClient(db_uri)

    def get_client(self) -> AgnosticClient:
        return self.client


db = Database()


def get_base_query(is_insert=False, is_update=False):
    if is_insert:
        now = datetime.utcnow()
        return {"created": now, "last_modified": now}
    elif is_update:
        now = datetime.utcnow()
        return {"last_modified": now}
    else:
        return {}
