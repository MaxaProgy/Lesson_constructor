from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox, QPushButton, QLineEdit, QMessageBox, QListView, QRadioButton, \
    QButtonGroup, QScrollArea, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from data.type_method import TypeMethod
from data.stage import Stage
from data.classes import Classes
from data.fgos import Fgos
from data.cards import Cards
from data.class_characteristic import ClassCharacteristic
from data.subject import Subject
from data.lesson_type import LessonType


class Card(QWidget):
    def __init__(self, parent, info_card):
        super(Card, self).__init__(parent.parent)
        self.parent = parent
        self.info_card = info_card
        self.__controls()

    def __controls(self):
        self.label = QLabel()
        self.label.setStyleSheet('.QLabel {'
                                 'min-height: 300px;'
                                 'min-width: 500px;'
                                 'margin-right: 8px;'
                                 'margin-left: 8px;'
                                 'margin-bottom: 16px;'
                                 '}')
        pixmap = QPixmap('data/image/фоны/cards1.png')
        self.label.setPixmap(pixmap)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox)

        self.label_lesson_topic = QLabel(self.info_card.name_method, self)
        self.label_lesson_topic.setMinimumSize(300, 100)
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet('''
            .QLabel {
            font: bold 18px;
        }''')
        self.label_lesson_topic.move(60, 40)

        self.btn_add = QPushButton(self)
        self.btn_add.setStyleSheet('.QPushButton {border-image: url(data/image/add.png);}'
                                   '.QPushButton:hover {border-image: url(data/image/add2.png);}')
        self.btn_add.move(430, 245)
        self.btn_add.resize(40, 40)
        self.btn_add.show()

        self.btn_del = QPushButton(self)
        self.btn_del.setStyleSheet('.QPushButton {border-image: url(data/image/del.png);}'
                                   '.QPushButton:hover {border-image: url(data/image/del2.png);}')
        self.btn_del.move(430, 245)
        self.btn_del.resize(40, 40)
        self.btn_del.hide()

        self.btn_add.clicked.connect(self.add_card)
        self.btn_del.clicked.connect(self.del_card)

    def add_card(self):
        self.parent.my_list_card.append(self)
        self.show_my_cards()
        self.btn_add.hide()
        self.btn_del.show()

    def del_card(self):
        del self.parent.my_list_card[self.parent.my_list_card.index(self)]
        self.show_my_cards()
        self.parent.show_cards_stage()

    def show_my_cards(self):
        layout = QGridLayout()
        for card in self.parent.my_list_card:
            layout.addWidget(card)
        widget = QWidget()
        widget.setLayout(layout)
        widget.setStyleSheet(".QWidget {background-color:transparent;}")
        # scroll_main.setWidgetResizable(True)
        self.parent.scroll_my_lesson_card.setWidget(widget)
        self.parent.scroll_my_lesson_card.show()


