import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QWidget
#from bq_data import

class Quest:

    def __init__(self, name):

        self.player = name
        self.rooms = []
        self.buttons = [canvas.choose_1, canvas.choose_2,
                        canvas.choose_3, canvas.choose_4]

    def change_room(self, index):
        pass


class Room:

    def __init__(self, name, text, image, halls):

        self.name = name
        self.text = text
        self.image = image
        self.halls = halls.copy()


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
