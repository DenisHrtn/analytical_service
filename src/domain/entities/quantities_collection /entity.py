from dataclasses import dataclass


@dataclass
class QuantitiesCollection:
    user_id: int
    projects: list[int]
    tasks: dict[int, list[int]]
    members: dict[int, list[int]]