class NewLesson:
    def __init__(self, parent):
        self.parent = parent
        self.flag_stage = 0
        self.list_card = []
        self.my_list_card = []

        # ------------------------------
        #  Объекты вкладки нового урока
        # ------------------------------

        # Фон для текстовых полей нового урока
        self.parent.background_new_lesson = QLabel(self.parent)
        self.parent.background_new_lesson.resize(900, 600)
        self.parent.background_new_lesson.move(self.parent.width_windows // 2 - 450,
                                               self.parent.height_windows // 2 - 300)
        self.parent.background_new_lesson.setStyleSheet('''
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

        # Тексты
        # -----------------------------------------
        self.parent.text_lesson_topic = QLabel("Тема урока", self.parent)
        self.parent.text_lesson_topic.resize(self.parent.text_lesson_topic.sizeHint())
        self.parent.text_lesson_topic.move(self.parent.width_windows // 2 - 400,
                                           self.parent.height_windows // 2 - 250)
        self.parent.text_lesson_topic.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_subjects = QLabel("Предмет", self.parent)
        self.parent.text_subjects.resize(self.parent.text_subjects.sizeHint())
        self.parent.text_subjects.move(self.parent.width_windows // 2 - 400,
                                       self.parent.height_windows // 2 - 170)
        self.parent.text_subjects.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_lesson_type = QLabel("Тип урока", self.parent)
        self.parent.text_lesson_type.resize(self.parent.text_lesson_type.sizeHint())
        self.parent.text_lesson_type.move(self.parent.width_windows // 2 - 400,
                                          self.parent.height_windows // 2 - 90)
        self.parent.text_lesson_type.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_class = QLabel("Класс", self.parent)
        self.parent.text_class.resize(self.parent.text_class.sizeHint())
        self.parent.text_class.move(self.parent.width_windows // 2 - 400, self.parent.height_windows // 2 - 10)
        self.parent.text_class.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_class_characteristic = QLabel("Характеристика класса", self.parent)
        self.parent.text_class_characteristic.resize(self.parent.text_class_characteristic.sizeHint())
        self.parent.text_class_characteristic.move(self.parent.width_windows // 2 - 400,
                                                   self.parent.height_windows // 2 + 70)
        self.parent.text_class_characteristic.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_lesson_duration = QLabel("Длительность урока", self.parent)
        self.parent.text_lesson_duration.resize(self.parent.text_lesson_duration.sizeHint())
        self.parent.text_lesson_duration.move(self.parent.width_windows // 2 - 400,
                                              self.parent.height_windows // 2 + 150)
        self.parent.text_lesson_duration.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_acquaintance = QLabel("Требуется знакомство?", self.parent)
        self.parent.text_acquaintance.resize(self.parent.text_acquaintance.sizeHint())
        self.parent.text_acquaintance.move(self.parent.width_windows // 2 - 20,
                                           self.parent.height_windows // 2 + 150)
        self.parent.text_acquaintance.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_competence = QLabel("Компетенции ", self.parent)
        self.parent.text_competence.resize(self.parent.text_competence.sizeHint())
        self.parent.text_competence.move(self.parent.width_windows // 2 - 400,
                                         self.parent.height_windows // 2 + 230)
        self.parent.text_competence.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        # Поля ввода значений
        # -----------------------------------------

        self.parent.edit_lesson_topic = QLineEdit(self.parent)
        self.parent.edit_lesson_topic.resize(480, 30)
        self.parent.edit_lesson_topic.move(self.parent.width_windows // 2 - 140,
                                           self.parent.height_windows // 2 - 260)
        self.parent.edit_lesson_topic.setStyleSheet('''
            .QLineEdit {
            font: bold 16px;
        }''')

        self.parent.combo_subjects = QComboBox(self.parent)
        self.parent.combo_subjects.addItems([item.name_subject for item
                                             in self.parent.session.query(Subject).all()])
        self.parent.combo_subjects.resize(480, 30)
        self.parent.combo_subjects.move(self.parent.width_windows // 2 - 140,
                                        self.parent.height_windows // 2 - 180)

        self.parent.combo_lesson_type = QComboBox(self.parent)
        self.parent.combo_lesson_type.addItems([item.name_lesson_type for item
                                                in self.parent.session.query(LessonType).all()])
        self.parent.combo_lesson_type.resize(480, 30)
        self.parent.combo_lesson_type.move(self.parent.width_windows // 2 - 140,
                                           self.parent.height_windows // 2 - 100)

        self.parent.combo_class = QComboBox(self.parent)
        self.parent.combo_class.addItems([item.name_class for item
                                          in self.parent.session.query(Classes).all()])
        self.parent.combo_class.resize(480, 30)
        self.parent.combo_class.move(self.parent.width_windows // 2 - 140, self.parent.height_windows // 2 - 20)

        self.parent.combo_class_characteristic = QComboBox(self.parent)
        self.parent.combo_class_characteristic.addItems([item.name_class_characteristic for item
                                                         in self.parent.session.query(ClassCharacteristic).all()])
        self.parent.combo_class_characteristic.resize(480, 30)
        self.parent.combo_class_characteristic.move(self.parent.width_windows // 2 - 140,
                                                    self.parent.height_windows // 2 + 60)

        self.parent.edit_lesson_duration = QLineEdit("40", self.parent)
        self.parent.edit_lesson_duration.resize(80, 30)
        self.parent.edit_lesson_duration.move(self.parent.width_windows // 2 - 130,
                                              self.parent.height_windows // 2 + 140)
        self.parent.edit_lesson_duration.setStyleSheet('''
            .QLineEdit {
            font: bold 16px;
        }''')

        self.parent.radio_btn_yes = QRadioButton('Да', self.parent)
        self.parent.radio_btn_yes.move(self.parent.width_windows // 2 + 200,
                                       self.parent.height_windows // 2 + 145)
        self.parent.radio_btn_yes.setStyleSheet('''
            .QRadioButton {
            font: bold 16px;
        }''')
        self.parent.radio_btn_no = QRadioButton('Нет', self.parent)
        self.parent.radio_btn_no.move(self.parent.width_windows // 2 + 260,
                                      self.parent.height_windows // 2 + 145)
        self.parent.radio_btn_no.setStyleSheet('''
            .QRadioButton {
            font: bold 16px;
        }''')
        self.parent.radio_btn_no.setChecked(True)
        self.parent.btn_radio_group = QButtonGroup()
        self.parent.btn_radio_group.addButton(self.parent.radio_btn_yes)
        self.parent.btn_radio_group.addButton(self.parent.radio_btn_no)

        self.parent.check_communication = QCheckBox('Коммуникация', self.parent)
        self.parent.check_communication.resize(200, 30)
        self.parent.check_communication.move(self.parent.width_windows // 2 - 140,
                                             self.parent.height_windows // 2 + 200)
        self.parent.check_communication.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')

        self.parent.check_literacy = QCheckBox('Грамотность', self.parent)
        self.parent.check_literacy.resize(200, 30)
        self.parent.check_literacy.move(self.parent.width_windows // 2 - 140,
                                        self.parent.height_windows // 2 + 220)
        self.parent.check_literacy.setStyleSheet('''
            .QCheckBox {
            font: bold 14px;
        }''')

        self.parent.check_cooperation = QCheckBox('Кооперация', self.parent)
        self.parent.check_cooperation.resize(200, 30)
        self.parent.check_cooperation.move(self.parent.width_windows // 2 - 140,
                                           self.parent.height_windows // 2 + 240)
        self.parent.check_cooperation.setStyleSheet('''
            .QCheckBox {
            font: bold 14px;
        }''')

        self.parent.check_creative_thinking = QCheckBox('Креативное мышление', self.parent)
        self.parent.check_creative_thinking.resize(200, 30)
        self.parent.check_creative_thinking.move(self.parent.width_windows // 2 + 60,
                                                 self.parent.height_windows // 2 + 200)
        self.parent.check_creative_thinking.setStyleSheet('''
                    .QCheckBox {
                    font: bold 14px;
                }''')

        self.parent.check_critical_thinking = QCheckBox('Критическое мышление', self.parent)
        self.parent.check_critical_thinking.resize(200, 30)
        self.parent.check_critical_thinking.move(self.parent.width_windows // 2 + 60,
                                                 self.parent.height_windows // 2 + 220)
        self.parent.check_critical_thinking.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')

        self.parent.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки', self.parent)
        self.parent.check_metacognitive_skills.resize(200, 30)
        self.parent.check_metacognitive_skills.move(self.parent.width_windows // 2 + 60,
                                                    self.parent.height_windows // 2 + 240)
        self.parent.check_metacognitive_skills.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')

        self.parent.value_lesson = QListView(self.parent)
        self.parent.value_lesson.resize(530, 200)
        self.parent.value_lesson.move(self.parent.width_windows - 550, 5)

        self.scroll_main = QScrollArea(self.parent)
        self.scroll_main.setStyleSheet(".QScrollArea {background-color:transparent;"
                                       "}")
        self.scroll_main.move(270, 80)
        self.scroll_main.resize(self.parent.width_windows - 820, self.parent.height_windows - 200)
        self.scroll_main.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_main.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_my_lesson_card = QScrollArea(self.parent)
        self.scroll_my_lesson_card.setStyleSheet(".QScrollArea {background-color:transparent;"
                                                 "}")
        self.scroll_my_lesson_card.move(self.parent.width_windows - 550, 204)
        self.scroll_my_lesson_card.resize(530, 800)
        self.scroll_my_lesson_card.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_my_lesson_card.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # -----------------------------------------
        #                Кнопки
        # -----------------------------------------

        self.parent.btn_back_valid = QPushButton(self.parent)
        self.parent.btn_back_valid.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                 '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.parent.btn_back_valid.move(self.parent.width_windows // 2 + 390,
                                        self.parent.height_windows // 2 - 350)
        self.parent.btn_back_valid.resize(55, 40)

        self.parent.btn_ok_valid = QPushButton(self.parent)
        self.parent.btn_ok_valid.setStyleSheet('.QPushButton {border-image: url(data/image/ок.png);}'
                                               '.QPushButton:hover {border-image: url(data/image/ок2.png);}')
        self.parent.btn_ok_valid.move(self.parent.width_windows // 2 + 350, self.parent.height_windows - 310)
        self.parent.btn_ok_valid.resize(63, 60)

        # -----------------------------------------

        self.parent.btn_back_constructor = QPushButton(self.parent)
        self.parent.btn_back_constructor.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                       '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.parent.btn_back_constructor.move(self.parent.width_windows - 700, 12)
        self.parent.btn_back_constructor.resize(55, 40)

        self.parent.btn_ok_constructor = QPushButton(self.parent)
        self.parent.btn_ok_constructor.setStyleSheet('.QPushButton {border-image: url(data/image/ок.png);}'
                                                     '.QPushButton:hover {border-image: url(data/image/ок2.png);}')
        self.parent.btn_ok_constructor.move(self.parent.width_windows - 630, 3)
        self.parent.btn_ok_constructor.resize(63, 60)

        # -----------------------------------------

        self.parent.btn_stage_acquaintance = QPushButton("Знакомство", self.parent)
        self.parent.btn_stage_acquaintance.setStyleSheet('''
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

        self.parent.btn_team_building = QPushButton("Командообразование", self.parent)
        self.parent.btn_team_building.setStyleSheet('''
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

        self.parent.btn_new_material = QPushButton("Новый материал", self.parent)
        self.parent.btn_new_material.setStyleSheet('''
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

        self.parent.btn_refreshments = QPushButton("Бодрилки", self.parent)
        self.parent.btn_refreshments.setStyleSheet('''
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

        self.parent.btn_test_of_understanding = QPushButton("Проверка понимания", self.parent)
        self.parent.btn_test_of_understanding.setStyleSheet('''
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

        self.parent.btn_material_fixing = QPushButton("Закрепление материала", self.parent)
        self.parent.btn_material_fixing.setStyleSheet('''
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

        self.parent.btn_assimilation_control = QPushButton("Контроль усвоения", self.parent)
        self.parent.btn_assimilation_control.setStyleSheet('''
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

        self.parent.btn_reflection = QPushButton("Рефлексия", self.parent)
        self.parent.btn_reflection.setStyleSheet('''
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

        self.parent.btn_homework = QPushButton("Домашнее задание", self.parent)
        self.parent.btn_homework.setStyleSheet('''
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

        self.group_button_stage = QButtonGroup(self.parent)
        self.group_button_stage.addButton(self.parent.btn_stage_acquaintance)
        self.group_button_stage.addButton(self.parent.btn_team_building)
        self.group_button_stage.addButton(self.parent.btn_new_material)
        self.group_button_stage.addButton(self.parent.btn_refreshments)
        self.group_button_stage.addButton(self.parent.btn_test_of_understanding)
        self.group_button_stage.addButton(self.parent.btn_material_fixing)
        self.group_button_stage.addButton(self.parent.btn_assimilation_control)
        self.group_button_stage.addButton(self.parent.btn_reflection)
        self.group_button_stage.addButton(self.parent.btn_homework)

        self.group_button_stage.buttonClicked.connect(self.stage_button_flag)

        # -----------------------------------------
        self.parent.btn_ok_valid.clicked.connect(self.valid_new_lesson_and_show_info)
        self.parent.btn_back_valid.clicked.connect(self.open_main_menu)
        self.parent.btn_back_constructor.clicked.connect(self.open_new_lesson)

        self.parent.btn_new_lesson.hide()
        self.open_new_lesson()

    def open_main_menu(self):
        self.hide_object_new_lesson()
        self.parent.main_menu()

    def open_new_lesson(self):
        pixmap = QPixmap('data/image/фоны/общий_фон.jpg')
        self.parent.background.setPixmap(pixmap)
        self.hide_object_constructor_field()
        self.show_object_new_lesson()

    def valid_new_lesson_and_show_info(self):
        if self.parent.edit_lesson_topic.text() != "" and \
                int(self.parent.edit_lesson_duration.text()) >= 20 and \
                (self.parent.check_creative_thinking.isChecked() or
                 self.parent.check_literacy.isChecked() or
                 self.parent.check_communication.isChecked() or
                 self.parent.check_cooperation.isChecked() or
                 self.parent.check_critical_thinking.isChecked() or
                 self.parent.check_metacognitive_skills.isChecked()):
            self.constructor_field()
        else:
            QMessageBox.critical(self.parent, "Ошибка", "Вы заполните все поля", QMessageBox.Ok)

    def constructor_field(self):
        pixmap = QPixmap('data/image/фоны/фон_конструктора.jpg')
        self.parent.background.setPixmap(pixmap)
        self.hide_object_new_lesson()
        self.show_object_constructor_field()
        if self.parent.radio_btn_no.isChecked():
            self.parent.btn_stage_acquaintance.hide()

            self.parent.btn_team_building.resize(200, 85)
            self.parent.btn_new_material.resize(200, 85)
            self.parent.btn_refreshments.resize(200, 85)
            self.parent.btn_test_of_understanding.resize(200, 85)
            self.parent.btn_material_fixing.resize(200, 85)
            self.parent.btn_assimilation_control.resize(200, 85)
            self.parent.btn_reflection.resize(200, 85)
            self.parent.btn_homework.resize(200, 85)
            self.parent.btn_assimilation_control.resize(200, 85)

            self.parent.btn_team_building.move(50, 140)
            self.parent.btn_new_material.move(50, 230)
            self.parent.btn_refreshments.move(50, 320)
            self.parent.btn_test_of_understanding.move(50, 410)
            self.parent.btn_material_fixing.move(50, 500)
            self.parent.btn_assimilation_control.move(50, 590)
            self.parent.btn_reflection.move(50, 680)
            self.parent.btn_homework.move(50, 770)
        else:
            self.parent.btn_stage_acquaintance.show()

            self.parent.btn_stage_acquaintance.resize(200, 80)
            self.parent.btn_team_building.resize(200, 80)
            self.parent.btn_new_material.resize(200, 80)
            self.parent.btn_refreshments.resize(200, 80)
            self.parent.btn_test_of_understanding.resize(200, 80)
            self.parent.btn_material_fixing.resize(200, 80)
            self.parent.btn_reflection.resize(200, 80)
            self.parent.btn_homework.resize(200, 80)
            self.parent.btn_assimilation_control.resize(200, 80)

            self.parent.btn_stage_acquaintance.move(50, 140)
            self.parent.btn_team_building.move(50, 225)
            self.parent.btn_new_material.move(50, 310)
            self.parent.btn_refreshments.move(50, 395)
            self.parent.btn_test_of_understanding.move(50, 480)
            self.parent.btn_material_fixing.move(50, 565)
            self.parent.btn_assimilation_control.move(50, 650)
            self.parent.btn_reflection.move(50, 735)
            self.parent.btn_homework.move(50, 820)

        title_value = [('Тема урока', self.parent.edit_lesson_topic.text()),
                       ('Предмет', self.parent.combo_subjects.currentText()),
                       ('Тип урока', self.parent.combo_lesson_type.currentText()),
                       ('Класс', self.parent.combo_class.currentText()),
                       ('Характеристика класса', self.parent.combo_class_characteristic.currentText()),
                       ('Длительность', self.parent.edit_lesson_duration.text()),
                       ('Креативное мышление', self.parent.check_creative_thinking.isChecked()),
                       ('Клитическое мышление', self.parent.check_critical_thinking.isChecked()),
                       ('Грамотность', self.parent.check_literacy.isChecked()),
                       ('Кооперация', self.parent.check_cooperation.isChecked()),
                       ('Коммуникация', self.parent.check_communication.isChecked()),
                       ('Метакогнитивные навыки', self.parent.check_metacognitive_skills.isChecked())]
        model = QStandardItemModel()
        self.parent.value_lesson.setModel(model)
        for i in title_value:
            if type(i[1]) == bool:
                if i[1]:
                    item = QStandardItem(i[0] + " - \u2713")
                    item.setEditable(False)
                    model.appendRow(item)
            else:
                item = QStandardItem(i[0] + " - " + i[1])
                item.setEditable(False)
                model.appendRow(item)

        self.show_cards_stage()

    def show_cards_stage(self):
        list_cards = self.parent.session.query(Cards).filter(Cards.id_stage_card.like(self.flag_stage)).all()
        layout = QGridLayout()

        for i in reversed(range(len(self.list_card))):
            del self.list_card[i]

        list_id_my_card = [card.info_card.id for card in self.my_list_card]
        print(list_id_my_card)
        for i in reversed(range(len(list_cards))):
            if list_cards[i].id in list_id_my_card:
                del list_cards[i]

        for i in range(len(list_cards)):
            self.list_card.append(Card(self, list_cards[i]))
            layout.addWidget(self.list_card[i], i // 2, i % 2)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setStyleSheet(".QWidget {background-color:transparent;}")

        # scroll_main.setWidgetResizable(True)
        self.scroll_main.setWidget(widget)
        self.scroll_main.show()
        self.scroll_my_lesson_card.show()

    def stage_button_flag(self, button):
        self.flag_stage = self.parent.session.query(Stage).filter(Stage.name_stage == button.text()).first().id
        self.show_cards_stage()

    def show_object_constructor_field(self):
        self.parent.btn_ok_constructor.show()
        self.parent.btn_back_constructor.show()
        self.parent.btn_stage_acquaintance.show()
        self.parent.btn_team_building.show()
        self.parent.btn_new_material.show()
        self.parent.btn_refreshments.show()
        self.parent.btn_test_of_understanding.show()
        self.parent.btn_material_fixing.show()
        self.parent.btn_assimilation_control.show()
        self.parent.btn_reflection.show()
        self.parent.btn_homework.show()
        self.parent.value_lesson.show()
        self.scroll_main.show()
        self.scroll_my_lesson_card.show()

    def hide_object_constructor_field(self):
        self.parent.btn_ok_constructor.hide()
        self.parent.btn_back_constructor.hide()
        self.parent.btn_stage_acquaintance.hide()
        self.parent.btn_team_building.hide()
        self.parent.btn_new_material.hide()
        self.parent.btn_refreshments.hide()
        self.parent.btn_test_of_understanding.hide()
        self.parent.btn_material_fixing.hide()
        self.parent.btn_assimilation_control.hide()
        self.parent.btn_reflection.hide()
        self.parent.btn_homework.hide()
        self.parent.value_lesson.hide()
        self.scroll_main.hide()
        self.scroll_my_lesson_card.hide()

    def show_object_new_lesson(self):
        self.parent.background_new_lesson.show()

        self.parent.text_lesson_topic.show()
        self.parent.text_subjects.show()
        self.parent.text_lesson_type.show()
        self.parent.text_class.show()
        self.parent.text_class_characteristic.show()
        self.parent.text_lesson_duration.show()
        self.parent.text_acquaintance.show()
        self.parent.text_competence.show()
        self.parent.edit_lesson_topic.show()
        self.parent.radio_btn_no.show()
        self.parent.radio_btn_yes.show()
        self.parent.combo_subjects.show()
        self.parent.combo_lesson_type.show()
        self.parent.combo_class.show()
        self.parent.combo_class_characteristic.show()
        self.parent.edit_lesson_duration.show()
        self.parent.check_creative_thinking.show()
        self.parent.check_literacy.show()
        self.parent.check_cooperation.show()
        self.parent.check_communication.show()
        self.parent.check_critical_thinking.show()
        self.parent.check_metacognitive_skills.show()

        self.parent.btn_back_valid.show()
        self.parent.btn_ok_valid.show()

    def hide_object_new_lesson(self):
        self.parent.background_new_lesson.hide()

        self.parent.text_lesson_topic.hide()
        self.parent.text_subjects.hide()
        self.parent.text_lesson_type.hide()
        self.parent.text_class.hide()
        self.parent.text_class_characteristic.hide()
        self.parent.text_lesson_duration.hide()
        self.parent.text_acquaintance.hide()
        self.parent.text_competence.hide()
        self.parent.edit_lesson_topic.hide()
        self.parent.radio_btn_no.hide()
        self.parent.radio_btn_yes.hide()
        self.parent.combo_subjects.hide()
        self.parent.combo_lesson_type.hide()
        self.parent.combo_class.hide()
        self.parent.combo_class_characteristic.hide()
        self.parent.edit_lesson_duration.hide()
        self.parent.check_creative_thinking.hide()
        self.parent.check_literacy.hide()
        self.parent.check_cooperation.hide()
        self.parent.check_communication.hide()
        self.parent.check_critical_thinking.hide()
        self.parent.check_metacognitive_skills.hide()

        self.parent.btn_back_valid.hide()
        self.parent.btn_ok_valid.hide()
