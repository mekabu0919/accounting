import calendar
from datetime import date


class Contract:
    def __init__(self, fee, deposit, key_money, start: date, end: date):
        self.fee = fee
        self.deposit = deposit
        self.key_money = key_money
        self.start = start
        self.end = end
        self.receptions = Receptions()

    def receive_initial_cost(self, date_: date):
        self.receptions.append(Reception(date_, self.deposit + self.key_money))

    def receive_fee(self, date_: date, fee: int):
        self.receptions.append(Reception(date_, fee))

    def calculate_prorated_initial_fee(self):
        year = self.start.year
        month = self.start.month
        days_in_month = calendar.monthrange(year, month)[1]
        return self.fee * (days_in_month - self.start.day) // days_in_month


class Reception:
    def __init__(self, date_: date, amount: int):
        self.date = date_
        self.amount = amount


class Receptions:
    def __init__(self):
        self.list = []

    def total(self):
        return sum(reception.amount for reception in self.list)

    def append(self, reception: Reception):
        self.list.append(reception)

    def history(self, year: int):
        history = {month: 0 for month in range(1, 13)}
        for reception in self.list:
            if reception.date.year == year:
                history[reception.date.month] += reception.amount
        return history
