# -*- coding: utf-8 -*-

import sys
import time
import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QDesktopWidget, QLabel, QWidget, QPushButton, \
    QGridLayout, QLineEdit, QCheckBox, QButtonGroup, QComboBox, QRadioButton, QMessageBox, QVBoxLayout, \
    QAbstractItemView, QSizePolicy

from app_window.const import *


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
        grid.setContentsMargins(25, int(self.window().width() / 18.5),
                                int(self.window().width() / 0.9),
                                int(self.window().width() / 12.5))
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
        self.setLayout(grid)

    def button_stage_flag(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
