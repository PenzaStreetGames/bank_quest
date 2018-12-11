import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QWidget
import room

class Quest:

    def __init__(self, name):
        self.player = name
        self.rooms = {}
        self.ways = {}
        room_names, room_text, ways = self.load_data()
        images = ""
        for i in range(len(room_names)):
            room = Room(room_names[str(i)], room_text[str(i)],
                        images[str[i]], i)
            self.rooms[str(i)] = room
        way_items = ways.items()
        for i in range(len(ways)):
            room_from, room_into = way_items[i][0].split()

        self.buttons = [canvas.choose_1, canvas.choose_2,
                        canvas.choose_3, canvas.choose_4]

    def change_room(self, index):
        pass


class Room:

    def __init__(self, name, text, image, index):
        self.name = name
        self.text = text
        self.image = image
        self.index = index


class Hall:

    def __init__(self, room_from, room_to, condition, index):
        self.room_from = room_from
        self.room_to = room_to
        self.condition = condition
        self.value = False

    def check_condition(self):

        self.value = eval(self.condition)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.plain = QPlainTextEdit(self)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())