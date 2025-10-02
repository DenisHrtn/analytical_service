from typing import Dict, Any

from application.use_cases.projects.crud_projects_use_case import CRUDProjectsUseCase
from application.use_cases.projects.dto import CreateProjectDTO, UpdateProjectDTO, DeleteProjectDTO
from application.interfaces.mongo_repo import IMongoRepo
from application.use_cases.analytics.creating_analytics import CreatingAnalyticsUseCase
from application.interfaces.decode_tokens.decode_tokens import IDecodeTokens
from .exceptions import ProjectAlreadyExists, ProjectDoesNotExist


class CRUDProjectsInteractor(CRUDProjectsUseCase):
    def __init__(
            self,
            mongodb_repo: IMongoRepo,
            analytic_service: CreatingAnalyticsUseCase
    ):
        super().__init__(mongodb_repo, analytic_service)

    async def get(self, user_id: int) -> Dict[str, Any]:
        data = await self.analytic_service.create_analytics(user_id)

        return data

    async def create(self, dto: CreateProjectDTO):
        existing_data = await self.mongodb_repo.get_by_id('projects', str(dto.id))
        if existing_data is not None:
            raise ProjectAlreadyExists()

        document = {

            'id': str(dto.id),
            'creator': str(dto.creator),
            'created_at': str(dto.created_at),
            'updated_at': str(dto.updated_at),
        }

        inserted_data = await self.mongodb_repo.insert('projects', document)
        return inserted_data

    async def update(self, dto: UpdateProjectDTO):
        existing_data = await self.mongodb_repo.get_by_id('projects', dto.id)

        document = {
            'id': str(dto.id),
            'creator': str(dto.creator),
            'updated_at': str(dto.updated_at)
        }

        if existing_data:
            updated = await self.mongodb_repo.update('projects', dto.id, document)
            return updated
        else:
            raise ProjectDoesNotExist()

    async def delete(self, dto: DeleteProjectDTO):
        existing_data = await self.mongodb_repo.get_by_id('projects', dto.id)
        if existing_data:
            deleted_data = await self.mongodb_repo.delete('projects', dto.id)
            return deleted_data
        else:
            raise ProjectDoesNotExist()
