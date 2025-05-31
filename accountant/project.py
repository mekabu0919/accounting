from typing import TypedDict

from .contract import Contract, JSONContract


class JSONProject(TypedDict):
    name: str
    contracts: list[JSONContract]


class Project:
    def __init__(self, name: str, contracts: list[Contract] | None = None):
        self.name = name
        self.contracts = contracts if contracts is not None else []

    def add_contract(self, contract):
        self.contracts.append(contract)

    def to_json(self) -> JSONProject:
        return {
            "name": self.name,
            "contracts": [contract.to_json() for contract in self.contracts],
        }

    @classmethod
    def from_json(cls, json_data: JSONProject) -> "Project":
        return cls(
            json_data["name"],
            [
                Contract.from_json(contract_data)
                for contract_data in json_data["contracts"]
            ],
        )
