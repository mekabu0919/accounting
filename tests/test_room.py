from accountant.room import Room, JSONRoom, Rooms
from accountant.contract import Contract

def test_部屋情報をJSON形式で保存():
    room = Room(id=1, number="101")
    json_data = room.to_json()
    assert json_data == {"id": 1, "number": "101"}


def test_部屋情報をJSON形式から復元():
    json_data: JSONRoom = {"id": 1, "number": "101"}
    room = Room.from_json(json_data)
    assert room.id == 1
    assert room.number == "101"


def test_部屋のリストをJSON形式で保存():
    rooms = Rooms({1: Room(id=1, number="101"), 2: Room(id=2, number="102")})
    json_data = rooms.to_json()
    assert json_data == {
        1: {"id": 1, "number": "101"},
        2: {"id": 2, "number": "102"},
    }


def test_部屋のリストをJSON形式から復元():
    json_data: dict[int, JSONRoom] = {
        1: {"id": 1, "number": "101"},
        2: {"id": 2, "number": "102"},
    }
    rooms = Rooms.from_json(json_data)
    assert len(rooms) == 2
    assert rooms.get(1).id == 1
    assert rooms.get(1).number == "101"


def test_idで部屋を取得する():
    rooms = Rooms({1: Room(id=1, number="101"), 2: Room(id=2, number="102")})
    room = rooms.get(id=1)
    assert room.id == 1
    assert room.number == "101"

# def test_部屋に紐づいた契約を取得する():
#     rooms = Rooms()
#     rooms.add(Room(id=1, number="101"))
#     contract = Contract(id=1, room_id=1, details="Test Contract")
#     contracts = rooms..get_contracts()  # Assuming this method exists