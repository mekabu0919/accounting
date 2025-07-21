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
    def __init__(self):
        self.list: list[Room] = []

    def add(self, room: Room):
        self.list.append(room)

    def get(self, id: int) -> Room:
        for room in self.list:
            if room.id == id:
                return room
        raise ValueError(f"Room with id {id} not found")

    def to_json(self) -> list[JSONRoom]:
        return [room.to_json() for room in self.list]

    @classmethod
    def from_json(cls, json_data: list[JSONRoom]) -> "Rooms":
        rooms = cls()
        for room_data in json_data:
            rooms.add(Room(**room_data))
        return rooms
