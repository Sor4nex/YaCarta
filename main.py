import pygame
import requests
import sys
import os
import math
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.a = 0
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 300)
        self.setWindowTitle('Карта')

        self.out1 = QLineEdit(self)
        self.out1.resize(250, 50)
        self.out1.move(25, 25)
        self.out1.setText('Координата 1')

        self.out1 = QLineEdit(self)
        self.out1.resize(250, 50)
        self.out1.move(325, 25)
        self.out1.setText('Координата 2')

        self.btn = QPushButton('-->', self)
        self.btn.resize(500, 100)
        self.btn.move(100, 150)
        self.btn.clicked.connect(self.clic)

    def clic(self):
        cor_x = 0
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
