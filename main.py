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
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Карта')

        self.out1 = QLineEdit(self)
        self.out1.resize(250, 30)
        self.out1.move(50, 25)
        self.out1.setPlaceholderText('Координата 1')

        self.out1 = QLineEdit(self)
        self.out1.resize(250, 30)
        self.out1.move(325, 25)
        self.out1.setPlaceholderText('Координата 2')

        self.txt1 = QLabel(self)
        self.txt1.setText('координата 1:')
        self.txt1.move(50, 5)

        self.txt2 = QLabel(self)
        self.txt2.setText('координата 2:')
        self.txt2.move(325, 5)

        self.btn = QPushButton('-->', self)
        self.btn.resize(550, 50)
        self.btn.move(50, 600)
        self.btn.clicked.connect(self.clic)

    def clic(self):
        cor_x = 0
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
