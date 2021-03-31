# -*- coding: utf-8 -*-

import sys
import time
import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QDesktopWidget, QLabel, QWidget, QPushButton, \
    QGridLayout, QLineEdit, QCheckBox, QButtonGroup, QComboBox, QRadioButton, QMessageBox, QVBoxLayout, \
    QScrollArea, QFrame, QHBoxLayout, QDialog, QListWidget, QTextEdit, QSpinBox
from sqlalchemy import or_

from app_window.const import *
from app_window.data.cards import Cards
from app_window.data.save_lesson import SaveLesson


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

    def run_menu(self):
        self.menu = Menu(self)
        self.menu.setAttribute(Qt.WA_DeleteOnClose)
        self.menu.create_new_lesson_event.connect(self.close_menu_on_new_lesson)
        self.menu.create_new_method_event.connect(self.close_menu_on_new_method)
        self.menu.show()

    def run_new_lesson(self):
        self.new_lesson = NewLesson(self)
        self.new_lesson.setAttribute(Qt.WA_DeleteOnClose)
        self.new_lesson.back_menu_event.connect(self.close_new_lesson_on_menu)
        self.new_lesson.create_constructor_event.connect(self.close_new_lesson_on_constructor)
        self.new_lesson.show()

    def run_constructor(self, data):
        self.constructor = Constructor(self, data)
        self.constructor.setAttribute(Qt.WA_DeleteOnClose)
        self.constructor.back_new_lesson_event.connect(self.close_constructor_on_new_lesson)
        self.constructor.create_result_event.connect(self.close_constructor_on_result)
        self.constructor.show()

    def run_result(self, data):
        self.result = ResultLesson(self, data)
        self.result.setAttribute(Qt.WA_DeleteOnClose)
        self.result.back_constructor_event.connect(self.close_result_on_constructor)
        self.result.show()

    def run_new_method(self):
        self.new_method = NewMethod(self)
        self.new_method.setAttribute(Qt.WA_DeleteOnClose)
        self.new_method.back_menu_event.connect(self.close_new_method_on_menu)
        self.new_method.show()

    def close_new_method_on_menu(self):
        self.new_method.close()
        self.new_method = None
        self.run_menu()

    def close_menu_on_new_method(self):
        self.menu.close()
        self.menu = None
        self.run_new_method()

    def close_result_on_constructor(self, data):
        self.result.close()
        self.result = None
        self.run_constructor(data)

    def close_constructor_on_result(self, data):
        self.constructor.close()
        self.constructor = None
        self.run_result(data)

    def close_menu_on_new_lesson(self):
        self.menu.close()
        self.menu = None
        self.run_new_lesson()

    def close_constructor_on_new_lesson(self):
        self.constructor.close()
        self.constructor = None
        self.run_new_lesson()

    def close_new_lesson_on_menu(self):
        self.new_lesson.close()
        self.new_lesson = None
        self.run_menu()

    def close_new_lesson_on_constructor(self, data):
        self.new_lesson.close()
        self.new_lesson = None
        self.run_constructor(data)


