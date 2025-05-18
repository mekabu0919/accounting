from datetime import date

from pytest import fixture

from accountant.contract import Contract, Transaction


@fixture
def contract():
    return Contract(
        fee=100,
        deposit=1000,
        key_money=1000,
        start=date(2020, 1, 14),
        end=date(2021, 1, 13),
    )


def test_取引履歴を確認する(contract):
    transactions = contract.transactions
    transactions.register(Transaction(date_=date(2020, 1, 1), amount=100, kind="家賃"))
    transactions.register(Transaction(date_=date(2020, 2, 1), amount=100, kind="敷金"))
    transactions.register(Transaction(date_=date(2020, 3, 1), amount=100, kind="礼金"))
    assert contract.transactions.history() == [
        {"日付": date(2020, 1, 1), "金額": 100, "種類": "家賃"},
        {"日付": date(2020, 2, 1), "金額": 100, "種類": "敷金"},
        {"日付": date(2020, 3, 1), "金額": 100, "種類": "礼金"},
    ]


def test_合計受取額を確認する(contract):
    transactions = contract.transactions
    transactions.register(Transaction(date_=date(2020, 1, 1), amount=100, kind="家賃"))
    transactions.register(Transaction(date_=date(2020, 1, 1), amount=100, kind="家賃"))
    transactions.register(Transaction(date_=date(2020, 1, 1), amount=100, kind="手数料"))
    assert contract.transactions.total_reception() == 200


def test_契約開始時の日割りの家賃を計算する(contract):
    result = contract.calculate_prorated_initial_fee()
    assert result == 100 * (31 - 14 + 1) // 31


def test_契約終了時の日割りの家賃を計算する(contract):
    result = contract.calculate_prorated_final_fee()
    assert result == 100 * 13 // 31
