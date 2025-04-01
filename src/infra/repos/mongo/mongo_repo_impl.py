from typing import Dict, Any, Optional, List

from application.interfaces.mongo_repo import IMongoRepo
from infra.repos.motor.db import MongoDBClient


class MongoRepoImpl(IMongoRepo):
    def __init__(self, db: MongoDBClient):
        self._db = db

    async def get_by_id(self, collection_name: str, doc_id: int):
        db = await self._db.db
        collection = db[collection_name]
        return await collection.find_one({"_id": doc_id})

    async def insert(self, collection_name: str, doc: Dict[str, Any]):
        db = await self._db.db
        collection = db[collection_name]
        data = await collection.insert_one(doc)
        return data.inserted_id

    async def delete(self, collection_name: str, entity_id: int):
        db = await self._db.db
        collection = db[collection_name]
        deleted_obj = await collection.delete_one({"_id": str(entity_id)})
        return deleted_obj.deleted_count > 0

    async def update(
            self,
            collection_name: str,
            entity_id: int,
            update_data: Dict[str, Any]
    ) -> Optional[Dict]:
        db = await self._db.db
        collection = db[collection_name]

        update_data = {key: value for key, value in update_data.items()
                       if value is not None
                       and
                       update_data is not None}

        updated_document = await collection.find_one_and_update(
            {'id', str(entity_id)}, {'$set': update_data}, return_document=True
        )

        return updated_document

    async def find(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        db = await self._db.db
        collection = db[collection_name]
        return await collection.find(query).to_list(None)

    async def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db = await self._db.db
        collection = db[collection_name]
        return await collection.find_one(query)

    async def update_one(
            self,
            collection_name: str,
            query: Dict[str, Any],
            update_data: Dict[str, Any],
            upsert: bool = False
    ):
        db = await self._db.db
        collection = db[collection_name]
        result = await collection.update_one(query, update_data, upsert=upsert)
        return result.modified_count > 0 or result.upserted_id is not None

    async def get_collection_count(self, collection_name: str, query: Dict):
        db = await self._db.db
        collection = db[collection_name]
        return await collection.count_documents(query)

    async def aggregate(self, collection_name: str, pipeline: List[Dict]):
        db = await self._db.db
        collection = db[collection_name]
        return await collection.aggregate(pipeline).to_list(None)
