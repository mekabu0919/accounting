from datetime import date

from pytest import fixture

from accountant.project import Project, JSONProject
from accountant.contract import Contract, Transactions, Transaction, Person
from accountant.room import Room, Rooms


@fixture
def project():
    return Project(
        name="Test Project",
        rooms=Rooms({1: Room(id=1, number="101")}),
    )


@fixture
def contract():
    return Contract(
        id=1,
        lessee=Person(family_name="Test", given_name="Lessee"),
        room=Room(id=1, number="101"),
        fee=100,
        deposit=1000,
        key_money=1000,
        start=date(2020, 1, 14),
        end=date(2021, 1, 13),
    )


def test_プロジェクトの新規作成(project):
    assert project.name == "Test Project"
    assert project.contracts == []


def test_プロジェクトに契約を追加(project, contract):
    project.add_contract(contract)
    assert len(project.contracts) == 1
    assert project.contracts[0] == contract


def test_プロジェクトに複数の契約を追加(project, contract):
    contract2 = Contract(
        id=2,
        lessee=Person(family_name="Another", given_name="Lessee"),
        room=Room(id=2, number="102"),
        fee=200,
        deposit=2000,
        key_money=2000,
        start=date(2021, 2, 14),
        end=date(2022, 2, 13),
    )

    project.add_contract(contract)
    project.add_contract(contract2)

    assert len(project.contracts) == 2
    assert project.contracts[0] == contract
    assert project.contracts[1] == contract2


def test_プロジェクトをJSON形式で保存(project, contract):
    project.add_contract(contract)
    json_data = project.to_json()
    assert json_data["name"] == "Test Project"
    assert json_data["contracts"] == [
        {
            "id": 1,
            "lessee": {"family_name": "Test", "given_name": "Lessee"},
            "room_id": 1,
            "fee": 100,
            "deposit": 1000,
            "key_money": 1000,
            "start": "2020-01-14",
            "end": "2021-01-13",
            "transactions": [],
        }
    ]
    assert json_data["rooms"] == {1: {"id": 1, "number": "101"}}


def test_JSON形式のプロジェクトデータを開く():
    json_data: JSONProject = {
        "name": "Test Project",
        "contracts": [
            {
                "id": 1,
                "lessee": {"family_name": "Test", "given_name": "Lessee"},
                "room_id": 1,
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
        "rooms": {1: {"id": 1, "number": "101"}},
    }

    project = Project.from_json(json_data)
    assert project.name == "Test Project"
    assert isinstance(project.contracts[0], Contract)
    assert project.contracts[0].fee == 100
    assert isinstance(project.contracts[0].transactions, Transactions)
    assert isinstance(project.contracts[0].transactions.list[0], Transaction)
