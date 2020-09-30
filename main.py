# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
    QSplashScreen, QPushButton, QLabel
from PyQt5 import uic, QtGui, QtCore
import time
import random

from data import db_session
from new_lesson_file import NewLesson
from data.type_method import TypeMethod
from data.stage import Stage
from data.classes import Classes
from data.fgos import Fgos
from data.subject import Subject
from data.class_characteristic import ClassCharacteristic
from data.lesson_type import LessonType


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Конструктор уроков')
        self.setWindowIcon(QIcon('data/image/фоны/заставка.png'))

        db_session.global_init("db/lesson_constructor_db.sqlite")
        self.session = db_session.create_session()
        self.list_lesson_quote = ["Учитель прикасается к вечности, никто не знает, где закончится его влияние..",
                                  "Кто постигает новое, лелея старое, Тот может быть учителем.",
                                  "Тот, кто обращаясь к старому, способен открывать новое, достоин быть учителем.",
                                  "Книга — немой учитель.",
                                  "Плохой учитель преподносит истину, хороший учит ее находить.",
                                  "Гений – это талант изобретения того, чему нельзя учить или научиться.",
                                  "Весьма имеют быть наставлены те, которые сами не знают.",
                                  "Кто хорошо выявляет различия, тот хорошо учит.",
                                  "Как в утлый мех воду лить, так безумного учить.",
                                  "Учись тому, чему сам учишь.",
                                  "Хорошо учит говорить тот, кто учит хорошо делать.",
                                  "Опыт – самый лучший учитель, но плата за обучение чересур велика."]

        type_method = [item.name_method for item in self.session.query(TypeMethod).all()]
        classes = [item.name_class for item in self.session.query(Classes).all()]
        fgos = [item.name_fgos for item in self.session.query(Fgos).all()]
        stage = [item.name_stage for item in self.session.query(Stage).all()]
        subject = [item.name_subject for item in self.session.query(Subject).all()]
        class_characteristic = [item.name_class_characteristic for item in self.session.query(ClassCharacteristic).all()]
        lesson_type = [item.name_lesson_type for item in self.session.query(LessonType).all()]

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
            classes_value = ["1-4", "5-8", "9-11", "1-11", "1-8", "5-11"]
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

        if not subject:
            session = db_session.create_session()
            subject_value = ["Начальные классы", "География", "Биология", "Химия", "Физика",
                             "Математика ", "Алгебра", "Геометрия", "Иностранный язык",
                             "Русский язык", "Литература", "Технология", "Физкультура", "Изобразительное искусство",
                             "Музыка", "История", "Обществознание"]
            for value in subject_value:
                subject_value = Subject(
                    name_subject=value,
                )
                session.add(subject_value)
                session.commit()

        if not class_characteristic:
            session = db_session.create_session()
            class_characteristic_value = ["Активные дети", "Пассивные дети", "Дружный класс",
                                          "Имеется наличие лидера (лидеров)", "Имеются проблемы с дисциплиной"]

            for value in class_characteristic_value:
                class_characteristic_value = ClassCharacteristic(
                    name_class_characteristic=value,
                )
                session.add(class_characteristic_value)
                session.commit()

        if not lesson_type:
            session = db_session.create_session()
            lesson_type_value = ["Новый материал", "Контроль усвоения",
                                 "Проверка понимания", "Закрепление материала"]

            for value in lesson_type_value:
                lesson_type_value = LessonType(
                    name_lesson_type=value,
                )
                session.add(lesson_type_value)
                session.commit()


        self.height_windows = 1030
        self.width_windows = 1920
        self.setMinimumHeight(self.height_windows)
        self.setMinimumWidth(self.width_windows)
        self.geometry = QDesktopWidget().availableGeometry()

        self.background = QLabel(self)
        pixmap = QPixmap('data/image/фоны/меню.jpg')
        self.background.resize(self.geometry.width(), self.geometry.height())

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

        self.quote = QLabel(random.choice(self.list_lesson_quote), self)
        self.quote.move(self.width_windows // 2 - 100, 350)
        self.quote.setMinimumSize(600, 100)
        self.quote.setWordWrap(True)
        self.quote.setStyleSheet('.QLabel {font-family: "Impact";'
                                 'font: 50px }')
        self.quote.setMinimumSize(self.quote.sizeHint())
        self.btn_new_lesson.clicked.connect(self.create_new_lesson)

        self.main_menu()

    # -----------------------------------------

    def main_menu(self):
        pixmap = QPixmap('data/image/фоны/меню.jpg')
        self.background.setPixmap(pixmap)
        self.btn_new_lesson.show()
        self.quote.show()

    # -----------------------------------------
    def create_new_lesson(self):
        self.quote.hide()
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
