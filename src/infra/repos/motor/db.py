from motor.motor_asyncio import AsyncIOMotorClient

from config import MongoDBConfig


class MongoDBClient:
    def __init__(self, config: MongoDBConfig) -> None:
        self._client = AsyncIOMotorClient(
            f"mongodb://{config.mongo_user}:{config.mongo_password}"
            f"@{config.mongo_host}:{config.mongo_port}/{config.mongo_db}"
        )
        self._db = self._client[config.mongo_db]

    @property
    def client(self) -> AsyncIOMotorClient:
        return self._client

    @property
    def db(self):
        return self._db
