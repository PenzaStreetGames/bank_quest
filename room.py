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

    def initButtons(self, names):
        for btn in range(len(names)):
            button = QPushButton(names[btn], self)
            button.move(20, (45 * btn) + 300)
            button.resize(530, 40)
            button.setFont(QFont("PSG Font", 11))
            button.setStyleSheet("background: rgba(236, 236, 236, 0.7);")
            button.clicked.connect(self.getKeyButtonSubmited)
            self.btn_layout.addWidget(button)

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
        submitted(self.sender().text())

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())


    def update(self, name="", text="", user="", image="", pldata="", buttons=[], user_disabled=True):
        self.initNameScene(name)
        self.initText(text)
        self.initButtons(buttons)
        self.initNamePlayer(user)
        self.initImage(image)
        self.initPlayerData(pldata)
        self.setNameUserMode(user_disabled)


def submitted(variant):
    ways = {"1 2": "Создатели", "1 3": "Помощь", "1 4": "Начать игру", "1 0": "Выход"} # Это как-то должно здесь оказаться
    for key, value in ways.items():
        if value == variant:
            # Здесь вызывается функция f(key), которая подготавливая новые данные обновляет сцену
            return key


app = QApplication(sys.argv)
ex = SceneInterface()
ex.setFixedSize(800, 500)
def a():
    ex.update(name="Scene",
           text="This is simple text forever",
           user="user123",
           image="img.jpg",
           pldata="DataPlayer",
           buttons=["Создатели", "Помощь", "Начать игру", "Выход"],
           user_disabled=False)
    ex.deleteItemsOfLayout(ex.layout)

    ex.update(name="Scene2",
                   text="This is simple text forever2",
                   user="user123",
                   image="img.jpg",
                   pldata="DataPlayer2",
                   buttons=["Создатели", "Помощь"],
                   user_disabled=True)
a()

pygame.mixer.init()
pygame.mixer.music.load('Quest Theme.mp3')
pygame.mixer.music.play(-1)

ex.show()
sys.exit(app.exec_())

