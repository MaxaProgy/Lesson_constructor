# -*- coding: utf-8 -*-

import sys
import time
import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QDesktopWidget, QLabel, QWidget, QPushButton, \
    QGridLayout, QLineEdit, QCheckBox, QButtonGroup, QComboBox, QRadioButton, QMessageBox, QVBoxLayout, \
    QScrollArea, QFrame, QHBoxLayout
from sqlalchemy import or_

from app_window.const import *
from app_window.data.cards import Cards


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

        self.run_menu()

    def on_new_lesson(self):
        self.menu.close()
        self.menu = None
        self.run_new_lesson()

    def on_menu(self):
        self.new_lesson.close()
        self.new_lesson = None
        self.run_menu()

    def on_constructor(self, data):
        self.new_lesson.close()
        self.new_lesson = None
        self.run_constructor(data)

    def run_menu(self):
        self.menu = Menu(self)
        self.menu.setAttribute(Qt.WA_DeleteOnClose)
        self.menu.create_new_lesson_event.connect(self.on_new_lesson)
        self.menu.show()

    def run_new_lesson(self):
        self.new_lesson = NewLesson(self)
        self.new_lesson.setAttribute(Qt.WA_DeleteOnClose)
        self.new_lesson.back_menu_event.connect(self.on_menu)
        self.new_lesson.create_constructor_event.connect(self.on_constructor)
        self.new_lesson.show()

    def run_constructor(self, data):
        self.constructor = Constructor(self, data)
        self.constructor.setAttribute(Qt.WA_DeleteOnClose)
        self.constructor.show()


class Menu(QWidget):
    create_new_lesson_event = pyqtSignal()

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
        self.create_new_lesson_event.emit()


