from logging import getLogger

from application.use_cases.tasks.dto import (
    CreateTaskDto,
    UpdateTaskDto,
)
from application.use_cases.assignees.dto import (
    CreateAssigneeDTO,
)
from application.use_cases.projects.dto import (
    CreateProjectDTO,
)
from application.use_cases.tasks.crud_tasks_use_case import (
    CRUDTasksUseCase
)
from application.use_cases.projects.crud_projects_use_case import (
    CRUDProjectsUseCase
)
from application.use_cases.assignees.crud_assignees_use_case import (
    CRUDAssigneesUseCase
)

logger = getLogger(__name__)


class CheckEventsDriver:
    def __init__(
            self,
            crud_tasks_use_case: CRUDTasksUseCase,
            crud_projects_use_case: CRUDProjectsUseCase,
            crud_assignees_use_case: CRUDAssigneesUseCase
    ):
        self._tasks_use_case = crud_tasks_use_case
        self._projects_use_case = crud_projects_use_case
        self._assignees_use_case = crud_assignees_use_case

    async def check_events(self, message: dict):
        try:
            logger.info("Получено сообщение:", message)
            event_type = message['event_type']

            if event_type == 'project_event':
                project_dto = CreateProjectDTO(
                    id=message['project_id'],
                    creator=message['owner_id'],
                    created_at=message['created_at'],
                    updated_at=message['updated_at']
                )
                logger.info("Создается проект с датой:", project_dto)
                await self._projects_use_case.create(project_dto)
            if event_type == 'members_event':
                assignee_dto = CreateAssigneeDTO(
                    project_id=message['project_id'],
                    user_id=message['user_id']
                )
                logger.info("Создается участник с датой:", assignee_dto)
                await self._assignees_use_case.create(assignee_dto)
            if event_type == 'ticket_event':
                task_dto = CreateTaskDto(
                    id=message['ticket_id'],
                    project_id=message['project_id'],
                    status=message['status'],
                    creator=message['creator'],
                    assignees_ids=message['assignee_ids'],
                    created_at=message['created_at'],
                    updated_at=message['due_date']
                )
                logger.info("Создается таска с датой:", task_dto)
                await self._tasks_use_case.create(task_dto)
            if event_type == 'ticket_status_change':
                task_dto = UpdateTaskDto(
                    id=message['ticket_id'],
                    project_id=message['project_id'],
                    status=message['status']
                )
                await self._tasks_use_case.update(task_dto)
        except Exception as e:
            print(e)
