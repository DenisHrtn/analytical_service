from application.interactors.projects.crud_projects_interactor import (
    CRUDProjectsInteractor
)
from containers import Container
from infra.services.decode_jwt_token.get_token import get_token

from fastapi import (
    APIRouter,
    Depends,
    status,
    Request
)
from dependency_injector.wiring import Provide, inject

router = APIRouter(tags=['projects-stats'])


@router.get('/projects-stats', status_code=status.HTTP_200_OK)
@inject
async def get_projects_stats(
        request: Request,
        crud_projects_interactor: CRUDProjectsInteractor = Depends(
            Provide[Container.crud_projects_interactor]
        ),
):
    user_id = await get_token(request)
    return await crud_projects_interactor.get(user_id)
