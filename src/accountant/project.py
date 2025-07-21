from typing import TypedDict

from .contract import Contract, JSONContract
from .room import Rooms, JSONRoom

class JSONProject(TypedDict):
    name: str
    contracts: list[JSONContract]
    rooms: dict[int, JSONRoom]


class Project:
    def __init__(self, name: str, contracts: list[Contract] | None = None, rooms: Rooms | None = None):
        self.name = name
        self.contracts = contracts if contracts is not None else []
        self.rooms = rooms if rooms is not None else Rooms()

    def add_contract(self, contract):
        self.contracts.append(contract)

    def to_json(self) -> JSONProject:
        return {
            "name": self.name,
            "contracts": [contract.to_json() for contract in self.contracts],
            "rooms": self.rooms.to_json(),
        }

    @classmethod
    def from_json(cls, json_data: JSONProject) -> "Project":
        return cls(
            name=json_data["name"],
            contracts=[
                Contract.from_json(contract_data)
                for contract_data in json_data["contracts"]
            ],
            rooms=Rooms.from_json(json_data["rooms"]),
        )
