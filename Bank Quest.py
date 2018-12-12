import sys
import pygame
from PyQt5.QtCore import QSize, QStringListModel
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QPlainTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QWidget, QLineEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.Qt import QHBoxLayout, QSpacerItem, QSizePolicy
from json import loads


class SceneInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bg = QLabel(self)
        self.bg.move(0, 0)
        self.bg.setPixmap(QPixmap("bg.jpg"))
        self.bg.resize(800, 500)

        self.exit = QPushButton('Выход', self)
        self.exit.resize(105, 40)
        self.exit.move(675, 455)
        self.exit.setFont(QFont("PSG Font", 11))
        self.exit.clicked.connect(self.close)

        self.restart = QPushButton('Рестарт', self)
        self.restart.resize(105, 40)
        self.restart.move(560, 455)
        self.restart.setFont(QFont("PSG Font", 11))

        self.text = QPlainTextEdit(self)
        self.text.move(20, 20)
        self.text.resize(530, 270)
        self.text.setReadOnly(True)
        self.text.setFont(QFont("PSG Font", 10))
        self.text.setStyleSheet("background: rgba(255, 255, 255, 0.9);")

        self.player_data = QPlainTextEdit(self)
        self.player_data.move(560, 300)
        self.player_data.resize(220, 130)
        self.player_data.setReadOnly(True)
        self.player_data.setFont(QFont("PSG Font", 10))
        self.player_data.setStyleSheet("background: rgba(238, 238, 238, 0.97);\
                                        border:none;")

        self.name_player = QLineEdit(self)
        self.name_player.resize(220, 44)
        self.name_player.move(560, 245)
        self.name_player.setFont(QFont("PSG Font", 11))
        self.name_player.setStyleSheet("background: rgba(255, 255, 255, 0.90);\
                                        border:none;\
                                        padding-left: 5px;")

        self.img = QLabel(self)
        self.img.resize(220, 220)
        self.img.move(560, 20)

        self.layout = QVBoxLayout(self)

        self.btn_layout = QHBoxLayout(self)
        self.btn_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(self.btn_layout)

        self.buttons = []
        for btn in range(4):
            button = QPushButton("", self)
            button.resize(530, 40)
            button.setFont(QFont("PSG Font", 11))
            button.setStyleSheet("background: rgba(236, 236, 236, 0.7);")
            button.move(20, (45 * btn) + 300)
            button.clicked.connect(self.getKeyButtonSubmited)
            self.btn_layout.addWidget(button)
            self.buttons += [button]

    def initButtons(self, names):
        while len(names) < 4:
            names += [""]
        for i in range(4):
            self.buttons[i].setText(names[i])
            if names[i]:
                self.buttons[i].setEnabled(True)
                self.buttons[i].setStyleSheet("background: rgba(236, 236, 236, 0.7);")
            else:
                self.buttons[i].setEnabled(False)
                self.buttons[i].setStyleSheet("background: rgba(236, 236, 236, 0);")


    def initText(self, text):
        self.text.setPlainText(text)

    def initImage(self, image):
        self.img.setPixmap(QPixmap(image))

    def initPlayerData(self, data):
        self.player_data.setPlainText(data)

    def initNameScene(self, name):
        self.setWindowTitle(name)

    def initNamePlayer(self, name):
        self.name_player.setText(name)

    def setNameUserMode(self, mode):
        self.name_player.setReadOnly(mode)

    def getKeyButtonSubmited(self):
        self.submitted(self.sender().text())
        print("asdf")

    def update(self, name="", text="", user="", image="", pldata="", buttons=[], user_disabled=True):
        self.initNameScene(name)
        self.initText(text)
        self.initButtons(buttons)
        self.initNamePlayer(user)
        self.initImage(image)
        self.initPlayerData(pldata)
        self.setNameUserMode(user_disabled)


    def submitted(self, variant):
        ways = {"1 2": "Создатели", "1 3": "Помощь", "1 4": "Начать игру", "1 0": "Выход"} # Это как-то должно здесь оказаться
        for key, value in ways.items():
            if value == variant:
                # Здесь вызывается функция f(key), которая подготавливая новые данные обновляет сцену
                self.update(name="Scene2",
                          text="This is simple text forever2",
                          user="user123",
                          image="img.jpg",
                          pldata="DataPlayer2",
                          buttons=["Создатели", "Помощь"],
                          user_disabled=True)
                return key


