from typing import Any, Optional, Dict, List
from abc import ABC, abstractmethod


class IMongoRepo(ABC):
    @abstractmethod
    async def get_by_id(self, collection_name: str, doc_id: int): pass

    @abstractmethod
    async def insert(self, collection_name: str, doc: Dict[str, Any]): pass

    @abstractmethod
    async def delete(self, collection_name: str, entity_id: int): pass

    @abstractmethod
    async def update(
            self,
            collection_name: str,
            entity_id: int,
            update_data: Dict[str, Any]
    ) -> Optional[Dict]: pass

    @abstractmethod
    async def find(self, collection_name: str, query: Dict[str, Any]) -> List[Dict[str, Any]]: pass

    @abstractmethod
    async def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]: pass

    @abstractmethod
    async def update_one(
            self,
            collection_name: str,
            query: Dict[str, Any],
            update_data: Dict[str, Any],
            upsert: bool = False
    ): pass

    @abstractmethod
    async def get_collection_count(self, collection_name: str, query: Dict): pass

    @abstractmethod
    async def aggregate(self, collection_name: str, pipeline: List[Dict]): pass
