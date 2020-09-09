# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, \
    QSplashScreen, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox
from PyQt5 import uic, QtGui, QtCore
import time


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
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

        # ------------------------------
        #  Объекты вкладки нового урока
        # ------------------------------

        # Фон для текстовых полей нового урока
        self.background_new_lesson = QLabel(self)
        self.background_new_lesson.resize(900, 600)
        self.background_new_lesson.move(self.geometry.width() // 2 - 450, self.geometry.height() // 2 - 300)
        self.background_new_lesson.setStyleSheet('''
            .QLabel {
            background-color: #6ca9b9;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
        }''')
        self.background_new_lesson.hide()

        # Тексты
        self.text_lesson_topic = QLabel("Тема урока", self)
        self.text_lesson_topic.resize(self.text_lesson_topic.sizeHint())
        self.text_lesson_topic.move(self.geometry.width() // 2 - 400, self.geometry.height() // 2 - 250)
        self.text_lesson_topic.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_lesson_topic.hide()

        self.text_subjects = QLabel("Предмет", self)
        self.text_subjects.resize(self.text_subjects.sizeHint())
        self.text_subjects.move(self.geometry.width() // 2 - 400, self.geometry.height() // 2 - 170)
        self.text_subjects.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_subjects.hide()

        self.text_lesson_type = QLabel("Тип урока", self)
        self.text_lesson_type.resize(self.text_lesson_type.sizeHint())
        self.text_lesson_type.move(self.geometry.width() // 2 - 400, self.geometry.height() // 2 - 90)
        self.text_lesson_type.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_lesson_type.hide()

        self.text_class = QLabel("Класс", self)
        self.text_class.resize(self.text_class.sizeHint())
        self.text_class.move(self.geometry.width() // 2 - 400, self.geometry.height() // 2 - 10)
        self.text_class.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_class.hide()

        self.text_class_characteristic = QLabel("Характеристика класса", self)
        self.text_class_characteristic.resize(self.text_class_characteristic.sizeHint())
        self.text_class_characteristic.move(self.geometry.width() // 2 - 400, self.geometry.height() // 2 + 70)
        self.text_class_characteristic.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_class_characteristic.hide()

        self.text_lesson_duration = QLabel("Длительность урока", self)
        self.text_lesson_duration.resize(self.text_lesson_duration.sizeHint())
        self.text_lesson_duration.move(self.geometry.width() // 2 - 400, self.geometry.height() // 2 + 150)
        self.text_lesson_duration.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_lesson_duration.hide()

        self.text_lesson_duration_2 = QLabel("Минут", self)
        self.text_lesson_duration_2.resize(self.text_lesson_duration_2.sizeHint())
        self.text_lesson_duration_2.move(self.geometry.width() // 2 - 50, self.geometry.height() // 2 + 150)
        self.text_lesson_duration_2.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_lesson_duration_2.hide()

        self.text_competence = QLabel("Компетенции ", self)
        self.text_competence.resize(self.text_competence.sizeHint())
        self.text_competence.move(self.geometry.width() // 2 - 400, self.geometry.height() // 2 + 230)
        self.text_competence.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')
        self.text_competence.hide()

        self.edit_lesson_topic = QLineEdit(self)
        self.edit_lesson_topic.resize(480, 30)
        self.edit_lesson_topic.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 - 260)
        self.edit_lesson_topic.setStyleSheet('''
            .QLineEdit {
            font: bold 16px;
        }''')
        self.edit_lesson_topic.hide()

        self.combo_subjects = QComboBox(self)
        self.combo_subjects.addItems(["Ubuntu", "Mandriva",
                                      "Fedora", "Arch", "Gentoo"])
        self.combo_subjects.resize(480, 30)
        self.combo_subjects.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 - 180)
        self.combo_subjects.hide()

        self.combo_lesson_type = QComboBox(self)
        self.combo_lesson_type.addItems(["Ubuntu", "Mandriva",
                                         "Fedora", "Arch", "Gentoo"])
        self.combo_lesson_type.resize(480, 30)
        self.combo_lesson_type.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 - 100)
        self.combo_lesson_type.hide()

        self.combo_class = QComboBox(self)
        self.combo_class.addItems(["Ubuntu", "Mandriva",
                                   "Fedora", "Arch", "Gentoo"])
        self.combo_class.resize(480, 30)
        self.combo_class.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 - 20)
        self.combo_class.hide()

        self.combo_class_characteristic = QComboBox(self)
        self.combo_class_characteristic.addItems(["Ubuntu", "Mandriva",
                                                  "Fedora", "Arch", "Gentoo"])
        self.combo_class_characteristic.resize(480, 30)
        self.combo_class_characteristic.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 + 60)
        self.combo_class_characteristic.hide()

        self.edit_lesson_duration = QLineEdit("40", self)
        self.edit_lesson_duration.resize(80, 30)
        self.edit_lesson_duration.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 + 140)
        self.edit_lesson_duration.setStyleSheet('''
            .QLineEdit {
            font: bold 16px;
        }''')
        self.edit_lesson_duration.hide()

        self.check_communication = QCheckBox('Коммуникация', self)
        self.check_communication.resize(200, 30)
        self.check_communication.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 + 200)
        self.check_communication.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')
        self.check_communication.hide()

        self.check_literacy = QCheckBox('Грамотность', self)
        self.check_literacy.resize(200, 30)
        self.check_literacy.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 + 220)
        self.check_literacy.setStyleSheet('''
            .QCheckBox {
            font: bold 14px;
        }''')
        self.check_literacy.hide()

        self.check_cooperation = QCheckBox('Кооперация', self)
        self.check_cooperation.resize(200, 30)
        self.check_cooperation.move(self.geometry.width() // 2 - 140, self.geometry.height() // 2 + 240)
        self.check_cooperation.setStyleSheet('''
            .QCheckBox {
            font: bold 14px;
        }''')
        self.check_cooperation.hide()

        self.check_creative_thinking = QCheckBox('Креативное мышление', self)
        self.check_creative_thinking.resize(200, 30)
        self.check_creative_thinking.move(self.geometry.width() // 2 + 60, self.geometry.height() // 2 + 200)
        self.check_creative_thinking.setStyleSheet('''
                    .QCheckBox {
                    font: bold 14px;
                }''')
        self.check_creative_thinking.hide()

        self.check_critical_thinking = QCheckBox('Критическое мышление', self)
        self.check_critical_thinking.resize(200, 30)
        self.check_critical_thinking.move(self.geometry.width() // 2 + 60, self.geometry.height() // 2 + 220)
        self.check_critical_thinking.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')
        self.check_critical_thinking.hide()

        self.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки', self)
        self.check_metacognitive_skills.resize(200, 30)
        self.check_metacognitive_skills.move(self.geometry.width() // 2 + 60, self.geometry.height() // 2 + 240)
        self.check_metacognitive_skills.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')
        self.check_metacognitive_skills.hide()

        self.btn_back = QPushButton(self)
        self.btn_back.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}')
        self.btn_back.move(self.geometry.width() // 2 + 390, self.geometry.height() // 2 - 350)
        self.btn_back.resize(55, 40)
        self.btn_back.hide()

        self.btn_new_lesson.clicked.connect(self.new_lesson)
        self.btn_back.clicked.connect(self.menu)
        self.menu()

    def menu(self):
        self.hide_object_new_lesson()
        self.setStyleSheet('.QWidget {background-image: url(data/image/фоны/меню.jpg);}')
        self.show_object_menu()

    def new_lesson(self):
        self.setStyleSheet('.QWidget {background-image: url(data/image/фоны/общий_фон.jpg);}')
        self.btn_new_lesson.hide()
        self.show_object_new_lesson()

    def show_object_menu(self):
        self.btn_new_lesson.show()

    def show_object_new_lesson(self):
        self.background_new_lesson.show()
        self.text_lesson_topic.show()
        self.text_subjects.show()
        self.text_lesson_type.show()
        self.text_class.show()
        self.text_class_characteristic.show()
        self.text_lesson_duration.show()
        self.text_lesson_duration_2.show()
        self.text_competence.show()
        self.edit_lesson_topic.show()
        self.combo_subjects.show()
        self.combo_lesson_type.show()
        self.combo_class.show()
        self.combo_class_characteristic.show()
        self.edit_lesson_duration.show()
        self.check_creative_thinking.show()
        self.check_literacy.show()
        self.check_cooperation.show()
        self.check_communication.show()
        self.check_critical_thinking.show()
        self.check_metacognitive_skills.show()
        self.btn_back.show()

    def hide_object_new_lesson(self):
        self.background_new_lesson.hide()
        self.text_lesson_topic.hide()
        self.text_subjects.hide()
        self.text_lesson_type.hide()
        self.text_class.hide()
        self.text_class_characteristic.hide()
        self.text_lesson_duration.hide()
        self.text_lesson_duration_2.hide()
        self.text_competence.hide()
        self.edit_lesson_topic.hide()
        self.combo_subjects.hide()
        self.combo_lesson_type.hide()
        self.combo_class.hide()
        self.combo_class_characteristic.hide()
        self.edit_lesson_duration.hide()
        self.check_creative_thinking.hide()
        self.check_literacy.hide()
        self.check_cooperation.hide()
        self.check_communication.hide()
        self.check_critical_thinking.hide()
        self.check_metacognitive_skills.hide()
        self.btn_back.hide()


app = QApplication(sys.argv)
ex = Menu()

# Заставка
splash = QSplashScreen(QtGui.QPixmap('data/image/фоны/заставка.png'), QtCore.Qt.WindowStaysOnTopHint)
splash.show()
time.sleep(1)
splash.close()

ex.show()
sys.exit(app.exec_())
