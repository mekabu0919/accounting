import calendar
from datetime import date
from typing import TypedDict
from dataclasses import dataclass

from .room import Room, JSONRoom


class JSONTransaction(TypedDict):
    date: str
    amount: int
    kind: str


@dataclass
class Transaction:
    date: date
    amount: int
    kind: str

    _reception_kinds = ["家賃", "敷金", "礼金", "更新料", "共益費", "保証料"]
    _payment_kinds = ["手数料", "修繕費"]

    @property
    def type(self):
        if self.kind in self._reception_kinds:
            return "受取"
        if self.kind in self._payment_kinds:
            return "支払"
        else:
            raise ValueError(f"Invalid kind: {self.kind}")

    def to_json(self) -> JSONTransaction:
        return {
            "date": self.date.isoformat(),
            "amount": self.amount,
            "kind": self.kind,
        }

    @classmethod
    def from_json(cls, data: JSONTransaction) -> "Transaction":
        return cls(
            date=date.fromisoformat(data["date"]),
            amount=data["amount"],
            kind=data["kind"],
        )


class Transactions:
    def __init__(self, initial_list: list[Transaction] = []):
        for transaction in initial_list:
            if not isinstance(transaction, Transaction):
                raise TypeError("All items must be of type Transaction")
        self.list = list(initial_list)

    def __getitem__(self, index: int) -> Transaction:
        return self.list[index]

    def total_reception(self):
        return sum(
            reception.amount for reception in self.list if reception.type == "受取"
        )

    def total_payment(self):
        return sum(
            reception.amount for reception in self.list if reception.type == "支払"
        )

    def register(self, reception: Transaction):
        self.list.append(reception)

    def to_json(self) -> list[JSONTransaction]:
        return [transaction.to_json() for transaction in self.list]


class JSONPerson(TypedDict):
    family_name: str
    given_name: str


@dataclass
class Person:
    family_name: str
    given_name: str

    @property
    def full_name(self) -> str:
        return f"{self.family_name} {self.given_name}"

    def to_json(self) -> JSONPerson:
        return {
            "family_name": self.family_name,
            "given_name": self.given_name,
        }


class JSONContract(TypedDict):
    id: int
    lessee: JSONPerson
    room: JSONRoom
    fee: int
    deposit: int
    key_money: int
    start: str
    end: str
    transactions: list[JSONTransaction]


class Contract:
    def __init__(
        self,
        id: int,
        lessee: Person,
        room: Room,
        fee: int,
        deposit: int,
        key_money: int,
        start: date,
        end: date,
        transactions: Transactions | None = None,
    ):
        self.id = id
        self.lessee = lessee
        self.room = room
        self.fee = fee
        self.deposit = deposit
        self.key_money = key_money
        self.start = start
        self.end = end
        self.transactions = transactions if transactions is not None else Transactions()

    def calculate_prorated_initial_fee(self):
        year = self.start.year
        month = self.start.month
        days_in_month = calendar.monthrange(year, month)[1]
        return self.fee * (days_in_month - self.start.day + 1) // days_in_month

    def calculate_prorated_final_fee(self):
        year = self.end.year
        month = self.end.month
        days_in_month = calendar.monthrange(year, month)[1]
        return self.fee * self.end.day // days_in_month

    def to_json(self) -> JSONContract:
        return {
            "id": self.id,
            "lessee": self.lessee.to_json(),
            "room": self.room.to_json(),
            "fee": self.fee,
            "deposit": self.deposit,
            "key_money": self.key_money,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "transactions": self.transactions.to_json(),
        }

    @classmethod
    def from_json(cls, data: JSONContract) -> "Contract":
        transactions = Transactions(
            [Transaction.from_json(t) for t in data["transactions"]]
        )
        return cls(
            id=data["id"],
            lessee=Person(**data["lessee"]),
            room=Room(**data["room"]),
            fee=data["fee"],
            deposit=data["deposit"],
            key_money=data["key_money"],
            start=date.fromisoformat(data["start"]),
            end=date.fromisoformat(data["end"]),
            transactions=transactions,
        )
