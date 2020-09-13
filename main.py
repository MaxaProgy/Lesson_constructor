# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
    QSplashScreen, QPushButton
from PyQt5 import uic, QtGui, QtCore
import time

from Lesson_constructor.data import db_session
from Lesson_constructor.new_lesson_file import NewLesson
from Lesson_constructor.data.type_method import TypeMethod
from Lesson_constructor.data.stage import Stage
from Lesson_constructor.data.classes import Classes
from Lesson_constructor.data.fgos import Fgos
from Lesson_constructor.data.cards import Cards


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        db_session.global_init("db/lesson_constructor.sqlite")
        session = db_session.create_session()

        type_method = [item.name_method for item in session.query(TypeMethod).all()]
        classes = [item.name_class for item in session.query(Classes).all()]
        fgos = [item.name_fgos for item in session.query(Fgos).all()]
        stage = [item.name_stage for item in session.query(Stage).all()]

        if not type_method:
            session = db_session.create_session()
            type_method_value = ["Индивидуальная", "Групповая", "Индивидуальная/Групповая"]
            for value in type_method_value:
                type_method_value = TypeMethod(
                    name_method=value,
                )
                session.add(type_method_value)
                session.commit()

        if not classes:
            session = db_session.create_session()
            classes_value = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
            for value in classes_value:
                classes_value = Classes(
                    name_class=value,
                )
                session.add(classes_value)
                session.commit()

        if not fgos:
            session = db_session.create_session()
            fgos_value = ["Предметные", "Личностные", "-"]
            for value in fgos_value:
                fgos_value = Fgos(
                    name_fgos=value,
                )
                session.add(fgos_value)
                session.commit()

        if not stage:
            session = db_session.create_session()
            stage_value = ["Знакомство", "Командообразование",
                           "Новый материал", "Бодрилки", "Проверка понимания", "Закрепление материала",
                           "Контроль усвоения", "Рефлексия", "Домашнее задание"]
            for value in stage_value:
                stage_value = Stage(
                    name_stage=value,
                )
                session.add(stage_value)
                session.commit()

        uic.loadUi('data/ui_file/untitled.ui', self)
        self.geometry = QDesktopWidget().availableGeometry()
        self.setMinimumHeight(self.geometry.height())
        self.setMinimumWidth(self.geometry.width())

        # --------------------------
        #       Кнопки меню
        # --------------------------

        # Кнопка создания нового урока
        self.btn_new_lesson = QPushButton("Новый урок", self)
        self.btn_new_lesson.resize(200, 50)
        self.btn_new_lesson.move(175, 200)
        # 548490 - темный голубой  76b7c7 - светлый голубой
        self.btn_new_lesson.setStyleSheet('''
            .QPushButton {
            background-color: #76b7c7;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
        }
        .QPushButton:hover {
            background-color: #548490;
            border-style: inset;
        }''')

        self.btn_new_lesson.clicked.connect(self.create_new_lesson)

        self.main_menu()

    # -----------------------------------------

    def main_menu(self):
        self.setStyleSheet('.QWidget {background-image: url(data/image/фоны/меню.jpg);}')
        self.btn_new_lesson.show()

    # -----------------------------------------
    def create_new_lesson(self):
        self.new_lesson = NewLesson(self)

    # -----------------------------------------


app = QApplication(sys.argv)
ex = Menu()

# Заставка
splash = QSplashScreen(QtGui.QPixmap('data/image/фоны/заставка.png'), QtCore.Qt.WindowStaysOnTopHint)
splash.show()
time.sleep(1)
splash.close()

ex.show()
sys.exit(app.exec_())
