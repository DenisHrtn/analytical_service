from application.use_cases.tasks.crud_tasks_use_case import CRUDTasksUseCase
from application.use_cases.tasks.dto import CreateTaskDto, UpdateTaskDto, DeleteTaskDto
from application.interfaces.mongo_repo import IMongoRepo
from application.use_cases.analytics.creating_analytics import CreatingAnalyticsUseCase
from .exceptions import TaskAlreadyExists


class CRUDTasksInteractor(CRUDTasksUseCase):
    def __init__(
            self,
            mongodb_repo: IMongoRepo,
            analytic_service: CreatingAnalyticsUseCase,
    ):
        super().__init__(mongodb_repo, analytic_service)

    async def get_tasks_statuses_analytics(self, user_id: int):
        data = await self.analytic_service.create_tasks_statuses_analytics(user_id)
        return data

    async def get_count_ready_tasks_per_week_analytics(self, user_id: int):
        data = await self.analytic_service.count_ready_tasks_per_week_analytics(user_id)
        return data

    async def get_average_task_completion_time_analytics(self, user_id: int):
        data = await self.analytic_service.average_task_completion_time_analytics(user_id)
        return data

    async def create(self, dto: CreateTaskDto):
        existing_data = await self.mongodb_repo.get_by_id('tasks', dto.id)
        if existing_data:
            raise TaskAlreadyExists()

        document = {
            'id': str(dto.id),
            'project_id': str(dto.project_id),
            'status': str(dto.status),
            'creator': str(dto.creator),
            'assignees_ids': str(dto.assignees_ids),
            'created_at': str(dto.created_at),
            'updated_at': str(dto.updated_at)
        }

        inserted_data = await self.mongodb_repo.insert('tasks', document)
        return inserted_data

    async def update(self, dto: UpdateTaskDto):
        existing_data = await self.mongodb_repo.get_by_id('tasks', dto.id)

        document = {
            'id': str(dto.id),
            'project_id': str(dto.project_id),
            'status': str(dto.status)
        }

        if existing_data:
            updated_data = await self.mongodb_repo.update('tasks', dto.id, document)
            return updated_data
        else:
            return None

    async def delete(self, dto: DeleteTaskDto):
        existing_data = await self.mongodb_repo.get_by_id('tasks', dto.id)
        if existing_data:
            deleted_data = await self.mongodb_repo.delete('tasks', dto.id)
            return deleted_data
        else:
            return None
