import requests
import sys
import os
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.Qt import Qt
SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.zoom = 10  # Мастштаб
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Панель управления')

        self.out1 = QLineEdit(self)
        self.out1.resize(250, 30)
        self.out1.move(50, 25)
        self.out1.setPlaceholderText('Координата 1')

        self.out2 = QLineEdit(self)
        self.out2.resize(250, 30)
        self.out2.move(325, 25)
        self.out2.setPlaceholderText('Координата 2')

        self.txt1 = QLabel(self)
        self.txt1.setText('координата 1:')
        self.txt1.move(50, 5)

        self.txt2 = QLabel(self)
        self.txt2.setText('координата 2:')
        self.txt2.move(325, 5)

        self.res_map = QLabel(self)
        self.res_map.resize(500, 500)
        self.res_map.move(50, 60)

        self.btn = QPushButton('-->', self)
        self.btn.resize(550, 50)
        self.btn.move(50, 600)
        self.btn.clicked.connect(self.clic)

    def clic(self):
        try:
            cor_x = float(self.out1.text())
            cor_y = float(self.out2.text())
            self.getImage(cor_x, cor_y)
        except:
            pass

    def getImage(self, cor_x, cor_y):
        map_request = "http://static-maps.yandex.ru/1.x/?ll=" + str(cor_x) + ',' + str(cor_y) + "&spn=20,20&l=sat"
        response = requests.get(map_request)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pix = QPixmap('map.png')
        self.pix = self.pix.scaled(500, 500)
        self.res_map.setPixmap(self.pix)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            pass
        if event.key() == Qt.Key_PageUp:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
