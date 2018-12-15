import sys
from pygame import mixer
from PyQt5.QtCore import QSize, QStringListModel
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QPlainTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QWidget, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.Qt import QHBoxLayout, QSpacerItem, QSizePolicy
from json import loads, dumps
import time
import datetime
from tests import Tester


class SceneInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bg = QLabel(self)
        self.bg.move(0, 0)
        self.bg.setPixmap(QPixmap("bg.jpg"))
        self.bg.resize(800, 560)

        self.exit = QPushButton('Выход', self)
        self.exit.resize(105, 40)
        self.exit.move(675, 510)
        self.exit.setFont(QFont("PSG Font", 11))
        self.exit.clicked.connect(self.close)

        self.restart = QPushButton('Рестарт', self)
        self.restart.resize(110, 40)
        self.restart.move(560, 510)
        self.restart.setFont(QFont("PSG Font", 11))

        self.opnsave = QPushButton('Загрузить', self)
        self.opnsave.resize(105, 40)
        self.opnsave.move(135, 510)
        self.opnsave.setFont(QFont("PSG Font", 11))
        # self.opnsave.clicked.connect(self.opensave)

        self.savebtn = QPushButton('Сохранить', self)
        self.savebtn.resize(110, 40)
        self.savebtn.move(20, 510)
        self.savebtn.setFont(QFont("PSG Font", 11))
        # self.opnsave.clicked.connect(self.save)


        self.text = QPlainTextEdit(self)
        self.text.move(20, 20)
        self.text.resize(530, 270)
        self.text.setReadOnly(True)
        self.text.setFont(QFont("PSG Font", 11))
        self.text.setStyleSheet("background: rgba(255, 255, 255, 0.9);")

        self.player_data = QPlainTextEdit(self)
        self.player_data.move(560, 300)
        self.player_data.resize(220, 175)
        self.player_data.setReadOnly(True)
        self.player_data.setFont(QFont("PSG Font", 10))
        self.player_data.setStyleSheet("background: rgba(238, 238, 238, 0.97);\
                                        border:none;")

        self.name_player = QLineEdit(self)
        self.name_player.setPlaceholderText("Введите имя...")
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

    def get_name_user(self):
        return self.name_player.text()

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

    def update(self, name="", text="", user="", image="", pldata="", buttons=[], user_disabled=True):
        self.initNameScene(name)
        self.initText(text)
        self.initButtons(buttons)
        self.initNamePlayer(user)
        self.initImage(image)
        self.initPlayerData(pldata)
        self.setNameUserMode(user_disabled)


    def submitted(self, variant):
        ways = quest.data["ways"]
        name = self.get_name_user()
        for key, value in ways.items():
            if value == variant:
                if key == "1 4" and not name:
                    QMessageBox.about(self, "Ошибка!", "Введите пожалуйста имя.")
                    return
                quest.user_move(key)
                self.name_player.setText(name)


