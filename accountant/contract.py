import calendar
from datetime import date


class Contract:
    def __init__(self, fee, deposit, key_money, start: date, end: date):
        self.fee = fee
        self.deposit = deposit
        self.key_money = key_money
        self.start = start
        self.end = end
        self.payments = Payments()

    def receive_initial_cost(self, date_):
        self.payments.append(date_, self.deposit + self.key_money)

    def receive_fee(self, date_, fee=None):
        if fee is None:
            self.payments.append(date_, self.fee)
        else:
            self.payments.append(date_, fee)

    def calculate_prorated_initial_fee(self):
        year = self.start.year
        month = self.start.month
        days_in_month = calendar.monthrange(year, month)[1]
        return self.fee * (days_in_month - self.start.day) // days_in_month

class Payments:
    def __init__(self):
        self.list = []

    def total(self):
        return sum(payment[1] for payment in self.list)

    def append(self, date_, amount):
        self.list.append((date_, amount))

    def history(self, year):
        history = {month: 0 for month in range(1, 13)}
        for payment_date, amount in self.list:
            if payment_date.year == year:
                history[payment_date.month] += amount
        return history