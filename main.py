# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QSplashScreen, QPushButton, QLabel
from PyQt5 import QtGui, QtCore
import time
import random
from util import Normalize

from new_lesson_file import NewLesson
from const import *


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Конструктор уроков')
        self.setWindowIcon(QIcon(PATH_SPLASH_SCREEN))
        self.geometry = QDesktopWidget().availableGeometry()

        self.normal = Normalize(self)
        self.background = QLabel(self)

        self.setMinimumSize(self.normal.width_windows * 0.6, self.normal.height_windows * 0.6)
        self.setGeometry(QRect(0, 0, self.normal.width_windows * 0.8, self.normal.height_windows * 0.8))
        """gridLayoutWidget = QWidget(self)
        gridLayoutWidget.setGeometry(QRect(0, 0, self.normal.width_windows * 0.8, self.normal.height_windows * 0.8  ))
        gridLayout = QGridLayout(gridLayoutWidget)
        gridLayout.setContentsMargins(0, 0, 0, 0)"""
        # --------------------------
        #       Кнопки меню
        # --------------------------

        # Кнопка создания нового урока
        self.btn_new_lesson = QPushButton("Новый урок", self)
        self.btn_new_lesson.resize(*self.normal.normal_prop_xy(200, 50))
        self.btn_new_lesson.move(*self.normal.normal_xy(175, 200))
        # 548490 - темный голубой  76b7c7 - светлый голубой
        self.btn_new_lesson.setStyleSheet(
            '.QPushButton {'
            'background-color: #76b7c7;'
            'border-style: outset;'
            'border-width: 2px;'
            'border-radius: 10px;'
            'border-color: beige;'
            'font: bold ' + self.normal.normal_font(14) + 'px;'
                                                          'min-width: 10em;'
                                                          'padding: 6px;'
                                                          '}'
                                                          '.QPushButton:hover {'
                                                          'background-color: #548490;'
                                                          'border-style: inset;'
                                                          '}')

        # Цитата в главном меню
        self.quote = QLabel(random.choice(LIST_LESSON_QUOTE), self)
        self.quote.move(self.normal.width_windows // 3, self.normal.height_windows // 3)
        self.quote.setWordWrap(True)
        self.quote.setStyleSheet('.QLabel {font-family: "Impact";'
                                 'font: ' + self.normal.normal_font(50) + 'px }')
        self.quote.setMinimumSize(self.normal.width_windows // 2, self.normal.height_windows // 4)

        # События на кнопки
        self.btn_new_lesson.clicked.connect(self.create_new_lesson)

        self.main_menu()

    # -----------------------------------------

    def main_menu(self):
        pixmap = QPixmap(PATH_MAIN_MENU)
        self.background.setPixmap(pixmap)
        self.background.resize(self.normal.width_windows, self.normal.height_windows)
        self.background.setScaledContents(True)
        self.btn_new_lesson.show()
        self.quote.show()

    # -----------------------------------------
    def create_new_lesson(self):
        self.quote.hide()
        self.new_lesson = NewLesson(self)

    # -----------------------------------------

    def new_size_object(self):
        self.btn_new_lesson.resize(*self.normal.normal_prop_xy(200, 50))
        self.background.resize(self.normal.width_windows, self.normal.height_windows)

    def new_move_object(self):
        self.btn_new_lesson.move(*self.normal.normal_xy(175, 200))
        self.quote.move(self.normal.width_windows // 3, self.normal.height_windows // 3)


app = QApplication(sys.argv)
ex = Menu()

# Заставка
splash = QSplashScreen(QtGui.QPixmap(PATH_SPLASH_SCREEN).scaled(*ex.normal.normal_prop_xy(1544, 900)),
                       QtCore.Qt.WindowStaysOnTopHint)
splash.show()
time.sleep(1)
splash.close()

ex.show()
sys.exit(app.exec_())
