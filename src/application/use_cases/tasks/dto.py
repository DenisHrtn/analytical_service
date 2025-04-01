from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class CreateTaskDto:
    id: int
    project_id: int
    status: str
    creator: int
    assignees_ids: List[int]
    created_at: datetime
    updated_at: datetime


@dataclass
class UpdateTaskDto:
    id: int
    project_id: int
    status: str


@dataclass
class DeleteTaskDto:
    id: int
    project_id: int