class Quest:

    def __init__(self):
        self.game_time = 0
        self.player = ""
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

    def create_rooms(self):
        self.rooms = {}
        room_names, room_text = (self.data["room_names"],
                                 self.data["room_text"])
        for i in range(len(room_names)):
            room = Room(room_names[str(i)], room_text[str(i)],
                        "img.jmg", i)
            self.rooms[str(i)] = room

    def user_move(self, way):
        self.eventlistener(self.ways[way].room_to.index)
        print(self.ways[way].room_to.index)
        if way == "1 4":
            self.player = ex.name_player.text()
        elif way == "1 0":
            ex.close()
        elif way.endswith(" 1"):
            self.default_properties()
            self.save()
        elif way == "10 12":
            self.properties["john_percent"] = 1
        elif way == "10 11":
            self.properties["john_percent"] = 2
        elif way == "15 16":
            self.properties["emmet_percent"] = 1
        elif way == "15 17":
            self.properties["emmet_percent"] = 2
        elif way == "24 25":
            self.properties["smith_percent"] = 1
        elif way == "24 26":
            self.properties["smith_percent"] = 2
        elif way == "20 21":
            self.properties["alcohol"] = 1
        elif way == "20 22":
            self.properties["alcohol"] = 2
        elif way == "20 23":
            self.properties["alcohol"] = 3
        elif way == "10 13":
            self.properties["emmet_know"] = True
        elif way == "15 18":
            self.properties["smith_know"] = True
        elif way == "5 27":
            self.properties["rob_begin"] = True
        elif way == "40 20":
            self.properties["james_meet"] = 1
        elif way == "42 14":
            self.properties["james_meet"] = 2
        room_into = self.ways[way].room_to.index
        self.change_room(str(room_into))

    def eventlistener(self, scene):
        print(scene)
        if scene == 1:
            self.game_time = 0
        elif scene == 4:
            self.game_time = time.time()

    def save(self):
        self.properties["time"] = self.game_time = time.time() - self.game_time
        with open("saves/{}.json".format(ex.get_name_user()), mode="w", encoding="utf-8") as file:
            file.write(dumps(self.properties) + "\n")

    def load(self):
        self.properties = loads(open("{}".format(ex.get_name_user()), "r", encoding="utf-8").read())

    def change_room(self, index):
        if index == "0":
            ex.close()
        self.current_room = self.rooms[index]
        self.update_room()

    def update_room(self):
        room = self.current_room
        buttons = list(map(lambda hall: hall.text, self.find_active_ways()))
        if int(self.current_room.index) > 4:
            self.check_state()
        state = "\n".join(self.state)
        ex.update(text=room.text, buttons=buttons, pldata=state, image="img.jpg",
                  user_disabled=False if self.current_room.index == 1 else True)

    def default_properties(self):
        self.data = loads(open("bq_data.json", "r", encoding="utf-8").read())
        self.properties = self.data["flags"]
        self.state = []

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
                if (way.name == "5 27" and
                        self.properties["smith_percent"] == 0):
                    pass
                elif (way.name == "7 14" and
                      not self.properties["emmet_know"]):
                    pass
                elif (way.name == "8 20" and
                      not self.properties["smith_know"]):
                    pass
                elif (way.name == "10 13" and
                      (self.properties["john_percent"] == 0 or
                       self.properties["emmet_know"])):
                    pass
                elif (way.name == "10 11" and
                      self.properties["john_percent"] != 0):
                    pass
                elif (way.name == "10 12" and
                      self.properties["john_percent"] != 0):
                    pass
                elif (way.name == "15 18" and
                      (self.properties["emmet_percent"] == 0 or
                       self.properties["smith_know"])):
                    pass
                elif (way.name == "15 16" and
                      self.properties["emmet_percent"] != 0):
                    pass
                elif (way.name == "15 17" and
                      self.properties["emmet_percent"] != 0):
                    pass
                elif (way.name == "24 25" and
                      self.properties["smith_percent"] != 0):
                    pass
                elif (way.name == "24 26" and
                      self.properties["smith_percent"] != 0):
                    pass
                elif (way.name == "20 21" and
                      self.properties["alcohol"] != 0):
                    pass
                elif (way.name == "20 22" and
                      self.properties["alcohol"] != 1):
                    pass
                elif (way.name == "20 23" and
                      self.properties["alcohol"] != 2):
                    pass
                elif (way.name == "28 29" and
                      self.properties["smith_percent"] != 1):
                    pass
                elif (way.name == "28 30" and
                      self.properties["smith_percent"] != 2):
                    pass
                elif (way.name == "33 34" and
                      self.properties["emmet_percent"] != 1):
                    pass
                elif (way.name == "33 35" and
                      self.properties["emmet_percent"] != 2):
                    pass
                elif (way.name == "35 36" and
                      self.properties["john_percent"] != 1):
                    pass
                elif (way.name == "35 38" and
                      self.properties["john_percent"] != 2):
                    pass
                elif (way.name == "20 40" and
                      self.properties["james_meet"] != 0):
                    pass
                elif (way.name == "27 44" and
                      self.properties["james_meet"] != 2):
                    pass
                elif (way.name == "33 46" and
                      self.properties["james_meet"] != 2):
                    pass
                else:
                    active_ways += [way]
        return active_ways

    def check_state(self):
        self.state = []
        self.state += [self.data["states"]["current_task"]]
        if self.properties["john_percent"] == 0:
            self.state += [self.data["states"]["go_to_john"]]
        elif not self.properties["emmet_know"]:
            self.state += [self.data["states"]["ask_about_emmet"]]
        elif self.properties["emmet_percent"] == 0:
            self.state += [self.data["states"]["go_to_emmet"]]
        elif not self.properties["smith_know"]:
            self.state += [self.data["states"]["ask_about_smith"]]
        elif self.properties["smith_percent"] == 0:
            self.state += [self.data["states"]["go_to_smith"]]
        elif not self.properties["rob_begin"]:
            self.state += [self.data["states"]["go_to_home"]]
        else:
            self.state += [self.data["states"]["rob_a_bank"]]
        self.state[-1] += "\n"
        if self.properties["james_meet"] == 2:
            self.state += [self.data["states"]["sewage_plan"]]
        if self.properties["alcohol"] == 1:
            self.state += [self.data["states"]["some_alcohol"]]
        elif self.properties["alcohol"] == 2:
            self.state += [self.data["states"]["much_alcohol"]]
        elif self.properties["alcohol"] == 3:
            self.state += [self.data["states"]["too_much_alcohol"]]
        if self.properties["john_percent"] != 0:
            self.state += [self.data["states"]["john_in_band"]]
        if self.properties["john_percent"] == 1:
            self.state += [self.data["states"]["small_percent"]]
        elif self.properties["john_percent"] == 2:
            self.state += [self.data["states"]["big_percent"]]
        if self.properties["emmet_percent"] != 0:
            self.state += [self.data["states"]["emmet_in_band"]]
        if self.properties["emmet_percent"] == 1:
            self.state += [self.data["states"]["small_percent"]]
        elif self.properties["emmet_percent"] == 2:
            self.state += [self.data["states"]["big_percent"]]
        if self.properties["smith_percent"] != 0:
            self.state += [self.data["states"]["smith_in_band"]]
        if self.properties["smith_percent"] == 1:
            self.state += [self.data["states"]["small_percent"]]
        elif self.properties["smith_percent"] == 2:
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
ex.setFixedSize(800, 560)

mixer.init()
mixer.music.load('Quest Theme.mp3')
mixer.music.play(-1)

ex.show()

quest = Quest()
quest.change_room("1")


# t = Tester(quest.data)
# t.test_isset_scene(200)

sys.exit(app.exec())
