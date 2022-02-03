import requests
import sys
import os
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.metki = 1
        self.metka = '&pt='
        self.x = 100  # Координаты центра карты на старте
        self.y = 100  # Координаты центра карты на старте
        self.zoom = 10  # Мастштаб
        self.type_map = 'map'  # Тип карты
        self.setGeometry(300, 300, 900, 700)
        self.setWindowTitle('Панель управления')

        self.ch_type1 = QPushButton(self)
        self.ch_type1.setText('map')
        self.ch_type1.resize(100, 30)
        self.ch_type1.move(600, 360)
        self.ch_type1.clicked.connect(self.type_changed)

        self.ch_type2 = QPushButton(self)
        self.ch_type2.setText('sat')
        self.ch_type2.resize(100, 30)
        self.ch_type2.move(600, 390)
        self.ch_type2.clicked.connect(self.type_changed)

        self.ch_type3 = QPushButton(self)
        self.ch_type3.setText('sat,skl')
        self.ch_type3.resize(100, 30)
        self.ch_type3.move(600, 420)
        self.ch_type3.clicked.connect(self.type_changed)

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

        self.btn_2 = QPushButton('V', self)
        self.btn_2.resize(250, 50)
        self.btn_2.move(600, 75)
        self.btn_2.clicked.connect(self.find)

        self.out4 = QLineEdit(self)
        self.out4.resize(115, 30)
        self.out4.move(600, 150)
        self.out4.setPlaceholderText('Координата 1')

        self.out5 = QLineEdit(self)
        self.out5.resize(115, 30)
        self.out5.move(730, 150)
        self.out5.setPlaceholderText('Координата 2')

        self.out3 = QLineEdit(self)
        self.out3.resize(250, 30)
        self.out3.move(600, 25)
        self.out3.setPlaceholderText('Поиск по названию')

        self.btn_3 = QPushButton('Сброс точек', self)
        self.btn_3.resize(250, 50)
        self.btn_3.move(600, 200)
        self.btn_3.clicked.connect(self.del_point)

    def to_ll(self):
        return "{0},{1}".format(self.x, self.y)

    def type_changed(self):
        print(self.sender().text())
        self.type_map = self.sender().text()
        self.clic()

    def clic(self):
        try:
            cor_x = float(self.out1.text())
            cor_y = float(self.out2.text())
            self.getImage(cor_x, cor_y)
        except:
            pass

    def clic2(self):
        try:
            self.getImage(self.x, self.y)
        except:
            pass

    def getImage(self, cor_x, cor_y):
        self.x = cor_x
        self.y = cor_y
        map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=self.to_ll(),
                                                                                        z=self.zoom,
                                                                                        type=self.type_map)
        if len(self.metka) > 4:
            map_request += self.metka
        response = requests.get(map_request)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pix = QPixmap('map.png')
        self.pix = self.pix.scaled(500, 500)
        self.res_map.setPixmap(self.pix)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp and self.zoom < 16:
            self.zoom += 1
            self.clic2()
        if event.key() == Qt.Key_PageDown and self.zoom > 2:
            self.zoom -= 1
            self.clic2()
        if event.key() == Qt.Key_A:
            self.x -= 0.005 * 2 ** (15 - self.zoom)
            self.clic2()
        if event.key() == Qt.Key_D:
            self.x += 0.005 * 2 ** (15 - self.zoom)
            self.clic2()
        if (event.key() == Qt.Key_W) and self.y < 90:
            self.y += 0.005 * 2 ** (15 - self.zoom)
            self.clic2()
        if (event.key() == Qt.Key_S) and self.y > -90:
            self.y -= 0.005 * 2 ** (15 - self.zoom)
            self.clic2()

        if self.x > 180:
            self.x -= 360
        if self.y < -180:
            self.y += 360

    def find(self):
        text = '+'.join(str(self.out3.text()).split())
        geocoder_requests = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + text + "&format=json"
        response = requests.get(geocoder_requests)
        if response:
            json_response = response.json()
            self.out4.setText((json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                'Point']['pos']).split()[0])
            self.out5.setText((json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                'Point']['pos']).split()[1])
            tt = '~' + str(self.out4.text()) + ',' + str(self.out5.text()) + ',pmrdm' + str(self.metki)
            if len(self.metka) > 4:
                self.metka += '~' + str(self.out4.text()) + ',' + str(self.out5.text()) + ',pmrdm' + str(self.metki)
            else:
                self.metka += str(self.out4.text()) + ',' + str(self.out5.text()) + ',pmrdm' + str(self.metki)
            self.metki += 1
        self.clic2()
            

    def del_point(self):
        self.metki = 1
        self.metka = '&pt='
        self.clic2()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
