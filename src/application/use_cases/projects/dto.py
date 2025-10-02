from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateProjectDTO:
    id: int
    creator: int | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class UpdateProjectDTO:
    id: int
    creator: int | None
    updated_at: datetime | None


@dataclass
class DeleteProjectDTO:
    id: int
