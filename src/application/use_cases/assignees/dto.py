from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateAssigneeDTO:
    project_id: str
    user_id: str


@dataclass
class UpdateAssigneeDTO:
    id: str
    project_id: str
    user_id: str
    updated_at: datetime | None


@dataclass
class DeleteAssigneeDTO:
    id: str
    project_id: str
    user_id: str
