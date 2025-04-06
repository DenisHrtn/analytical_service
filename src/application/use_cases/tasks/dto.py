from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class CreateTaskDto:
    id: str
    project_id: str
    status: str
    creator: str
    assignees_ids: List[int]
    created_at: datetime
    updated_at: datetime


@dataclass
class UpdateTaskDto:
    id: str
    project_id: str
    status: str


@dataclass
class DeleteTaskDto:
    id: str
    project_id: str
