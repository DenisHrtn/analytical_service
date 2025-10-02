from abc import ABC, abstractmethod
from typing import Dict, Any

from application.interfaces.mongo_repo import IMongoRepo
from application.use_cases.analytics.creating_analytics import CreatingAnalyticsUseCase
from .dto import CreateProjectDTO, UpdateProjectDTO, DeleteProjectDTO


class CRUDProjectsUseCase(ABC):
    def __init__(
            self,
            mongodb_repo: IMongoRepo,
            analytic_service: CreatingAnalyticsUseCase,
    ):
        self.mongodb_repo = mongodb_repo
        self.analytic_service = analytic_service

    @abstractmethod
    async def get(self, user_id: int) -> Dict[str, Any]: pass

    @abstractmethod
    async def create(self, dto: CreateProjectDTO): pass

    @abstractmethod
    async def update(self, dto: UpdateProjectDTO): pass

    @abstractmethod
    async def delete(self, dto: DeleteProjectDTO): pass
