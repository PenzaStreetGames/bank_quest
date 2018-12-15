import sys
import pygame
from PyQt5.QtCore import QSize, QStringListModel, Qt
from time import sleep
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QPlainTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QWidget, QLineEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.Qt import QHBoxLayout, QSpacerItem, QSizePolicy


class SceneInterface(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bg = QLabel(self)
        self.bg.move(0, 0)
        self.bg.setPixmap(QPixmap("bg.jpg"))
        self.bg.resize(800, 500)

        self.exit = QPushButton('Выход', self)
        self.exit.resize(105, 40)
        self.exit.move(675, 457)
        self.exit.setFont(QFont("PSG Font", 11))
        self.exit.clicked.connect(self.close)

        self.restart = QPushButton('Рестарт', self)
        self.restart.resize(110, 40)
        self.restart.move(560, 457)
        self.restart.setFont(QFont("PSG Font", 11))

        self.opnsave = QPushButton('Открыть', self)
        self.opnsave.resize(105, 40)
        self.opnsave.move(675, 415)
        self.opnsave.setFont(QFont("PSG Font", 11))
        # self.opnsave.clicked.connect(self.opensave)

        self.savebtn = QPushButton('Сохранить', self)
        self.savebtn.resize(110, 40)
        self.savebtn.move(560, 415)
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
        self.player_data.resize(220, 110)
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

    def getNameUser(self):
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
        for key, value in ways.items():
            if value == variant:
                quest.user_move(key)