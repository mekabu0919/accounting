from accountant.room import Room, JSONRoom


def test_部屋情報をJSON形式で保存():
    room = Room(id=1, number="101")
    json_data = room.to_json()
    assert json_data == {"id": 1, "number": "101"}


def test_部屋情報をJSON形式から復元():
    json_data: JSONRoom = {"id": 1, "number": "101"}
    room = Room.from_json(json_data)
    assert room.id == 1
    assert room.number == "101"
