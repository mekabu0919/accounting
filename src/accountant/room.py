from dataclasses import dataclass
from typing import TypedDict


class JSONRoom(TypedDict):
    id: int
    number: str


@dataclass
class Room:
    id: int
    number: str

    def to_json(self) -> JSONRoom:
        return {
            "id": self.id,
            "number": self.number,
        }