class Menu(QWidget):
    create_new_lesson_event = pyqtSignal()
    create_new_method_event = pyqtSignal()

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
        layout_menu = QGridLayout()
        layout_menu.setContentsMargins(int(self.window().width() / 25.5), int(self.window().width() / 15.5),
                                       int(self.window().width() / 6.5), int(self.window().width() / 13.5))

        layout_btn_menu = QGridLayout()
        layout_btn_menu.setContentsMargins(int(self.window().width() / 20.5), int(self.window().width() / 14.5),
                                           int(self.window().width() / 6.5), int(self.window().width() / 3.5))

        self.btn_new_lesson = QPushButton("Новый урок", self)
        # 548490 - темный голубой  76b7c7 - светлый голубой
        self.btn_new_lesson.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.normal.normal_xy(200, 0)[0]}px;'
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
                                                          '}'
        )
        layout_btn_menu.addWidget(self.btn_new_lesson, 0, 0)
        self.btn_new_lesson.clicked.connect(self.create_new_lesson)

        self.btn_new_method = QPushButton("Создать методику", self)
        self.btn_new_method.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.normal.normal_xy(200, 0)[0]}px;'
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
                                                          '}'
        )
        layout_btn_menu.addWidget(self.btn_new_method, 1, 0)
        self.btn_new_method.clicked.connect(self.create_new_method)

        widget_btn = QWidget()
        widget_btn.setStyleSheet(
            ".QWidget {background-color:transparent;}"
        )
        widget_btn.setLayout(layout_btn_menu)
        layout_menu.addWidget(widget_btn, 0, 0, 0, 3)

        # Цитата в главном меню
        self.quote = QLabel(random.choice(LIST_LESSON_QUOTE), self)
        self.quote.setWordWrap(True)
        self.quote.setStyleSheet(
            '.QLabel {font-family: "Impact";'
            'font: ' + self.normal.normal_font(55) + 'px}'
        )
        layout_menu.addWidget(self.quote, 0, 3, 3, 5)
        self.setLayout(layout_menu)

    def create_new_lesson(self):
        self.create_new_lesson_event.emit()

    def create_new_method(self):
        self.create_new_method_event.emit()


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
            '}'
        )
        self.background_form_options_new_lesson.resize(self.geometry().width(), self.geometry().height())

        # Тексты
        # -----------------------------------------
        self.text_lesson_topic = QLabel("Тема урока")
        self.text_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_subjects = QLabel("Предмет")
        self.text_subjects.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_lesson_type = QLabel("Тип урока")
        self.text_lesson_type.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_class = QLabel("Класс")
        self.text_class.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_class_characteristic = QLabel("Характеристика класса")
        self.text_class_characteristic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_lesson_duration = QLabel("Длительность урока")
        self.text_lesson_duration.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_acquaintance = QLabel("Требуется знакомство?")
        self.text_acquaintance.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_competence = QLabel("Компетенции ")
        self.text_competence.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )

        # Поля ввода значений
        # -----------------------------------------
        self.edit_lesson_topic = QLineEdit()
        self.edit_lesson_topic.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.combo_subjects = QComboBox()
        self.combo_subjects.addItems([item.name_subject for item in SESSION.query(Subject).all()])
        self.combo_subjects.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_lesson_type = QComboBox()
        self.combo_lesson_type.addItems([item.name_lesson_type for item in SESSION.query(LessonType).all()])
        self.combo_lesson_type.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_class = QComboBox()
        self.combo_class.addItems([str(class_) for class_ in range(1, 12)])
        self.combo_class.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_class_characteristic = QComboBox()
        self.combo_class_characteristic.addItems([item.name_class_characteristic for item
                                                  in SESSION.query(ClassCharacteristic).all()])
        self.combo_class_characteristic.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.edit_lesson_duration = QSpinBox()
        self.edit_lesson_duration.setValue(40)
        self.edit_lesson_duration.setStyleSheet(
            ".QSpinBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.radio_btn_yes = QRadioButton('Да')
        self.radio_btn_yes.setStyleSheet(
            ".QRadioButton {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        self.radio_btn_no = QRadioButton('Нет')
        self.radio_btn_no.setStyleSheet(
            ".QRadioButton {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        self.radio_btn_no.setChecked(True)
        self.btn_radio_group = QButtonGroup()
        self.btn_radio_group.addButton(self.radio_btn_yes)
        self.btn_radio_group.addButton(self.radio_btn_no)
        # -----------------------------------------
        self.check_communication = QCheckBox('Коммуникация')
        self.check_communication.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_literacy = QCheckBox('Грамотность')
        self.check_literacy.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_cooperation = QCheckBox('Кооперация')
        self.check_cooperation.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_creative_thinking = QCheckBox('Креативное мышление')
        self.check_creative_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_critical_thinking = QCheckBox('Критическое мышление')
        self.check_critical_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки')
        self.check_metacognitive_skills.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.btn_back_valid = QPushButton(self)
        self.btn_back_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back_valid.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back_valid.move(15, 5)
        self.btn_back_valid.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok_valid = QPushButton(self)
        self.btn_ok_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}'
        )
        self.btn_ok_valid.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok_valid.move(self.geometry().width() - self.main_window.normal.normal_proportion(75, 0)[0] - 12, 5)
        self.btn_ok_valid.clicked.connect(self.valid_options_new_lesson)

        # -----------------------------------------

        layout = QGridLayout()
        layout.setContentsMargins(int(self.window().width() / 25.5), int(self.window().width() / 20.5),
                                  int(self.window().width() / 25.5), int(self.window().width() / 50.5))
        layout.addWidget(self.text_lesson_topic, 1, 0)
        layout.addWidget(self.edit_lesson_topic, 1, 1)

        layout.addWidget(self.text_subjects, 2, 0)
        layout.addWidget(self.combo_subjects, 2, 1)

        layout.addWidget(self.text_lesson_type, 3, 0)
        layout.addWidget(self.combo_lesson_type, 3, 1)

        layout.addWidget(self.text_class, 4, 0)
        layout.addWidget(self.combo_class, 4, 1)

        layout.addWidget(self.text_class_characteristic, 5, 0)
        layout.addWidget(self.combo_class_characteristic, 5, 1)

        layout.addWidget(self.text_lesson_duration, 6, 0)
        layout.addWidget(self.edit_lesson_duration, 6, 1)

        layout.addWidget(self.text_acquaintance, 7, 0)
        layout_acquaintance = QGridLayout()
        layout_acquaintance.addWidget(self.radio_btn_yes, 1, 0)
        layout_acquaintance.addWidget(self.radio_btn_no, 1, 1)
        layout.addLayout(layout_acquaintance, 7, 1)

        layout.addWidget(self.text_competence, 8, 0)
        layout_competence = QGridLayout()
        layout_competence.addWidget(self.check_communication, 1, 0)
        layout_competence.addWidget(self.check_literacy, 2, 0)
        layout_competence.addWidget(self.check_cooperation, 3, 0)
        layout_competence.addWidget(self.check_creative_thinking, 1, 1)
        layout_competence.addWidget(self.check_critical_thinking, 2, 1)
        layout_competence.addWidget(self.check_metacognitive_skills, 3, 1)
        layout.addLayout(layout_competence, 8, 1)
        self.setLayout(layout)

    def back_menu(self):
        self.back_menu_event.emit()

    def valid_options_new_lesson(self):
        if self.edit_lesson_topic.text() != "" and \
                self.edit_lesson_duration.value() >= 20 and \
                (self.check_creative_thinking.isChecked() or
                 self.check_literacy.isChecked() or
                 self.check_communication.isChecked() or
                 self.check_cooperation.isChecked() or
                 self.check_critical_thinking.isChecked() or
                 self.check_metacognitive_skills.isChecked()):

            self.create_constructor_event.emit(
                {
                    "lesson_topic": self.edit_lesson_topic.text(),
                    "subject": self.combo_subjects.currentText(),
                    "lesson_type": self.combo_lesson_type.currentText(),
                    "class": self.combo_class.currentText(),
                    "class_characteristic": self.combo_class_characteristic.currentText(),
                    "lesson_duration": self.edit_lesson_duration.value(),
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
    back_new_lesson_event = pyqtSignal()
    create_result_event = pyqtSignal(dict)

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
                "}"
            )
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
            "}"
        )
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
            "}"
        )
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
            "}"
        )
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
            "}"
        )
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
            "}"
        )
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
            "}"
        )
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
            "}"
        )
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
            "}"
        )

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, int(self.window().width() / 18.5), 10, int(self.window().width() / 12.5))
        if self.data_lesson['acquaintance']:
            layout.addWidget(self.btn_stage_acquaintance)
        layout.addWidget(self.btn_team_building)
        layout.addWidget(self.btn_new_material)
        layout.addWidget(self.btn_refreshments)
        layout.addWidget(self.btn_test_of_understanding)
        layout.addWidget(self.btn_material_fixing)
        layout.addWidget(self.btn_assimilation_control)
        layout.addWidget(self.btn_reflection)
        layout.addWidget(self.btn_homework)

        layout.addStretch(int(self.window().width() / 23.5))
        layout.setSpacing(int(self.window().width() / 23.5))

        self.layout_constructor_h_3.addLayout(layout, 0, 0, 0, 1)
        # -------------------------------------------
        self.scroll_main_methods = QScrollArea(self)
        self.scroll_main_methods.setStyleSheet(
            ".QScrollArea {"
            "background-color:transparent;"
            "}"
        )
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
            "}"
        )
        layout_time_back_ok.addWidget(self.time_lesson)

        self.btn_back_constructor = QPushButton()
        self.btn_back_constructor.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back_constructor.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back_constructor.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        layout_time_back_ok.addWidget(self.btn_back_constructor)
        self.btn_back_constructor.clicked.connect(self.back_new_lesson)

        self.btn_ok_constructor = QPushButton()
        self.btn_ok_constructor.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}'
        )
        self.btn_ok_constructor.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok_constructor.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        layout_time_back_ok.addWidget(self.btn_ok_constructor)
        self.btn_ok_constructor.clicked.connect(self.volid_data_constructor)

        layout_3_constructor.addLayout(layout_time_back_ok)
        # -------------------------------------------
        self.scroll_my_methods = QScrollArea(self)
        self.scroll_my_methods.setStyleSheet(
            ".QScrollArea {background-color:transparent;}"
        )
        self.scroll_my_methods.setFrameShape(QFrame.NoFrame)
        self.scroll_my_methods.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
            "}"
        )
        self.btn_save_lesson.clicked.connect(self.save_lesson)

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
            "}"
        )
        self.btn_open_lesson.clicked.connect(self.open_lesson)

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
            "}"
        )
        self.btn_del_lesson.clicked.connect(self.del_lesson)

        layout_btn_save_open_del.addWidget(self.btn_del_lesson)
        layout_3_constructor.addLayout(layout_btn_save_open_del)
        self.layout_constructor_h_3.addLayout(layout_3_constructor, 0, 5, 0, 2)

    def button_stage_flag(self, button):
        self.flag_stage = SESSION.query(Stage).filter(Stage.name_stage == button.text()).first().id
        self.show_methods_stage()

    def save_lesson(self):
        if int(self.time_lesson.text().split()[2]) == 0:
            if self.data_lesson["lesson_topic"] in [item.name for item in SESSION.query(SaveLesson).all()]:
                reply = QMessageBox.question(self, "Предупреждение",
                                             "Урок с таким названием уже сущестует. Вы хотите перезаписать?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    lesson = SESSION.query(SaveLesson).filter(
                        SaveLesson.name == self.data_lesson["lesson_topic"]).first()
                    SESSION.delete(lesson)
                    SESSION.commit()

            save_lesson = SaveLesson(
                name=self.data_lesson["lesson_topic"],
                ids=';'.join([str(method.data.id) for method in self.my_methods]),
            )
            SESSION.add(save_lesson)
            SESSION.commit()
            QMessageBox.information(self, "Ок", "Урок сохранен", QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Ошибка", "Вы не использовали все время урока", QMessageBox.Ok)

    def open_lesson(self):
        self.open = QDialog()
        self.open.setWindowTitle("Открыть")
        self.open.resize(*self.main_window.normal.normal_proportion(300, 150))
        self.list_view = QListWidget(self.open)
        self.list_view.resize(*self.main_window.normal.normal_proportion(300, 150))
        self.list_view.addItems([item.name for item in SESSION.query(SaveLesson).all()])
        self.list_view.doubleClicked.connect(self.open_select_lesson)
        self.open.exec()

    def open_select_lesson(self):
        self.open.close()
        self.my_methods = []
        for id_card in SESSION.query(SaveLesson).filter(SaveLesson.name ==
                                                        self.list_view.currentItem().text()).first().ids.split(";"):
            self.my_methods.append(Method(self, SESSION.query(Cards).filter(Cards.id == id_card).first()))
            self.my_methods[-1].btn_add.hide()
            self.my_methods[-1].btn_del.show()
            self.my_methods[-1].background.setStyleSheet(
                '.QLabel {'
                f'min-height: {100}px;'
                f'min-width: {int(self.my_methods[-1].parent.scroll_my_methods.size().width())}px;'
                'margin-bottom: 16px;'
                'background-color: #FFA25F;'
                '}'
            )
        self.my_methods[0].show_my_methods()
        self.my_methods[0].show_time_methods()
        self.show_methods_stage()

    def del_lesson(self):
        self.delete = QDialog()
        self.delete.setWindowTitle("Удалить")
        self.delete.resize(*self.main_window.normal.normal_proportion(300, 150))
        self.list_view = QListWidget(self.delete)
        self.list_view.resize(*self.main_window.normal.normal_proportion(300, 150))
        self.list_view.addItems([item.name for item in SESSION.query(SaveLesson).all()])
        self.list_view.doubleClicked.connect(self.del_select_lesson)
        self.delete.exec()

    def del_select_lesson(self):
        self.delete.close()
        reply = QMessageBox.question(self, "Удаление", "Вы хотите удалить урок?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            lesson = SESSION.query(SaveLesson).filter(SaveLesson.name == self.list_view.currentItem().text()).first()
            SESSION.delete(lesson)
            SESSION.commit()

    def back_new_lesson(self):
        self.back_new_lesson_event.emit()

    def volid_data_constructor(self):
        if int(self.time_lesson.text().split()[2]) == 0:
            self.create_result_event.emit(
                {
                    "methods": self.my_methods,
                    "lesson_topic": self.data_lesson["lesson_topic"],
                    "subject": self.data_lesson["subject"],
                    "lesson_type": self.data_lesson["lesson_type"],
                    "class": self.data_lesson["class"],
                    "class_characteristic": self.data_lesson["class_characteristic"],
                    "lesson_duration": self.data_lesson["lesson_duration"],
                    "acquaintance": self.data_lesson["acquaintance"],
                    "competence": {
                        "creative_thinking": self.data_lesson["competence"]["creative_thinking"],
                        "literacy": self.data_lesson["competence"]["literacy"],
                        "communication": self.data_lesson["competence"]["communication"],
                        "cooperation": self.data_lesson["competence"]["cooperation"],
                        "critical_thinking": self.data_lesson["competence"]["critical_thinking"],
                        "metacognitive_skills": self.data_lesson["competence"]["metacognitive_skills"]
                    }
                })
        else:
            QMessageBox.critical(self, "Ошибка", "Вы не использовали все время урока", QMessageBox.Ok)

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
        widget.setStyleSheet(
            ".QWidget {background-color:transparent;}"
        )
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
        self.background.setStyleSheet(
            '.QLabel {'
            f'min-height: {100}px;'
            f'min-width: {int(self.parent.scroll_main_methods.size().width() / 1.1)}px;'
            'margin-bottom: 16px;'
            'background-color: #FFA25F;'
            'border-radius: 14px'
            '}'
        )
        layout = QHBoxLayout(self)
        self.method_time = QLabel(self.data.time + "'", self)
        self.method_time.setStyleSheet(
            '.QLabel {'
            'font-family: "Impact";'
            f"font: bold {self.parent.main_window.normal.normal_font(24)}px;"
            '}'
        )
        self.method_time.setWordWrap(True)
        layout.addWidget(self.method_time)

        self.label_lesson_topic = QLabel(self.data.name_method[0].upper() + self.data.name_method[1:].lower(), self)
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.parent.main_window.normal.normal_font(24)}px;"
            "}"
        )
        layout.addWidget(self.label_lesson_topic)

        self.btn_more_details = QPushButton(self)
        self.btn_more_details.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_PADROBNEE});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_PADROBNEE_HOVER});'
            '}'
        )
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
            '}'
        )
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
            '}'
        )
        self.btn_del.setMinimumSize(*self.parent.main_window.normal.normal_proportion(40, 40))
        self.btn_del.setFixedWidth(self.parent.main_window.normal.normal_proportion(40, 0)[0])
        layout.addWidget(self.btn_del)
        self.btn_del.hide()

        self.btn_add.clicked.connect(self.add_card)
        self.btn_del.clicked.connect(self.del_card)
        self.btn_more_details.clicked.connect(self.details)

    def add_card(self):
        time_my_methods = [int(method.data.time) for method in self.parent.my_methods]
        if sum(time_my_methods) + int(self.data.time) <= self.parent.data_lesson['lesson_duration'] + 20:
            self.parent.my_methods.append(self)
            self.background.setStyleSheet(
                '.QLabel {'
                f'min-height: {100}px;'
                f'min-width: {int(self.parent.scroll_my_methods.size().width() / 1.2)}px;'
                'margin-bottom: 16px;'
                'background-color: #FFA25F;'
                '}'
            )
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
        widget.setStyleSheet(
            ".QWidget {background-color:transparent;}"
        )
        self.parent.scroll_my_methods.setWidget(widget)

    def show_time_methods(self):
        for method in self.parent.my_methods:
            method.method_time.setText(method.data.time + "'")

        sum_1 = sum([int(method.data.time) for method in self.parent.my_methods])
        if sum_1 > self.parent.data_lesson['lesson_duration']:
            count = 0
            k = self.parent.data_lesson['lesson_duration'] / sum_1
            for method in self.parent.my_methods:
                cur_time = int(round(int(method.method_time.text()[:-1]) * k, 0))
                count += cur_time
                method.method_time.setText(str(cur_time) + "'")

            self.parent.my_methods[-1].method_time.setText(str(
                int(self.parent.my_methods[-1].method_time.text()[:-1]) + self.parent.data_lesson[
                    'lesson_duration'] - count) + "'")
            sum_1 = sum([int(method.method_time.text()[:-1]) for method in self.parent.my_methods])

        self.parent.time_lesson.setText(
            "Время урока: " + str(self.parent.data_lesson['lesson_duration'] - sum_1) + " минут")

    def details(self):
        self.card_info = MethodMoreDetails(self.data, self.parent)
        self.card_info.show()


