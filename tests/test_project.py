from datetime import date

from accountant.project import Project, JSONProject
from accountant.contract import Contract, Transactions, Transaction


def test_プロジェクトの新規作成():
    project = Project(
        name="Test Project",
    )
    assert project.name == "Test Project"
    assert project.contracts == []


def test_プロジェクトに契約を追加():
    project = Project(
        name="Test Project",
    )

    contract = Contract(
        fee=100,
        deposit=1000,
        key_money=1000,
        start=date(2020, 1, 14),
        end=date(2021, 1, 13),
    )

    project.add_contract(contract)
    assert len(project.contracts) == 1
    assert project.contracts[0] == contract


def test_プロジェクトに複数の契約を追加():
    project = Project(
        name="Test Project",
    )

    contract1 = Contract(
        fee=100,
        deposit=1000,
        key_money=1000,
        start=date(2020, 1, 14),
        end=date(2021, 1, 13),
    )
    contract2 = Contract(
        fee=200,
        deposit=2000,
        key_money=2000,
        start=date(2021, 2, 14),
        end=date(2022, 2, 13),
    )

    project.add_contract(contract1)
    project.add_contract(contract2)

    assert len(project.contracts) == 2
    assert project.contracts[0] == contract1
    assert project.contracts[1] == contract2


def test_プロジェクトをJSON形式で保存():
    project = Project(
        name="Test Project",
    )

    contract = Contract(
        fee=100,
        deposit=1000,
        key_money=1000,
        start=date(2020, 1, 14),
        end=date(2021, 1, 13),
    )

    project.add_contract(contract)

    json_data = project.to_json()
    assert json_data["name"] == "Test Project"
    assert len(json_data["contracts"]) == 1
    assert json_data["contracts"][0]["fee"] == 100
    assert json_data["contracts"][0]["deposit"] == 1000
    assert json_data["contracts"][0]["key_money"] == 1000
    assert json_data["contracts"][0]["start"] == "2020-01-14"
    assert json_data["contracts"][0]["end"] == "2021-01-13"
    assert json_data["contracts"][0]["transactions"] == []


def test_JSON形式のプロジェクトデータを開く():
    json_data: JSONProject = {
        "name": "Test Project",
        "contracts": [
            {
                "fee": 100,
                "deposit": 1000,
                "key_money": 1000,
                "start": "2020-01-14",
                "end": "2021-01-13",
                "transactions": [
                    {
                        "date": "2020-01-14",
                        "amount": 1000,
                        "kind": "家賃",
                    }
                ],
            }
        ],
    }

    project = Project.from_json(json_data)
    assert project.name == "Test Project"
    assert isinstance(project.contracts[0], Contract)
    assert project.contracts[0].fee == 100
    assert isinstance(project.contracts[0].transactions, Transactions)
    assert isinstance(project.contracts[0].transactions.list[0], Transaction)
