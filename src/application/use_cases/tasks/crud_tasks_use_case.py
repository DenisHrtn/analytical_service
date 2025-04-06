from abc import ABC, abstractmethod

from application.use_cases.analytics.creating_analytics import CreatingAnalyticsUseCase
from application.interfaces.mongo_repo import IMongoRepo
from .dto import CreateTaskDto, UpdateTaskDto, DeleteTaskDto


class CRUDTasksUseCase(ABC):
    def __init__(
            self,
            mongodb_repo: IMongoRepo,
            analytic_service: CreatingAnalyticsUseCase,
    ):
        self.mongodb_repo = mongodb_repo
        self.analytic_service = analytic_service

    @abstractmethod
    async def get_tasks_statuses_analytics(self, user_id: int): pass

    @abstractmethod
    async def get_count_ready_tasks_per_week_analytics(self, user_id: int): pass

    @abstractmethod
    async def get_average_task_completion_time_analytics(self, user_id: int): pass

    @abstractmethod
    async def create(self, dto: CreateTaskDto): pass

    @abstractmethod
    async def update(self, dto: UpdateTaskDto): pass

    @abstractmethod
    async def delete(self, dto: DeleteTaskDto): pass
