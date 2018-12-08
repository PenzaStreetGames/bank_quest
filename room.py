import sys

from PyQt5.QtCore import QSize, QStringListModel
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QPlainTextEdit, QVBoxLayout, QTableWidget, QWidget, QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.Qt import QHBoxLayout, QSpacerItem, QSizePolicy


class Buttons(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.btn1 = QPushButton("Button 1")
        self.btn2 = QPushButton("Button 2")
        self.btn3 = QPushButton("Button 3")

        self.btn_layout.addWidget(self.btn1)
        self.btn_layout.addWidget(self.btn2)
        self.btn_layout.addWidget(self.btn3)

        self.layout.addLayout(self.btn_layout)


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
        self.text.setPlaceholderText("asdf")

        self.player_data = QPlainTextEdit(self)
        self.player_data.move(540, 240)
        self.player_data.resize(240, 190)
        self.player_data.setPlaceholderText("asdf")

        self.name_player = QLineEdit(self)
        self.name_player.resize(240, 30)
        self.name_player.move(540, 205)

        self.label = QLabel(self)
        self.label.setText("Картинка")
        self.label.resize(200, 160)
        self.label.move(700, 30)

        self.layout = QVBoxLayout(self)

        self.btn_layout = QHBoxLayout(self)
        self.btn_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.choose = [QPushButton("Вариант 1", self), QPushButton("Вариант 2", self), QPushButton("Вариант 3", self)]
        for btn in range(len(self.choose)):
            self.btn_layout.addWidget(self.choose[btn])
            self.choose[btn].move(20, (45 * btn) + 300)
            self.choose[btn].resize(510, 40)

        self.layout.addLayout(self.btn_layout)




app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())

