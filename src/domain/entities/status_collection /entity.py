from dataclasses import dataclass


@dataclass
class StatusCollection:
    analytics: dict[int, list[int]]
