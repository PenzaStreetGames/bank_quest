import sys
from os import walk, getcwd
from pygame import mixer
from PyQt5.QtWidgets import (QApplication, QPushButton, QLabel, QPlainTextEdit,
                             QVBoxLayout)
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.Qt import QHBoxLayout, QSpacerItem, QSizePolicy
from json import loads, dumps
import time
from random import random


class SceneInterface(QMainWindow):
    """Класс интерфейса квеста"""
    def __init__(self):
        """Инициализация интерфейса"""
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
        self.restart.clicked.connect(self.restart_quest)

        self.opnsave = QPushButton('Загрузить', self)
        self.opnsave.resize(105, 40)
        self.opnsave.move(135, 510)
        self.opnsave.setFont(QFont("PSG Font", 11))
        self.opnsave.clicked.connect(self.load_quest)

        self.savebtn = QPushButton('Сохранить', self)
        self.savebtn.resize(110, 40)
        self.savebtn.move(20, 510)
        self.savebtn.setFont(QFont("PSG Font", 11))
        self.savebtn.clicked.connect(self.save_quest)

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
        self.player_data.setFont(QFont("PSG Font", 11))
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
        self.btn_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(self.btn_layout)

        self.buttons = []
        for btn in range(4):
            button = QPushButton("", self)
            button.resize(530, 40)
            button.setFont(QFont("PSG Font", 11))
            button.setStyleSheet("background: rgba(236, 236, 236, 0.7);")
            button.move(20, (45 * btn) + 300)
            button.clicked.connect(self.get_key_button_submited)
            self.btn_layout.addWidget(button)
            self.buttons += [button]

    def get_name_user(self):
        """Возвращает имя игрока"""
        return self.name_player.text()

    def init_buttons(self, names):
        """Иницилизация кнопок"""
        while len(names) < 4:
            names += [""]
        for i in range(4):
            self.buttons[i].setText(names[i])
            if names[i]:
                self.buttons[i].setEnabled(True)
                self.buttons[i].setStyleSheet(
                    "background: rgba(236, 236, 236, 0.7);")
            else:
                self.buttons[i].setEnabled(False)
                self.buttons[i].setStyleSheet(
                    "background: rgba(236, 236, 236, 0);")

    def init_text(self, text):
        """Иницилизация текста на текущей сцене"""
        self.text.setPlainText(text)

    def init_image(self, image):
        """Иницилизация картинки сцены"""
        self.img.setPixmap(QPixmap(image))

    def init_player_data(self, data):
        """Иницилизация характеристики игрока"""
        self.player_data.setPlainText(data)

    def init_name_scene(self, name):
        """Иницилизация имени сцены"""
        self.setWindowTitle(name)

    def init_name_player(self, name):
        """Иницилизация имени игрока"""
        self.name_player.setText(name)

    def set_name_user_mode(self, mode):
        """Иницилизация редактируемости поля имени игрока"""
        self.name_player.setReadOnly(mode)

    def get_key_button_submited(self):
        """Какую из кнопок нажали"""
        self.submitted(self.sender().text())

    def update(self, name="", text="", user="", image="", pldata="", buttons=[],
               user_disabled=True):
        """Обновление сцены"""
        self.init_name_scene(name)
        self.init_text(text)
        self.init_buttons(buttons)
        self.init_name_player(user)
        self.init_image(image)
        self.init_player_data(pldata)
        self.set_name_user_mode(user_disabled)

    def submitted(self, variant):
        """Обработка нажатия на кнопки"""
        ways = quest.data["ways"]
        name = self.get_name_user()
        for key, value in ways.items():
            if value == variant:
                if key == "1 4" and not name:
                    QMessageBox.about(self, "Ошибка!",
                                      "Введите пожалуйста имя.")
                    return
                quest.user_move(key)
                self.name_player.setText(name)

    def restart_quest(self):
        """Вызов рестарта у квеста"""
        quest.restart()

    def save_quest(self):
        """Сохранение квеста"""
        quest.save()

    def load_quest(self):
        """Загрузка квеста"""
        quest.load()


