from .exceptions import AssigneeAlreadyExistsException
from application.interfaces.mongo_repo import IMongoRepo
from application.use_cases.assignees.crud_assignees_use_case import (
    CRUDAssigneesUseCase
)
from application.use_cases.assignees.dto import (
    CreateAssigneeDTO,
    DeleteAssigneeDTO,
    UpdateAssigneeDTO
)


class CRUDAssigneesInteractor(CRUDAssigneesUseCase):
    def __init__(self, mongodb_repo: IMongoRepo) -> None:
        super().__init__(mongodb_repo)

    async def create(self, assignee: CreateAssigneeDTO):
        existing_data = await self.mongodb_repo.get_by_id('assignees', str(assignee.user_id))
        if existing_data:
            raise AssigneeAlreadyExistsException()

        document = {
            'id': str(assignee.user_id),
            'project_id': str(assignee.project_id),
            'user_id': str(assignee.user_id),
        }

        inserted_data = await self.mongodb_repo.insert('assignees', document)
        return inserted_data

    async def update(self, assignee: UpdateAssigneeDTO):
        existing_data = await self.mongodb_repo.get_by_id('assignees', assignee.id)

        document = {
            'id': assignee.id,
            'project_id': assignee.project_id,
            'user_id': assignee.user_id,
            'updated_at': assignee.updated_at
        }

        if existing_data:
            updated_data = await self.mongodb_repo.update('assignees', assignee.id, document)
            return updated_data
        else:
            return None

    async def delete(self, assignee: DeleteAssigneeDTO):
        existing_data = await self.mongodb_repo.get_by_id('assignees', assignee.id)
        if existing_data:
            deleted_data = await self.mongodb_repo.delete('assignees', assignee.id)
            return deleted_data
        else:
            return None
