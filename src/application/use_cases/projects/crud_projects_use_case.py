from abc import ABC, abstractmethod

from application.interfaces.mongo_repo import IMongoRepo
from .dto import CreateProjectDTO, UpdateProjectDTO, DeleteProjectDTO


class CRUDProjectsUseCase(ABC):
    def __init__(self, mongodb_repo: IMongoRepo):
        self.mongodb_repo = mongodb_repo

    @abstractmethod
    async def create(self, dto: CreateProjectDTO): pass

    @abstractmethod
    async def update(self, dto: UpdateProjectDTO): pass

    @abstractmethod
    async def delete(self, dto: DeleteProjectDTO): pass
