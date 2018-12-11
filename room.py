import sys
import pygame
from time import sleep
from PyQt5.QtCore import QSize, QStringListModel
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QPlainTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QWidget, QLineEdit
from PyQt5.Qt import QHBoxLayout, QSpacerItem, QSizePolicy

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 500)
        self.setWindowTitle('Комната')

        self.exit = QPushButton('Выход', self)
        self.exit.resize(115, 40)
        self.exit.move(665, 455)

        self.restart = QPushButton('Рестарт', self)
        self.restart.resize(120, 40)
        self.restart.move(540, 455)

        self.text = QPlainTextEdit(self)
        self.text.move(20, 20)
        self.text.resize(510, 270)
        self.text.setReadOnly(True)

        self.player_data = QPlainTextEdit(self)
        self.player_data.move(540, 240)
        self.player_data.resize(240, 190)
        self.player_data.setReadOnly(True)


        self.name_player = QLineEdit(self)
        self.name_player.resize(240, 30)
        self.name_player.move(540, 205)
        self.name_player.setReadOnly(True)

        self.label = QLabel(self)
        self.label.setText("Картинка")
        self.label.resize(200, 160)
        self.label.move(700, 30)

        self.layout = QVBoxLayout(self)

        self.btn_layout = QHBoxLayout(self)
        self.btn_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(self.btn_layout)


    def initButtons(self, names):
        for btn in range(len(names)):
            button = QPushButton(names[btn], self)
            self.btn_layout.addWidget(button)
            button.move(20, (45 * btn) + 300)
            button.resize(510, 40)

    def initText(self, text):
        self.text.setPlainText(text)

    def initImage(self, image):
        pass

    def initPlayerData(self, data):
        self.player_data.setPlainText(data)

    def initNameScene(self, name):
        self.setWindowTitle(name)

    def initNamePlayer(self, name):
        self.name_player.setText(name)

app = QApplication(sys.argv)
ex = MyWidget()

ex.initNameScene("Scene")
ex.initText("This is simple text forever")
ex.initButtons(["Вариант 1", "Вариант 2", "Вариант 3"])
ex.initNamePlayer("user123")
ex.initPlayerData("DataPlayer")

pygame.mixer.init()
pygame.mixer.music.load('Quest Theme.mp3')
pygame.mixer.music.play()

ex.show()
sys.exit(app.exec_())

