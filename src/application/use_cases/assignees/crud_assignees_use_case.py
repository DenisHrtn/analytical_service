from abc import abstractmethod, ABC

from application.interfaces.mongo_repo import IMongoRepo
from application.use_cases.analytics.creating_analytics import CreatingAnalyticsUseCase
from .dto import CreateAssigneeDTO, DeleteAssigneeDTO, UpdateAssigneeDTO


class CRUDAssigneesUseCase:
    def __init__(self, mongodb_repo: IMongoRepo) -> None:
        self.mongodb_repo = mongodb_repo

    @abstractmethod
    async def create(self, assignee: CreateAssigneeDTO): pass

    @abstractmethod
    async def update(self, assignee: UpdateAssigneeDTO): pass

    @abstractmethod
    async def delete(self, assignee: DeleteAssigneeDTO): pass