class MethodMoreDetails(QDialog):
    def __init__(self, data, parent):
        super(QDialog, self).__init__()
        self.setWindowIcon(QIcon(PATH_SPLASH_SCREEN))
        self.setModal(True)
        self.setWindowTitle(data.name_method[0].upper() + data.name_method[1:].lower())
        self.setFixedSize(int(parent.main_window.geometry.width() / 2), int(parent.main_window.geometry.height() / 2))
        self.parent = parent
        self.data = data
        self.initUI()

    def initUI(self):
        self.background = QLabel(self)
        self.background.setStyleSheet(
            '.QLabel {'
            'background-color: #76b7c7;'
            '}'
        )
        self.background.resize(int(self.parent.main_window.geometry.width() / 2),
                               int(self.parent.main_window.geometry.height() / 2))

        layout = QGridLayout(self)

        self.title_method = QLabel(self.data.name_method[0].upper() + self.data.name_method[1:].lower(), self)
        self.title_method.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.parent.main_window.normal.normal_font(42)}px;"
            "}"
        )
        self.title_method.setWordWrap(True)
        layout.addWidget(self.title_method, 0, 0, 1, 4)

        self.time_and_сlass_method = QLabel("   " + self.data.time + "' минут;    " + SESSION.query(Classes).filter(
            Classes.id == self.data.id_classes_number).first().name_class + " Класс   ", self)
        self.time_and_сlass_method.setStyleSheet(
            ".QLabel {"
            'background-color: #FFA25F;'
            f"font: bold {self.parent.main_window.normal.normal_font(32)}px;"
            "}"
        )
        layout.addWidget(self.time_and_сlass_method, 1, 1, 1, 4)

        text = ''
        if self.data.text:
            for word in self.data.text.split():
                if word[-1] == ")" and word[-2].isdigit():
                    text += "\n"
                text += word + " "
        self.text_card = QLabel(text, self)
        self.text_card.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.parent.main_window.normal.normal_font(18)}px;"
            "margin-bottom: 10%"
            "}"
        )
        self.text_card.setWordWrap(True)
        layout.addWidget(self.text_card, 2, 0)

        list_compet = [(self.data.creative_thinking, "- Креативное мышление"),
                       (self.data.critical_thinking, "- Критическое мышление"),
                       (self.data.literacy, "- Грамотность"),
                       (self.data.cooperation, "- Кооперация"),
                       (self.data.cooperation, "- Коммуникация"),
                       (self.data.metacognitive_skills, "- Метакогнитивные навыки")]
        list_compet = [i[1] for i in list_compet if i[0]]
        name_fgos = SESSION.query(Fgos).filter(Fgos.id == self.data.id_fgos).first().name_fgos
        if name_fgos != "-":
            list_compet.append("- " + name_fgos + " навыки ФГОС")
        self.competence = QLabel("\n".join(list_compet), self)
        self.competence.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.parent.main_window.normal.normal_font(22)}px;"
            "margin-right: 20%;"
            "}"
        )
        layout.addWidget(self.competence, 2, 3)


