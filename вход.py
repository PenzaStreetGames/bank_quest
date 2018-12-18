#in_rooms = list(map(way.split()[0] for way in self.ways))


def test_ways_room_have_exits(self):
    """Каждая комната имеет вход из неё"""
    fr, to = [], []
    for way in self.ways:
        fr.append(way.split()[1])
        to.append(way.split()[0])

    for element in fr:
        if int(element):
            assert element in to