class Quest:

    def __init__(self, name):
        self.player = name
        self.properties = {}
        self.state = []
        self.rooms = {}
        self.ways = {}
        self.data = {}
        self.data = loads(open("bq_data.json", "r", encoding="utf-8").read())

        self.create_rooms()
        self.current_room = self.rooms["1"]
        self.create_ways()
        self.default_properties()

        buttons = list(map(lambda hall: hall.text, self.find_active_ways()))
        ex.update(buttons=buttons)

        # self.buttons = [canvas.choose_1, canvas.choose_2,
        #                canvas.choose_3, canvas.choose_4]

    def change_room(self, index):
        pass

    def create_rooms(self):
        self.rooms = {}
        room_names, room_text = (self.data["room_names"],
                                 self.data["room_text"])
        for i in range(len(room_names)):
            i = i + 1
            room = Room(room_names[str(i)], room_text[str(i)],
                        "img.jmg", i)
            self.rooms[str(i)] = room

    def change_room(self, name):
        self.current_room = self.rooms[name]

    def default_properties(self):
        self.properties = self.data["flags"]

    def create_ways(self):
        self.ways = {}
        way_items = list(self.data["ways"].items())
        for i in range(len(way_items)):
            way_name = way_items[i][0]
            room_from_name, room_into_name = way_items[i][0].split()
            room_from = self.rooms.get(room_from_name, None)
            room_into = self.rooms.get(room_into_name, None)
            text = way_items[i][1]
            self.ways[way_name] = Hall(way_name, room_from, room_into, text)

    def find_active_ways(self):
        active_ways = []
        for way in self.ways.values():
            if way.room_from.index == self.current_room.index:
                active_ways += [way]
        return active_ways

    def check_state(self):
        self.state = []
        self.state += [self.data["current_task"]]
        if self.properties["john_percent"] == 0:
            self.state += [self.data["states"]["go_to_john"]]
        elif self.properties["emmet_percent"] == 0:
            self.state += [self.data["states"]["go_to_emmet"]]
        elif self.properties["smith_percent"] == 0:
            self.state += [self.data["states"]["go_to_smith"]]
        else:
            self.state += [self.data["states"]["go_to_home"]]
        if self.properties["john_percent"] != 0:
            self.state += [self.data["states"]["john_in_band"]]
        if self.properties["john_percent"] == 1:
            self.state += [self.data["states"]["small_percent"]]
        elif self.propeties["john_percent"] == 2:
            self.state += [self.data["states"]["big_percent"]]
        if self.properties["emmet_percent"] != 0:
            self.state += [self.data["states"]["emmet_in_band"]]
        if self.properties["emmet_percent"] == 1:
            self.state += [self.data["states"]["small_percent"]]
        elif self.propeties["emmet_percent"] == 2:
            self.state += [self.data["states"]["big_percent"]]
        if self.properties["smith_percent"] != 0:
            self.state += [self.data["states"]["smith_in_band"]]
        if self.properties["smith_percent"] == 1:
            self.state += [self.data["states"]["small_percent"]]
        elif self.propeties["smith_percent"] == 2:
            self.state += [self.data["states"]["big_percent"]]


class Room:

    def __init__(self, name, text, image, index):
        self.name = name
        self.text = text
        self.image = image
        self.index = index


class Hall:

    def __init__(self, name, room_from, room_to, text):
        self.room_from = room_from
        self.room_to = room_to
        self.name = name
        self.text = text


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.plain = QPlainTextEdit(self)
        self.show()

app = QApplication(sys.argv)
ex = SceneInterface()
ex.setFixedSize(800, 500)
ex.update(name="Scene",
       text="This is simple text forever",
       user="user123",
       image="img.jpg",
       pldata="DataPlayer",
       buttons=["Создатели", "Помощь", "Начать игру", "Выход"],
       user_disabled=False)

pygame.mixer.init()
pygame.mixer.music.load('Quest Theme.mp3')
pygame.mixer.music.play(-1)

ex.show()

quest = Quest("name")

sys.exit(app.exec())