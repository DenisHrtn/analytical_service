from application.interactors.tasks.crud_tasks_interactor import (
    CRUDTasksInteractor
)
from infra.services.decode_jwt_token.get_token import get_token
from containers import Container

from fastapi import (
    APIRouter,
    Depends,
    status,
    Request
)
from dependency_injector.wiring import Provide, inject


router = APIRouter(tags=['tasks'])


@router.get('/tasks-statuses', status_code=status.HTTP_200_OK)
@inject
async def get_tasks_statuses_analytics(
        request: Request,
        crud_tasks_interactor: CRUDTasksInteractor = Depends(
            Provide[Container.crud_tasks_interactor]
        )
):
    user_id = await get_token(request)
    return await crud_tasks_interactor.get_tasks_statuses_analytics(user_id)


@router.get('/count-ready-tasks-per-week', status_code=status.HTTP_200_OK)
@inject
async def get_count_ready_tasks_per_week(
    request: Request,
        crud_tasks_interactor: CRUDTasksInteractor = Depends(
            Provide[Container.crud_tasks_interactor]
        )
):
    user_id = await get_token(request)
    return await crud_tasks_interactor.get_count_ready_tasks_per_week_analytics(user_id)


@router.get('/average-task-completion-time', status_code=status.HTTP_200_OK)
@inject
async def get_average_task_completion_time(
        request: Request,
        crud_tasks_interactor: CRUDTasksInteractor = Depends(
            Provide[Container.crud_tasks_interactor]
        )
):
    user_id = await get_token(request)
    return await crud_tasks_interactor.get_average_task_completion_time_analytics(user_id)
