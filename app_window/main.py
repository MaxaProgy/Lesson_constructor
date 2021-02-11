# -*- coding: utf-8 -*-

import sys
import time
import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QDesktopWidget, QLabel, QWidget, QPushButton, \
    QGridLayout, QLineEdit, QTextEdit

from const import *


class Normalize:
    def __init__(self, width, height):
        self.init_width = 1920
        self.init_height = 1080

        self.window_width = width
        self.window_height = height

    def normal_xy(self, x, y):
        return int(self.window_width / self.init_width * x), int(self.window_height / self.init_height * y)

    def normal_proportion(self, x, y):
        return int(self.window_width / self.init_width * x), \
               int(self.window_width / self.init_width * y)

    def normal_font(self, font):
        if self.window_width / self.init_width > self.window_height / self.init_height:
            return str(int(self.window_width / self.init_width * font))
        else:
            return str(int(self.window_height / self.init_height * font))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Конструктор уроков')
        self.setWindowIcon(QIcon(PATH_SPLASH_SCREEN))
        self.geometry = QDesktopWidget().availableGeometry()
        self.setWindowState(Qt.WindowMaximized)
        self.setMinimumSize(self.geometry.width(), self.geometry.height())
        self.move(self.geometry.x(), self.geometry.y())

        self.normal = Normalize(self.geometry.width(), self.geometry.height())

        self.background = QLabel(self)

        self.initUI()

    def initUI(self):
        # Заставка
        splash = QSplashScreen(QtGui.QPixmap(PATH_SPLASH_SCREEN).scaled(*self.normal.normal_proportion(1544, 900)),
                               QtCore.Qt.WindowStaysOnTopHint)
        splash.show()
        time.sleep(1)
        splash.close()

        pixmap = QPixmap(PATH_MAIN_MENU)
        self.background.setPixmap(pixmap)
        self.background.resize(self.geometry.width(), self.geometry.width())
        self.background.setScaledContents(True)

        self.menu = Menu(self)
        self.menu.setAttribute(Qt.WA_DeleteOnClose)
        self.menu.new_lesson_event.connect(self.on_new_lesson)
        self.menu.show()

    def on_new_lesson(self):
        self.menu.close()
        self.menu = None
        self.new_lesson = NewLesson(self)
        self.new_lesson.show()


class Menu(QWidget):
    new_lesson_event = pyqtSignal()

    def __init__(self, main_window):
        super().__init__(main_window)
        self.normal = main_window.normal
        self.main_window = main_window

        self.setGeometry(0, 0, self.main_window.geometry.width(), self.main_window.geometry.height())

        self.initUI()

    def initUI(self):
        # --------------------------
        #       Кнопки меню
        # --------------------------

        # Кнопка создания нового урока
        self.btn_new_lesson = QPushButton("Новый урок", self)
        self.btn_new_lesson.resize(*self.normal.normal_xy(200, 50))
        self.btn_new_lesson.move(*self.normal.normal_xy(175, 200))
        # 548490 - темный голубой  76b7c7 - светлый голубой
        self.btn_new_lesson.setStyleSheet(
            '.QPushButton {'
            'background-color: #76b7c7;'
            'border-style: outset;'
            'border-width: 2px;'
            'border-radius: 10px;'
            'border-color: beige;'
            'font: bold ' + self.normal.normal_font(17) + 'px;'
                                                          'min-width: 10em;'
                                                          'padding: 6px;'
                                                          '}'
                                                          '.QPushButton:hover {'
                                                          'background-color: #548490;'
                                                          'border-style: inset;'
                                                          '}')
        self.btn_new_lesson.clicked.connect(self.create_new_lesson)

        # Цитата в главном меню
        self.quote = QLabel(random.choice(LIST_LESSON_QUOTE), self)
        self.quote.move(int(self.main_window.geometry.width() / 2.6), int(self.main_window.geometry.height() / 3))
        self.quote.setWordWrap(True)
        self.quote.setStyleSheet('.QLabel {font-family: "Impact";'
                                 'font: ' + self.normal.normal_font(55) + 'px}')
        self.quote.setMinimumSize(self.main_window.geometry.width() // 2, self.main_window.geometry.height() // 4)

    def create_new_lesson(self):
        self.new_lesson_event.emit()


class NewLesson(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setGeometry(self.main_window.geometry.width() // 4, self.main_window.geometry.height() // 4,
                         self.main_window.geometry.width() // 2, self.main_window.geometry.height() // 2)
        self.initUI()

    def initUI(self):
        self.background_form_options_new_lesson = QLabel(self)
        self.background_form_options_new_lesson.setStyleSheet(
            '.QLabel {'
            'background-color: #76b7c7;'
            'border-style: outset;'
            'border-width: 2px;'
            'border-radius: 10px;'
            'border-color: beige;'
            'min-width: 10em;'
            'padding: 6px;'
            '}')
        self.background_form_options_new_lesson.resize(self.geometry().width(), self.geometry().height())

        # self.layout_options_new_lesson =

        # Тексты
        # -----------------------------------------
        self.text_lesson_topic = QLabel("Тема урока")
        self.text_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_subjects = QLabel("Предмет")
        self.text_subjects.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_lesson_type = QLabel("Тип урока")
        self.text_lesson_type.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_class = QLabel("Класс")
        self.text_class.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_class_characteristic = QLabel("Характеристика класса")
        self.text_class_characteristic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_lesson_duration = QLabel("Длительность урока")
        self.text_lesson_duration.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_acquaintance = QLabel("Требуется знакомство?")
        self.text_acquaintance.setStyleSheet(".QLabel {"
                                             f"font: bold {self.main_window.normal.normal_font(16)}px;"
                                             "min-width: 12em;"
                                             "}")
        # -----------------------------------------
        self.text_competence = QLabel("Компетенции ")
        self.text_competence.setStyleSheet(".QLabel {"
                                                       f"font: bold {self.main_window.normal.normal_font(16)}px;"
                                                       "min-width: 12em;"
                                                       "}")

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.text_lesson_topic, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(self.text_subjects, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(self.text_lesson_type, 3, 0)
        grid.addWidget(authorEdit, 3, 1)

        grid.addWidget(self.text_class, 4, 0)
        grid.addWidget(authorEdit, 4, 1)

        grid.addWidget(self.text_class_characteristic, 5, 0)
        grid.addWidget(authorEdit, 5, 1)

        grid.addWidget(self.text_lesson_duration, 6, 0)
        grid.addWidget(authorEdit, 6, 1)

        grid.addWidget(self.text_acquaintance, 7, 0)
        grid.addWidget(authorEdit, 7, 1)

        grid.addWidget(self.text_competence, 8, 0)
        grid.addWidget(authorEdit, 8, 1)
        self.setLayout(grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