class NewLesson(QWidget):
    back_menu_event = pyqtSignal()
    create_constructor_event = pyqtSignal(dict)

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

        # Тексты
        # -----------------------------------------
        self.text_lesson_topic = QLabel("Тема урока")
        self.text_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_subjects = QLabel("Предмет")
        self.text_subjects.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_lesson_type = QLabel("Тип урока")
        self.text_lesson_type.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_class = QLabel("Класс")
        self.text_class.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_class_characteristic = QLabel("Характеристика класса")
        self.text_class_characteristic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_lesson_duration = QLabel("Длительность урока")
        self.text_lesson_duration.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_acquaintance = QLabel("Требуется знакомство?")
        self.text_acquaintance.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")
        # -----------------------------------------
        self.text_competence = QLabel("Компетенции ")
        self.text_competence.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}")

        # Поля ввода значений
        # -----------------------------------------
        self.edit_lesson_topic = QLineEdit()
        self.edit_lesson_topic.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.combo_subjects = QComboBox()
        self.combo_subjects.addItems([item.name_subject for item in SESSION.query(Subject).all()])
        self.combo_subjects.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}")
        # -----------------------------------------
        self.combo_lesson_type = QComboBox()
        self.combo_lesson_type.addItems([item.name_lesson_type for item in SESSION.query(LessonType).all()])
        self.combo_lesson_type.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}")
        # -----------------------------------------
        self.combo_class = QComboBox()
        self.combo_class.addItems([str(class_) for class_ in range(1, 12)])
        self.combo_class.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}")
        # -----------------------------------------
        self.combo_class_characteristic = QComboBox()
        self.combo_class_characteristic.addItems([item.name_class_characteristic for item
                                                  in SESSION.query(ClassCharacteristic).all()])
        self.combo_class_characteristic.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}")
        # -----------------------------------------
        self.edit_lesson_duration = QLineEdit("40")
        self.edit_lesson_duration.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.radio_btn_yes = QRadioButton('Да')
        self.radio_btn_yes.setStyleSheet(
            ".QRadioButton {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        self.radio_btn_no = QRadioButton('Нет')
        self.radio_btn_no.setStyleSheet(
            ".QRadioButton {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        self.radio_btn_no.setChecked(True)
        self.btn_radio_group = QButtonGroup()
        self.btn_radio_group.addButton(self.radio_btn_yes)
        self.btn_radio_group.addButton(self.radio_btn_no)
        # -----------------------------------------
        self.check_communication = QCheckBox('Коммуникация')
        self.check_communication.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.check_literacy = QCheckBox('Грамотность')
        self.check_literacy.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.check_cooperation = QCheckBox('Кооперация')
        self.check_cooperation.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.check_creative_thinking = QCheckBox('Креативное мышление')
        self.check_creative_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.check_critical_thinking = QCheckBox('Критическое мышление')
        self.check_critical_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки')
        self.check_metacognitive_skills.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}")
        # -----------------------------------------
        self.btn_back_valid = QPushButton(self)
        self.btn_back_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}')
        self.btn_back_valid.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back_valid.move(15, 3)
        self.btn_back_valid.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok_valid = QPushButton(self)
        self.btn_ok_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}')
        self.btn_ok_valid.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok_valid.move(self.geometry().width() - self.main_window.normal.normal_proportion(75, 0)[0] - 12, 3)
        self.btn_ok_valid.clicked.connect(self.valid_options_new_lesson)
        # -----------------------------------------

        grid = QGridLayout()
        grid.setContentsMargins(15, self.main_window.normal.normal_proportion(75, 0)[0], 15, 15)
        grid.addWidget(self.text_lesson_topic, 1, 0)
        grid.addWidget(self.edit_lesson_topic, 1, 1)

        grid.addWidget(self.text_subjects, 2, 0)
        grid.addWidget(self.combo_subjects, 2, 1)

        grid.addWidget(self.text_lesson_type, 3, 0)
        grid.addWidget(self.combo_lesson_type, 3, 1)

        grid.addWidget(self.text_class, 4, 0)
        grid.addWidget(self.combo_class, 4, 1)

        grid.addWidget(self.text_class_characteristic, 5, 0)
        grid.addWidget(self.combo_class_characteristic, 5, 1)

        grid.addWidget(self.text_lesson_duration, 6, 0)
        grid.addWidget(self.edit_lesson_duration, 6, 1)

        grid.addWidget(self.text_acquaintance, 7, 0)
        grid_acquaintance = QGridLayout()
        grid_acquaintance.addWidget(self.radio_btn_yes, 1, 0)
        grid_acquaintance.addWidget(self.radio_btn_no, 1, 1)
        grid.addLayout(grid_acquaintance, 7, 1)

        grid.addWidget(self.text_competence, 8, 0)
        grid_competence = QGridLayout()
        grid_competence.addWidget(self.check_communication, 1, 0)
        grid_competence.addWidget(self.check_literacy, 2, 0)
        grid_competence.addWidget(self.check_cooperation, 3, 0)
        grid_competence.addWidget(self.check_creative_thinking, 1, 1)
        grid_competence.addWidget(self.check_critical_thinking, 2, 1)
        grid_competence.addWidget(self.check_metacognitive_skills, 3, 1)
        grid.addLayout(grid_competence, 8, 1)
        self.setLayout(grid)

    def back_menu(self):
        self.back_menu_event.emit()

    def valid_options_new_lesson(self):
        if self.edit_lesson_topic.text() != "" and \
                int(self.edit_lesson_duration.text()) >= 20 and \
                (self.check_creative_thinking.isChecked() or
                 self.check_literacy.isChecked() or
                 self.check_communication.isChecked() or
                 self.check_cooperation.isChecked() or
                 self.check_critical_thinking.isChecked() or
                 self.check_metacognitive_skills.isChecked()):

            self.create_constructor_event.emit(
                {
                    "lesson_topic": self.edit_lesson_topic.text(),
                    "subjects": self.combo_subjects.currentText(),
                    "lesson_type": self.combo_lesson_type.currentText(),
                    "class": self.combo_class.currentText(),
                    "class_characteristic": self.combo_class_characteristic.currentText(),
                    "lesson_duration": int(self.edit_lesson_duration.text()),
                    "acquaintance": self.radio_btn_yes.isChecked(),
                    "competence": {
                        "creative_thinking": self.check_creative_thinking.isChecked(),
                        "literacy": self.check_literacy.isChecked(),
                        "communication": self.check_communication.isChecked(),
                        "cooperation": self.check_cooperation.isChecked(),
                        "critical_thinking": self.check_critical_thinking.isChecked(),
                        "metacognitive_skills": self.check_metacognitive_skills.isChecked()
                    }
                })
        else:
            QMessageBox.critical(self, "Ошибка", "Вы заполните все поля", QMessageBox.Ok)


