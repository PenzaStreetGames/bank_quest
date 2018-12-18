#in_rooms = list(map(way.split()[0] for way in self.ways))


def test_ways_room_have_exits(self):
    """Каждая комната не имеет вход и выход"""
    fr, to = [], []
    for way in self.ways:
        fr.append(way.split()[0])
        to.append(way.split()[0])

    for element in fr and to:
        if int(element):
            assert element in fr and to