class ResultLesson(QWidget):
    back_constructor_event = pyqtSignal(dict)

    def __init__(self, main_window, data):
        super().__init__(main_window)
        self.data_constructor = data
        self.main_window = main_window
        self.setGeometry(0, 0, self.main_window.geometry.width(), self.main_window.geometry.height())

        self.initUI()

    def initUI(self):
        layout_result = QGridLayout(self)
        layout_result.setContentsMargins(int(self.window().width() / 25.5), int(self.window().width() / 25.5),
                                         int(self.window().width() / 25.5), int(self.window().width() / 25.5))

        layout_v_btn_result = QGridLayout(self)
        layout_v_btn_result.setContentsMargins(0, 0, int(self.window().width() / 25.5), 10)

        self.btn_back_result = QPushButton()
        self.btn_back_result.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back_result.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back_result.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        self.btn_back_result.clicked.connect(self.back_constructor)
        layout_v_btn_result.addWidget(self.btn_back_result, 0, 0, 1, 1)

        self.btn_ok_result = QPushButton()
        self.btn_ok_result.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}'
        )
        self.btn_ok_result.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok_result.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        layout_v_btn_result.addWidget(self.btn_ok_result, 0, 1, 1, 1)

        self.btn_save_lesson = QPushButton("Сохранить", self)
        self.btn_save_lesson.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.main_window.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.main_window.normal.normal_xy(200, 0)[0]}px;'
            'background-color: #76b7c7;'
            'border-style: outset;'
            'border-width: 2px;'
            'border-radius: 10px;'
            'border-color: beige;'
            'font: bold ' + self.main_window.normal.normal_font(17) + 'px;'
                                                                      'min-width: 10em;'
                                                                      'padding: 6px;'
                                                                      '}'
                                                                      '.QPushButton:hover {'
                                                                      'background-color: #548490;'
                                                                      'border-style: inset;'
                                                                      '}'
        )
        layout_v_btn_result.addWidget(self.btn_save_lesson, 1, 0, 1, 3)

        self.btn_print_lesson = QPushButton("Печать", self)
        self.btn_print_lesson.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.main_window.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.main_window.normal.normal_xy(200, 0)[0]}px;'
            'background-color: #76b7c7;'
            'border-style: outset;'
            'border-width: 2px;'
            'border-radius: 10px;'
            'border-color: beige;'
            'font: bold ' + self.main_window.normal.normal_font(17) + 'px;'
                                                                      'min-width: 10em;'
                                                                      'padding: 6px;'
                                                                      '}'
                                                                      '.QPushButton:hover {'
                                                                      'background-color: #548490;'
                                                                      'border-style: inset;'
                                                                      '}'
        )
        layout_v_btn_result.addWidget(self.btn_print_lesson, 2, 0, 1, 3)

        widget_btn_result = QWidget(self)
        widget_btn_result.setLayout(layout_v_btn_result)
        widget_btn_result.setStyleSheet(
            ".QWidget {background-color:transparent;}"
        )
        layout_result.addWidget(widget_btn_result, 0, 0, 1, 2)

        self.document_result = QTextEdit(self)
        layout_result.addWidget(self.document_result, 0, 2, 3, 5)

        self.setLayout(layout_result)

    def back_constructor(self):
        self.back_constructor_event.emit(
            {
                "lesson_topic": self.data_constructor["lesson_topic"],
                "subject": self.data_constructor["subject"],
                "lesson_type": self.data_constructor["lesson_type"],
                "class": self.data_constructor["class"],
                "class_characteristic": self.data_constructor["class_characteristic"],
                "lesson_duration": self.data_constructor["lesson_duration"],
                "acquaintance": self.data_constructor["acquaintance"],
                "competence": {
                    "creative_thinking": self.data_constructor["competence"]["creative_thinking"],
                    "literacy": self.data_constructor["competence"]["literacy"],
                    "communication": self.data_constructor["competence"]["communication"],
                    "cooperation": self.data_constructor["competence"]["cooperation"],
                    "critical_thinking": self.data_constructor["competence"]["critical_thinking"],
                    "metacognitive_skills": self.data_constructor["competence"]["metacognitive_skills"]
                }
            })


