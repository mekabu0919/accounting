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

    @classmethod
    def from_json(cls, data: JSONRoom) -> "Room":
        return cls(id=data["id"], number=data["number"])


class Rooms:
    def __init__(self, initial_data: dict[int, Room] = {}):
        self._id_map: dict[int, Room] = initial_data

    def add(self, room: Room):
        self._id_map[room.id] = room

    def __len__(self) -> int:
        return len(self._id_map)

    def get(self, id: int) -> Room:
        return self._id_map[id]

    def get_all(self) -> list[Room]:
        return list(self._id_map.values())

    def to_json(self) -> dict[int, JSONRoom]:
        return {id: room.to_json() for id, room in self._id_map.items()}

    @classmethod
    def from_json(cls, json_data: dict[int, JSONRoom]) -> "Rooms":
        return cls(initial_data={id: Room.from_json(data) for id, data in json_data.items()})
