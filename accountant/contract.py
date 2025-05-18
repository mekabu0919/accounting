import calendar
from datetime import date


class Transaction:
    reception_kinds = [
        "家賃", "敷金", "礼金", "更新料", "共益費", "保証料"
    ]
    payment_kinds = [
        "手数料", "修繕費"
    ]

    def __init__(self, date_: date, amount: int, kind: str):
        self.date = date_
        self.amount = amount
        self.kind = kind
        self.type = self._judge_type()

    def _judge_type(self):
        if self.kind in self.reception_kinds:
            return "受取"
        if self.kind in self.payment_kinds:
            return "支払"
        else:
            raise ValueError(f"Invalid kind: {self.kind}")

    def to_dict(self):
        return {
            "日付": self.date,
            "金額": self.amount,
            "種類": self.kind,
        }


class Contract:
    def __init__(self, fee, deposit, key_money, start: date, end: date):
        self.fee = fee
        self.deposit = deposit
        self.key_money = key_money
        self.start = start
        self.end = end
        self.transactions = Transactions()

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


class Transactions:
    def __init__(self):
        self.list = []

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

    def history(self):
        return [reception.to_dict() for reception in self.list]