class NewMethod(QWidget):
    back_menu_event = pyqtSignal()

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setGeometry(int(self.main_window.geometry.width() / 6), int(self.main_window.geometry.height() / 6),
                         int(self.main_window.geometry.width() / 1.5), int(self.main_window.geometry.height() / 1.5))
        self.initUI()

    def initUI(self):
        self.background_form_options_new_method = QLabel(self)
        self.background_form_options_new_method.setStyleSheet(
            '.QLabel {'
            'background-color: #76b7c7;'
            'border-style: outset;'
            'border-width: 2px;'
            'border-radius: 10px;'
            'border-color: beige;'
            'min-width: 10em;'
            'padding: 6px;'
            '}'
        )
        self.background_form_options_new_method.resize(self.geometry().width(), self.geometry().height())

        self.text_method_topic = QLabel("Название")
        self.text_method_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_method_duration = QLabel("Длительность")
        self.text_method_duration.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_class_method = QLabel("Классы")
        self.text_class_method.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_method_type = QLabel("Тип")
        self.text_method_type.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_stage_method = QLabel("Этап урока")
        self.text_stage_method.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_fgos_method = QLabel("Фгос")
        self.text_fgos_method.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_competence_method = QLabel("Компетенции")
        self.text_competence_method.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_method_text = QLabel("Содержание")
        self.text_method_text.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # Поля ввода значений
        # -----------------------------------------
        self.edit_method_topic = QLineEdit()
        self.edit_method_topic.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.edit_method_duration = QSpinBox()
        self.edit_method_duration.setStyleSheet(
            ".QSpinBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.combo_class_method = QComboBox()
        self.combo_class_method.addItems([item.name_class for item in SESSION.query(Classes).all()])
        self.combo_class_method.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_method_type = QComboBox()
        self.combo_method_type.addItems([item.name_method for item in SESSION.query(TypeMethod).all()])
        self.combo_method_type.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_stage_method = QComboBox()
        self.combo_stage_method.addItems([item.name_stage for item in SESSION.query(Stage).all()])
        self.combo_stage_method.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_fgos_method = QComboBox()
        self.combo_fgos_method.addItems([item.name_fgos for item in SESSION.query(Fgos).all()])
        self.combo_fgos_method.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.check_communication = QCheckBox('Коммуникация')
        self.check_communication.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_literacy = QCheckBox('Грамотность')
        self.check_literacy.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_cooperation = QCheckBox('Кооперация')
        self.check_cooperation.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_creative_thinking = QCheckBox('Креативное мышление')
        self.check_creative_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_critical_thinking = QCheckBox('Критическое мышление')
        self.check_critical_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки')
        self.check_metacognitive_skills.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.text_method = QTextEdit()
        self.text_method.setStyleSheet(
            ".QTextEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )

        # -----------------------------------------
        self.btn_back_valid = QPushButton(self)
        self.btn_back_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back_valid.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back_valid.move(15, 5)
        self.btn_back_valid.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok_valid = QPushButton(self)
        self.btn_ok_valid.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}'
        )
        self.btn_ok_valid.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok_valid.move(self.geometry().width() - self.main_window.normal.normal_proportion(75, 0)[0] - 12, 5)
        self.btn_ok_valid.clicked.connect(self.valid_options_new_method)
        # -----------------------------------------

        layout_new_method = QGridLayout()
        layout_new_method.setContentsMargins(int(self.window().width() / 25.5), int(self.window().width() / 20.5),
                                             int(self.window().width() / 25.5), int(self.window().width() / 50.5))
        layout_new_method.addWidget(self.text_method_topic, 0, 0)
        layout_new_method.addWidget(self.edit_method_topic, 0, 1)

        layout_new_method.addWidget(self.text_method_duration, 1, 0)
        layout_new_method.addWidget(self.edit_method_duration, 1, 1)

        layout_new_method.addWidget(self.text_class_method, 2, 0)
        layout_new_method.addWidget(self.combo_class_method, 2, 1)

        layout_new_method.addWidget(self.text_method_type, 3, 0)
        layout_new_method.addWidget(self.combo_method_type, 3, 1)

        layout_new_method.addWidget(self.text_stage_method, 4, 0)
        layout_new_method.addWidget(self.combo_stage_method, 4, 1)

        layout_new_method.addWidget(self.text_fgos_method, 5, 0)
        layout_new_method.addWidget(self.combo_fgos_method, 5, 1)

        layout_new_method.addWidget(self.text_competence_method, 6, 0)

        layout_competence = QGridLayout()
        layout_competence.addWidget(self.check_communication, 1, 0)
        layout_competence.addWidget(self.check_literacy, 2, 0)
        layout_competence.addWidget(self.check_cooperation, 3, 0)
        layout_competence.addWidget(self.check_creative_thinking, 1, 1)
        layout_competence.addWidget(self.check_critical_thinking, 2, 1)
        layout_competence.addWidget(self.check_metacognitive_skills, 3, 1)

        widget_competence = QWidget()
        widget_competence.setLayout(layout_competence)
        widget_competence.setStyleSheet(
            ".QWidget {background-color:transparent;}"
        )
        layout_new_method.addWidget(widget_competence, 6, 1)

        layout_new_method.addWidget(self.text_method_text, 7, 0)
        layout_new_method.addWidget(self.text_method, 7, 1)

        self.setLayout(layout_new_method)

    def back_menu(self):
        self.back_menu_event.emit()

    def valid_options_new_method(self):
        if self.edit_method_topic.text() != "" and self.text_method.toPlainText() != "":
            new_method = Cards(
                name_method=self.edit_method_topic.text(),
                time=self.edit_method_duration.value(),
                id_classes_number=SESSION.query(Classes).filter(
                    Classes.name_class == self.combo_class_method.currentText()).first().id,
                id_type_method_card=SESSION.query(TypeMethod).filter(
                    TypeMethod.name_method == self.combo_method_type.currentText()).first().id,
                id_stage_card=SESSION.query(Stage).filter(
                    Stage.name_stage == self.combo_stage_method.currentText()).first().id,
                creative_thinking=self.check_creative_thinking.isChecked(),
                critical_thinking=self.check_critical_thinking.isChecked(),
                communication=self.check_communication.isChecked(),
                cooperation=self.check_cooperation.isChecked(),
                metacognitive_skills=self.check_metacognitive_skills.isChecked(),
                literacy=self.check_literacy.isChecked(),
                id_fgos=SESSION.query(Fgos).filter(Fgos.name_fgos == self.combo_fgos_method.currentText()).first().id,
                text=self.text_method.toPlainText(),
            )
            SESSION.add(new_method)
            SESSION.commit()
            QMessageBox.information(self, "Ок", "Метод Добавлен", QMessageBox.Ok)
            self.back_menu()
        else:
            QMessageBox.critical(self, "Ошибка", "Вы заполните все поля", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
