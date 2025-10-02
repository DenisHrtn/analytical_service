from abc import ABC, abstractmethod

from application.interfaces.mongo_repo import IMongoRepo


class CreatingAnalyticsUseCase(ABC):
    def __init__(self, mongodb_repo: IMongoRepo):
        self.mongodb_repo = mongodb_repo

    @abstractmethod
    async def create_analytics(self, user_id: int): pass

    @abstractmethod
    async def create_tasks_statuses_analytics(self, user_id: int): pass

    @abstractmethod
    async def count_ready_tasks_per_week_analytics(self, user_id: int): pass

    @abstractmethod
    async def average_task_completion_time_analytics(self, user_id: int): pass

