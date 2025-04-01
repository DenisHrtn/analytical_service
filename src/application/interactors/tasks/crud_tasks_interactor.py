from application.use_cases.tasks.crud_tasks_use_case import CRUDTasksUseCase
from application.use_cases.tasks.dto import CreateTaskDto, UpdateTaskDto, DeleteTaskDto
from application.interfaces.mongo_repo import IMongoRepo
from .exceptions import TaskAlreadyExists


class CRUDTasksInteractor(CRUDTasksUseCase):
    def __init__(self, mongodb_repo: IMongoRepo):
        super().__init__(mongodb_repo)

    async def create(self, dto: CreateTaskDto):
        existing_data = await self.mongodb_repo.get_by_id('tasks', dto.id)
        if existing_data:
            raise TaskAlreadyExists()

        document = {
            'id': dto.id,
            'project_id': dto.project_id,
            'status': dto.status,
            'creator': dto.creator,
            'assignees_ids': dto.assignees_ids,
            'created_at': dto.created_at,
            'updated_at': dto.updated_at
        }

        inserted_data = await self.mongodb_repo.insert('tasks', document)
        return inserted_data

    async def update(self, dto: UpdateTaskDto):
        existing_data = await self.mongodb_repo.get_by_id('tasks', dto.id)

        document = {
            'id': dto.id,
            'project_id': dto.project_id,
            'status': dto.status
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
