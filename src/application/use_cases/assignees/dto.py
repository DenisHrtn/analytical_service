from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateAssigneeDTO:
    id: int
    project_id: int
    user_id: int
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class UpdateAssigneeDTO:
    id: int
    project_id: int
    user_id: int
    updated_at: datetime | None


@dataclass
class DeleteAssigneeDTO:
    id: int
    project_id: int
    user_id: int
