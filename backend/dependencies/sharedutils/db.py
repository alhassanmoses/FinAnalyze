from dependencies.settings import settings

from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    def __init__(self):
        self.client = None

    async def connect(self, db_uri):
        self.client = AsyncIOMotorClient(db_uri)

    def get_client(self):
        return self.client


db = Database()
