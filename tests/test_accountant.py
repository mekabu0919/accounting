from datetime import date

from pytest import fixture

from accountant.contract import Contract


@fixture
def contract():
    return Contract(
        fee=100,
        deposit=1000,
        key_money=1000,
        start=date(2020, 1, 14),
        end=date(2021, 1, 13),
    )


def test_月ごとの支払い履歴を確認する(contract):
    contract.receive_fee(date_=date(2020, 1, 1))
    contract.receive_fee(date_=date(2020, 2, 1))
    contract.receive_fee(date_=date(2020, 3, 1))
    assert contract.payments.history(2020) == {
        1: 100,
        2: 100,
        3: 100,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
    }


def test_契約開始時の日割りの家賃を計算する(contract):
    result = contract.calculate_prorated_initial_fee()
    assert result == 100 * (31 - 14) // 31


def test_日割りの家賃と敷金礼金を受け取る(contract):
    contract.receive_initial_cost(date(2019, 12, 20))
    contract.receive_fee(
        date(2019, 12, 20), fee=contract.calculate_prorated_initial_fee()
    )
    assert contract.payments.total() == 1000 + 1000 + 54
    assert contract.payments.history(2019) == {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 2054,
    }