class Constructor(QWidget):
    def __init__(self, main_window, data):
        super().__init__(main_window)
        self.data_lesson = data
        self.main_window = main_window
        self.setGeometry(0, 0, self.main_window.geometry.width(), self.main_window.geometry.height())

        self.filter_methods = SESSION.query(Cards).filter(
            or_(Cards.creative_thinking == data['competence']['creative_thinking'],
                Cards.critical_thinking == data['competence']['critical_thinking'],
                Cards.communication == data['competence']['communication'],
                Cards.cooperation == data['competence']['cooperation'],
                Cards.metacognitive_skills == data['competence']['metacognitive_skills'],
                Cards.literacy == data['competence']['literacy'])
        )
        self.flag_stage = 0  # id Командообразования
        self.object_methods = []
        self.my_methods = []
        self.initUI()

    def initUI(self):
        # -----------------------------------------
        #                Кнопки
        # -----------------------------------------

        """self.btn_back_valid = QPushButton(self)
        self.btn_back_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}')
        self.btn_back_valid.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back_valid.move(15, 3)
        self.btn_back_valid.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok_valid = QPushButton(self)
        self.btn_ok_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}')"""
        # -----------------------------------------
        self.layout_constructor_h_3 = QGridLayout(self)
        self.layout_constructor_h_3.setContentsMargins(0, int(self.window().width() / 25.5), 0,
                                                       int(self.window().width() / 25.5))
        # Кнопки этапов урока
        if self.data_lesson['acquaintance']:
            self.btn_stage_acquaintance = QPushButton("Знакомство", self)
            self.btn_stage_acquaintance.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
            self.btn_stage_acquaintance.setStyleSheet(
                ".QPushButton {"
                "background-color: #76b7c7;"
                "border-style: outset;"
                "border-width: 2px;"
                "border-radius: 10px;"
                "border-color: beige;"
                f"font: bold {self.main_window.normal.normal_font(18)}px;"
                "min-width: 10em;"
                "padding: 6px;"
                "}"
                ".QPushButton:hover {"
                "background-color: #548490;"
                "border-style: inset;"
                "}")
        self.btn_team_building = QPushButton("Командообразование", self)
        self.btn_team_building.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_team_building.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.btn_new_material = QPushButton("Новый материал", self)
        self.btn_new_material.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_new_material.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.btn_refreshments = QPushButton("Бодрилки", self)
        self.btn_refreshments.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_refreshments.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.btn_test_of_understanding = QPushButton("Проверка понимания", self)
        self.btn_test_of_understanding.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_test_of_understanding.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.btn_material_fixing = QPushButton("Закрепление", self)
        self.btn_material_fixing.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_material_fixing.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.btn_assimilation_control = QPushButton("Контроль усвоения", self)
        self.btn_assimilation_control.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_assimilation_control.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.btn_reflection = QPushButton("Рефлексия", self)
        self.btn_reflection.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_reflection.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.btn_homework = QPushButton("Домашнее задание", self)
        self.btn_homework.setMinimumSize(*self.main_window.normal.normal_proportion(55, 80))
        self.btn_homework.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")

        self.group_button_stage = QButtonGroup(self)
        if self.data_lesson['acquaintance']:
            self.group_button_stage.addButton(self.btn_stage_acquaintance)
        self.group_button_stage.addButton(self.btn_team_building)
        self.group_button_stage.addButton(self.btn_new_material)
        self.group_button_stage.addButton(self.btn_refreshments)
        self.group_button_stage.addButton(self.btn_test_of_understanding)
        self.group_button_stage.addButton(self.btn_material_fixing)
        self.group_button_stage.addButton(self.btn_assimilation_control)
        self.group_button_stage.addButton(self.btn_reflection)
        self.group_button_stage.addButton(self.btn_homework)
        self.group_button_stage.buttonClicked.connect(self.button_stage_flag)

        grid = QVBoxLayout(self)
        grid.setContentsMargins(25, int(self.window().width() / 18.5), 10, int(self.window().width() / 12.5))
        if self.data_lesson['acquaintance']:
            grid.addWidget(self.btn_stage_acquaintance)
        grid.addWidget(self.btn_team_building)
        grid.addWidget(self.btn_new_material)
        grid.addWidget(self.btn_refreshments)
        grid.addWidget(self.btn_test_of_understanding)
        grid.addWidget(self.btn_material_fixing)
        grid.addWidget(self.btn_assimilation_control)
        grid.addWidget(self.btn_reflection)
        grid.addWidget(self.btn_homework)

        grid.addStretch(int(self.window().width() / 23.5))
        grid.setSpacing(int(self.window().width() / 23.5))

        self.layout_constructor_h_3.addLayout(grid, 0, 0, 0, 1)
        # -------------------------------------------
        self.scroll_main_methods = QScrollArea(self)
        self.scroll_main_methods.setStyleSheet(".QScrollArea {"
                                               "background-color:transparent;"
                                               "}")
        self.scroll_main_methods.setFrameShape(QFrame.NoFrame)
        self.scroll_main_methods.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_main_methods.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_main_methods.resize(int(self.window().width() / 2),
                                        int(self.window().height() / 1.1))
        self.layout_constructor_h_3.addWidget(self.scroll_main_methods, 0, 1, 0, 4)

        layout_3_constructor = QVBoxLayout()
        # -------------------------------------------
        layout_time_back_ok = QHBoxLayout()
        self.time_lesson = QLabel(f"Время урока: {self.data_lesson['lesson_duration']} минут")
        self.time_lesson.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(20)}px;"
            "}")
        layout_time_back_ok.addWidget(self.time_lesson)

        self.btn_back_constructor = QPushButton()
        self.btn_back_constructor.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}')
        self.btn_back_constructor.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back_constructor.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        layout_time_back_ok.addWidget(self.btn_back_constructor)

        self.btn_ok_constructor = QPushButton()
        self.btn_ok_constructor.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}')
        self.btn_ok_constructor.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok_constructor.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        layout_time_back_ok.addWidget(self.btn_ok_constructor)

        layout_3_constructor.addLayout(layout_time_back_ok)
        # -------------------------------------------
        self.scroll_my_methods = QScrollArea(self)
        self.scroll_my_methods.setStyleSheet(".QScrollArea {background-color:transparent;}")
        self.scroll_my_methods.setFrameShape(QFrame.NoFrame)
        self.scroll_my_methods.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_my_methods.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout_3_constructor.addWidget(self.scroll_my_methods)
        # -------------------------------------------
        layout_btn_save_open_del = QVBoxLayout(self)
        self.btn_save_lesson = QPushButton("Сохранить урок")
        self.btn_save_lesson.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")

        layout_btn_save_open_del.addWidget(self.btn_save_lesson)
        self.btn_open_lesson = QPushButton("Открыть урок")
        self.btn_open_lesson.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")

        layout_btn_save_open_del.addWidget(self.btn_open_lesson)
        self.btn_del_lesson = QPushButton("Удалить урок")
        self.btn_del_lesson.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")

        layout_btn_save_open_del.addWidget(self.btn_del_lesson)
        layout_3_constructor.addLayout(layout_btn_save_open_del)
        self.layout_constructor_h_3.addLayout(layout_3_constructor, 0, 5, 0, 2)

    def button_stage_flag(self, button):
        self.flag_stage = SESSION.query(Stage).filter(Stage.name_stage == button.text()).first().id
        self.show_methods_stage()

    def show_methods_stage(self):
        # Забираем все методы в соответствии с выбранным нами этапом урока
        filter_stage_methods = self.filter_methods.filter(Cards.id_stage_card.like(self.flag_stage)).all()

        # Удаление всех элементов из прошлого списка обектов методов
        for i in reversed(range(len(self.object_methods))):
            del self.object_methods[i]

        # Список id выбранных мной методов
        id_my_methods = [method.data.id for method in self.my_methods]

        # Удаляем все методы, входящие в список моих методов из общего списка
        # Чтобы повторно не отображать методы в панели
        for i in reversed(range(len(filter_stage_methods))):
            if filter_stage_methods[i].id in id_my_methods:
                del filter_stage_methods[i]

        # Создаем обекты-методы вносим их в лейаут
        layout = QVBoxLayout()
        for i in range(len(filter_stage_methods)):
            self.object_methods.append(Method(self, filter_stage_methods[i]))
            layout.addWidget(self.object_methods[i])

        widget = QWidget()
        widget.setGeometry(0, 0, int(self.main_window.geometry.height() / 1.1), 116 * len(filter_stage_methods))
        widget.setLayout(layout)
        widget.setStyleSheet(".QWidget {background-color:transparent;}")
        self.scroll_main_methods.setWidget(widget)
        self.scroll_main_methods.show()