class Quest:
    """Класс системы комнат, переходов, и взамодействия между ними."""
    def __init__(self):
        """Инициализация квеста"""
        self.properties = {}
        self.state = []
        self.rooms = {}
        self.ways = {}
        self.users = {}
        self.highscores = ""
        self.data = {}
        self.data = loads(open("bq_data.json", "r", encoding="utf-8").read())

        self.menu_rooms = self.data["menu_rooms"]
        self.create_rooms()
        self.current_room = self.rooms["1"]
        self.create_ways()
        self.default_properties()

    def create_rooms(self):
        """Создаёт объекты класса Room и записывает их в словарь квеста"""
        self.rooms = {}
        room_names, room_text, room_images = (self.data["room_names"],
                                              self.data["room_text"],
                                              self.data["room_images"])
        for i in range(len(room_names)):
            room = Room(room_names[str(i)], room_text[str(i)],
                        room_images[str(i)], i)
            self.rooms[str(i)] = room

    def user_move(self, way):
        """Вычисляет возможные изменения при переходе из одной комнаты
        в другую"""
        print(self.ways[way].room_to.index)
        value = random()
        other_room = ""
        if (value < self.data["chances"]["random_die"] and
                str(self.current_room.index) not in self.menu_rooms):
            other_room = "51"
        if way == "1 4":
            self.properties["player"] = ex.get_name_user()
            self.properties["time"] = time.time()
            ex.update(user_disabled=True)
        elif way == "1 0":
            ex.close()
        elif way.endswith(" 1") and way.split()[0] not in self.menu_rooms:
            self.save()
            self.default_properties()
        elif way == "1 3":
            self.load_saves()
        elif way == "3 52":
            self.sort_by_name()
            other_room = 3
        elif way == "3 53":
            self.sort_by_time()
            other_room = 3
        elif way == "3 54":
            self.sort_by_score()
            other_room = 3
        elif way == "10 12":
            self.properties["john_percent"] = 1
        elif way == "10 11":
            self.properties["john_percent"] = 2
        elif way == "14 15":
            if value < self.data["chances"]["dump_stay"]:
                other_room = "14"
        elif way == "14 7":
            if value < self.data["chances"]["dump_stay"]:
                other_room = "14"
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
        elif way == "27 43":
            self.properties["entry"] = "wall"
            if (self.data["chances"]["boom_shot"][0] < value
                    < self.data["chances"]["boom_shot"][1]):
                other_room = "49"
            elif (self.data["chances"]["boom_die"][0] < value
                  < self.data["chances"]["boom_die"][1]):
                other_room = "50"
        elif way == "27 44":
            self.properties["entry"] = "sewage"
        elif way == "30 33":
            self.properties["door"] = "boom"
            if (self.data["chances"]["boom_shot"][0] < value
                 < self.data["chances"]["boom_shot"][1]):
                other_room = "49"
            elif (self.data["chances"]["boom_die"][0] < value
                  < self.data["chances"]["boom_die"][1]):
                other_room = "50"
        elif way == "31 33":
            self.properties["door"] = "puzzle"
        elif way == "33 45":
            self.properties["exit"] = "town"
        elif way == "33 46":
            self.properties["exit"] = "sewage"
        elif way == "35 38":
            self.calculate_money()
        if other_room == "":
            room_into = self.ways[way].room_to.index
        else:
            room_into = other_room
        self.change_room(str(room_into))

    def save(self):
        self.properties["time"] = time.time() - self.properties["time"]
        self.properties["current_room"] = str(self.current_room.index)
        self.write_ending()
        with open("saves/{}.json".format(ex.get_name_user()), mode="w",
                  encoding="utf-8") as file:
            file.write(dumps(self.properties) + "\n")

    def load(self):
        try:
            self.properties = loads(
                open("saves/{}.json".format(ex.get_name_user()), "r",
                     encoding="utf-8").read())
            self.change_room(self.properties["current_room"])
        except Exception:
            pass

    def write_ending(self):
        """Определяет концовку игрока"""
        room = str(self.current_room.index)
        if room == "23":
            self.properties["end"] = "too_many_drink"
        elif room == "39":
            self.properties["end"] = "no_play"
        elif room == "49":
            self.properties["end"] = "boom_shot"
        elif room == "50":
            self.properties["end"] = "boom_die"
        elif room == "51":
            self.properties["end"] = "random_die"
        elif room == "29":
            self.properties["end"] = "bad_explosive"
        elif room == "34":
            self.properties["end"] = "bad_weapon"
        elif room == "36":
            self.properties["end"] = "john_kill"
        elif room == "37":
            self.properties["end"] = "band_kill"
        elif room == "32" or room == "47" or room == "48":
            self.properties["end"] = "wrong_answer"
        elif room == "38":
            self.properties["end"] = "complete_rob"
        else:
            self.properties["end"] = "in_process"

    def change_room(self, index):
        """Изменяет текущую комнату"""
        if index == "0":
            ex.close()
        elif index == "3":
            self.highscores = self.show_highscores()
        self.current_room = self.rooms[index]
        self.update_room()

    def update_room(self):
        """Обновляет комнату при переходе, меняя отображение интерфейса"""
        room = self.current_room
        buttons = list(map(lambda hall: hall.text, self.find_active_ways()))
        self.check_state()
        state = "\n".join(self.state)
        text = room.text
        if "{name}" in text:
            text = text.replace("{name}", self.properties["player"])
        if "{money}" in text:
            text = text.replace("{money}", str(self.properties["money"]))
        if str(room.index) == "3":
            text = self.highscores
        ex.update(text=text, buttons=buttons, pldata=state, image=room.image,
                  user_disabled=False if str(self.current_room.index)
                  in self.menu_rooms else True)
        ex.name_player.setText(self.properties["player"])

    def default_properties(self):
        """Устанавливает все настройки пользователя в значение по умолчанию"""
        self.data = loads(open("bq_data.json", "r", encoding="utf-8").read())
        self.properties = self.data["flags"]
        self.state = []

    def create_ways(self):
        """Создаёт объекты класса Hall и записывает их в словарь квеста"""
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
        """Определяет доступные в данной комнате в данный момент переходы"""
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
        """Составляет текст о текущем состоянии игрока и игровых событиях"""
        self.state = []
        if str(self.current_room.index) in self.menu_rooms:
            print(self.current_room.index)
            return
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

    def restart(self):
        """Возвращает игрока в начало квеста, обнуляя игровые события"""
        if str(self.current_room.index) not in self.menu_rooms:
            name = self.properties["player"]
            self.default_properties()
            self.properties["player"] = name
            self.change_room("4")

    def calculate_money(self):
        """Рассчитывает итоговый заработок игрока"""
        money = 1000000
        if self.properties["entry"] == "wall":
            money *= 0.8
        if self.properties["door"] == "boom":
            money *= 0.8
        if self.properties["exit"] == "town":
            money *= 0.8
        total = money
        if self.properties["john_percent"] == 2:
            money -= total * 0.2
        elif self.properties["john_percent"] == 1:
            money -= total * 0.07
        if self.properties["emmet_percent"] == 2:
            money -= total * 0.2
        elif self.properties["emmet_percent"] == 1:
            money -= total * 0.07
        if self.properties["smith_percent"] == 2:
            money -= total * 0.2
        elif self.properties["smith_percent"] == 1:
            money -= total * 0.07
        self.properties["money"] = money

    def load_saves(self):
        """Возвращает все сохранения, загруженные в словари из файлов"""
        saves = []
        for root, dirs, files in walk(getcwd() + "/saves"):
            saves = files
        users = []
        for save in saves:
            users += [loads(open(f"saves/{save}", "r",
                                 encoding="utf-8").read())]
        self.users = {}
        for user in users:
            self.users[user["player"]] = Highscore(user)

    def show_highscores(self):
        """Возвращает сохранения игроков в читаемом виде"""
        text = []
        for user in self.users.values():
            player = []
            player += [f"{user.data['player']}:"]
            player += [f"    {self.data['endings'][user.data['end']]}"]
            player += [f"    Время прохождения: {int(user.data['time'])} секунд"]
            player += [f"    Награбил {user.data['money']} долларов"]
            player = "\n".join(player)
            text += [player]
        text = "\n".join(text)
        return text

    def sort_by_name(self):
        """Сортирует рекорды по имени игрока"""
        users = self.users.items()
        users = list(sorted(users, key=lambda user: user[1].data["player"]))
        users = dict(users)
        self.users = users.copy()

    def sort_by_time(self):
        """Сортирует рекорды по времени прохождения"""
        users = self.users.items()
        users = list(sorted(users, key=lambda user: user[1].data["time"]))
        users = dict(users)
        self.users = users.copy()

    def sort_by_score(self):
        """Сортирует рекорды по награбленным деньгам"""
        users = self.users.items()
        users = list(sorted(users, key=lambda user: user[1].data["money"],
                            reverse=True))
        users = dict(users)
        self.users = users.copy()


