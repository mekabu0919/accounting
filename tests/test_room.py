from accountant.room import Room, JSONRoom, Rooms


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
    rooms = Rooms()
    rooms.add(Room(id=1, number="101"))
    rooms.add(Room(id=2, number="102"))
    json_data = rooms.to_json()
    assert json_data == [
        {"id": 1, "number": "101"},
        {"id": 2, "number": "102"},
    ]


def test_部屋のリストをJSON形式から復元():
    json_data: list[JSONRoom] = [
        {"id": 1, "number": "101"},
        {"id": 2, "number": "102"},
    ]
    rooms = Rooms.from_json(json_data)
    assert len(rooms.list) == 2
    assert rooms.list[0].id == 1
    assert rooms.list[0].number == "101"
    assert rooms.list[1].id == 2
    assert rooms.list[1].number == "102"