class Method(QWidget):
    def __init__(self, parent, data):
        super(Method, self).__init__(parent.main_window)
        self.parent = parent
        self.data = data
        self.initUI()

    def initUI(self):
        self.background = QLabel(self)
        self.background.setStyleSheet('.QLabel {'
                                      f'min-height: {100}px;'
                                      f'min-width: {int(self.parent.scroll_main_methods.size().width() / 1.1)}px;'
                                      'margin-bottom: 16px;'
                                      'background-color: #FFA25F;'
                                      'border-radius: 14px'
                                      '}')
        layout = QHBoxLayout(self)
        self.label_lesson_topic = QLabel(self.data.name_method[0].upper() + self.data.name_method[1:], self)
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.parent.main_window.normal.normal_font(24)}px;"
            "margin-left: 4px"
            "}")
        layout.addWidget(self.label_lesson_topic)

        self.btn_more_details = QPushButton(self)
        self.btn_more_details.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_PADROBNEE});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_PADROBNEE_HOVER});'
            '}')
        self.btn_more_details.setMinimumSize(*self.parent.main_window.normal.normal_proportion(175, 60))
        self.btn_more_details.setFixedWidth(self.parent.main_window.normal.normal_proportion(175, 0)[0])
        layout.addWidget(self.btn_more_details)

        self.btn_add = QPushButton(self)
        self.btn_add.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_ADD});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_ADD_HOVER});'
            '}')
        self.btn_add.setMinimumSize(*self.parent.main_window.normal.normal_proportion(40, 40))
        self.btn_add.setFixedWidth(self.parent.main_window.normal.normal_proportion(40, 0)[0])
        layout.addWidget(self.btn_add)

        self.btn_del = QPushButton(self)
        self.btn_del.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_DEL});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_DEL_HOVER});'
            '}')
        self.btn_del.setMinimumSize(*self.parent.main_window.normal.normal_proportion(40, 40))
        self.btn_del.setFixedWidth(self.parent.main_window.normal.normal_proportion(40, 0)[0])
        layout.addWidget(self.btn_del)
        self.btn_del.hide()

        self.btn_add.clicked.connect(self.add_card)
        self.btn_del.clicked.connect(self.del_card)

    def add_card(self):
        time_my_methods = [int(method.data.time) for method in self.parent.my_methods]
        if sum(time_my_methods) + int(self.data.time) <= self.parent.data_lesson['lesson_duration'] + 20:
            self.parent.my_methods.append(self)
            self.show_my_methods()
            self.btn_add.hide()
            self.btn_del.show()
            self.parent.show_methods_stage()
            self.show_time_methods()

        else:
            QMessageBox.critical(self.parent, "Ошибка", "Превышен лимит времени", QMessageBox.Ok)
            return

    def del_card(self):
        del self.parent.my_methods[self.parent.my_methods.index(self)]
        self.show_my_methods()
        self.parent.show_methods_stage()
        self.show_time_methods()

    def show_my_methods(self):
        layout = QGridLayout()
        for method in self.parent.my_methods:
            layout.addWidget(method)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setStyleSheet(".QWidget {background-color:transparent;}")
        self.parent.scroll_my_methods.setWidget(widget)

    def show_time_methods(self):
        sum_1 = sum([int(method.data.time) for method in self.parent.my_methods])
        self.parent.time_lesson.setText(
            "Время урока: " + str(self.parent.data_lesson['lesson_duration'] - sum_1) + " минут")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
