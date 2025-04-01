from abc import ABC, abstractmethod

from application.interfaces.mongo_repo import IMongoRepo
from .dto import CreateTaskDto, UpdateTaskDto, DeleteTaskDto


class CRUDTasksUseCase(ABC):
    def __init__(self, mongodb_repo: IMongoRepo):
        self.mongodb_repo = mongodb_repo

    @abstractmethod
    async def create(self, dto: CreateTaskDto): pass

    @abstractmethod
    async def update(self, dto: UpdateTaskDto): pass

    @abstractmethod
    async def delete(self, dto: DeleteTaskDto): pass