class Room:
    """Класс комнаты - места, описывающего текущее положение игрока"""
    def __init__(self, name, text, image, index):
        """Инициализация комнаты"""
        self.name = name
        self.text = text
        self.image = image
        self.index = index


class Hall:
    """Класс перехода - связи между двумя комнатами, доступной пользователю"""
    def __init__(self, name, room_from, room_to, text):
        """Описание перехода"""
        self.room_from = room_from
        self.room_to = room_to
        self.name = name
        self.text = text


class Highscore:
    """Класс информации о игроке в рекордах"""
    def __init__(self, data):
        """Инициализация рекорда"""
        self.data = data.copy()


class Tester:
    """Класс тестирующий систему квеста"""
    def __init__(self, data):
        """Инициализация тестировщика"""
        self.ways = data["ways"]
        self.room_names = data["room_names"]
        self.room_text = data["room_text"]

    def test_ways_room_have_exit(self):
        """Каждая комната имеет выход"""
        rooms = self.room_names.copy()
        fr = set(way.split()[0] for way in self.ways)
        for room in rooms:
            if int(room):
                assert room in fr

    def test_ways_room_have_entry(self):
        """Каждая комната имеет вход"""
        rooms = self.room_names.copy()
        to = set(way.split()[1] for way in self.ways)
        for room in rooms:
            if int(room):
                assert room in to

    def test_ways_room_have_connect(self):
        """Каждая комната имеет вход и выход"""
        rooms = self.room_names.copy()
        fr = set(way.split()[0] for way in self.ways)
        to = set(way.split()[1] for way in self.ways)
        for room in rooms:
            if int(room):
                assert room in fr and room in to

    def test_isset_scene(self, scene_index):
        """Вспомогательная функция"""
        assert str(scene_index) in self.room_names.keys()

    def test_all_rooms_in_ways_isset(self):
        """Все комнаты, указанные в путях, существуют"""
        fr, to = [], []
        for way in self.ways:
            fr.append(way.split()[0])
            to.append(way.split()[1])
        all = fr + to
        for room in all:
            self.test_isset_scene(room)

    def test_isset_scene_name(self):
        """Есть ли имя у сцены"""
        for code in self.room_names:
             assert self.room_names[code]


    def test_isset_description_scene(self):
        """Есть ли описание у сцены"""
        for code in self.room_text:
             assert self.room_text[code]

    def test_count_scenes(self):
        """Совпадают количества описаний сцен"""
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


app = QApplication(sys.argv)
ex = SceneInterface()
ex.setFixedSize(800, 560)

mixer.init()
mixer.music.load('Quest Theme.mp3')
mixer.music.play(-1)

ex.show()

quest = Quest()
quest.change_room("1")

test = Tester(quest.data)
try:
    test.test_ways_room_have_exit()
    test.test_ways_room_have_entry()
    test.test_ways_room_have_connect()
    test.test_all_rooms_in_ways_isset()
    test.test_isset_scene_name()
    test.test_isset_description_scene()
    test.test_count_scenes()
    print("Тесты пройдены успешно")
except AssertionError:
    print("Не все тесты пройдены успешно")

sys.exit(app.exec())