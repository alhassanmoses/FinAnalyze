from dependencies.settings import settings

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient

from typing import Optional


class Database:
    def __init__(self):
        self.client: Optional[AgnosticClient] = None

    async def connect(self, db_uri: str):
        self.client: AgnosticClient = AsyncIOMotorClient(db_uri)

    def get_client(self) -> AgnosticClient:
        return self.client


db = Database()
