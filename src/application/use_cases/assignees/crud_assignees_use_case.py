from application.interfaces.mongo_repo import IMongoRepo
from .dto import CreateAssigneeDTO, DeleteAssigneeDTO, UpdateAssigneeDTO


class CRUDAssigneesUseCase:
    def __init__(self, mongodb_repo: IMongoRepo) -> None:
        self.mongodb_repo = mongodb_repo

    async def create(self, assignee: CreateAssigneeDTO): pass

    async def update(self, assignee: UpdateAssigneeDTO): pass

    async def delete(self, assignee: DeleteAssigneeDTO): pass
