class Tester:

    def __init__(self, data):
        self.ways = data["ways"]
        self.room_names = data["room_names"]
        self.room_text = data["room_text"]

    def test_ways(self):
        fr, to = [], []
        for way in self.ways:
            fr.append(way.split()[0])
            to.append(way.split()[1])
        for element in to:
            if int(element):
                assert element in fr

    def test_isset_scene(self):
        for code in self.room_names:
             assert self.room_names[code]


    def test_isset_description_scene(self):
        for code in self.room_text:
             assert self.room_text[code]

    def test_count_scenes(self):
        rooms_names = []
        for code in self.room_names:
            rooms_names.append(code)
        room_text = []
        for code in self.room_text:
            room_text.append(code)
        assert len(rooms_names) == len(room_text)
        room_text = list(map(int, room_text))
        rooms_names = list(map(int, rooms_names))
        rooms_names.sort()
        room_text.sort()
        assert rooms_names == room_text
