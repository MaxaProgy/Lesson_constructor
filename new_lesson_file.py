from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox, QPushButton, QLineEdit, QMessageBox, QListView, QRadioButton, \
    QButtonGroup


class NewLesson:
    def __init__(self, parent):
        self.parent = parent
        # ------------------------------
        #  Объекты вкладки нового урока
        # ------------------------------

        # Фон для текстовых полей нового урока
        self.parent.background_new_lesson = QLabel(self.parent)
        self.parent.background_new_lesson.resize(900, 600)
        self.parent.background_new_lesson.move(self.parent.geometry.width() // 2 - 450,
                                               self.parent.geometry.height() // 2 - 300)
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
        self.parent.text_lesson_topic.move(self.parent.geometry.width() // 2 - 400,
                                           self.parent.geometry.height() // 2 - 250)
        self.parent.text_lesson_topic.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_subjects = QLabel("Предмет", self.parent)
        self.parent.text_subjects.resize(self.parent.text_subjects.sizeHint())
        self.parent.text_subjects.move(self.parent.geometry.width() // 2 - 400,
                                       self.parent.geometry.height() // 2 - 170)
        self.parent.text_subjects.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_lesson_type = QLabel("Тип урока", self.parent)
        self.parent.text_lesson_type.resize(self.parent.text_lesson_type.sizeHint())
        self.parent.text_lesson_type.move(self.parent.geometry.width() // 2 - 400,
                                          self.parent.geometry.height() // 2 - 90)
        self.parent.text_lesson_type.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_class = QLabel("Класс", self.parent)
        self.parent.text_class.resize(self.parent.text_class.sizeHint())
        self.parent.text_class.move(self.parent.geometry.width() // 2 - 400, self.parent.geometry.height() // 2 - 10)
        self.parent.text_class.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_class_characteristic = QLabel("Характеристика класса", self.parent)
        self.parent.text_class_characteristic.resize(self.parent.text_class_characteristic.sizeHint())
        self.parent.text_class_characteristic.move(self.parent.geometry.width() // 2 - 400,
                                                   self.parent.geometry.height() // 2 + 70)
        self.parent.text_class_characteristic.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_lesson_duration = QLabel("Длительность урока", self.parent)
        self.parent.text_lesson_duration.resize(self.parent.text_lesson_duration.sizeHint())
        self.parent.text_lesson_duration.move(self.parent.geometry.width() // 2 - 400,
                                              self.parent.geometry.height() // 2 + 150)
        self.parent.text_lesson_duration.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_acquaintance = QLabel("Требуется знакомство?", self.parent)
        self.parent.text_acquaintance.resize(self.parent.text_acquaintance.sizeHint())
        self.parent.text_acquaintance.move(self.parent.geometry.width() // 2 - 20,
                                           self.parent.geometry.height() // 2 + 150)
        self.parent.text_acquaintance.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        self.parent.text_competence = QLabel("Компетенции ", self.parent)
        self.parent.text_competence.resize(self.parent.text_competence.sizeHint())
        self.parent.text_competence.move(self.parent.geometry.width() // 2 - 400,
                                         self.parent.geometry.height() // 2 + 230)
        self.parent.text_competence.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 12em;
        }''')

        # Поля ввода значений
        # -----------------------------------------

        self.parent.edit_lesson_topic = QLineEdit(self.parent)
        self.parent.edit_lesson_topic.resize(480, 30)
        self.parent.edit_lesson_topic.move(self.parent.geometry.width() // 2 - 140,
                                           self.parent.geometry.height() // 2 - 260)
        self.parent.edit_lesson_topic.setStyleSheet('''
            .QLineEdit {
            font: bold 16px;
        }''')

        self.parent.combo_subjects = QComboBox(self.parent)
        self.parent.combo_subjects.addItems(["Ubuntu", "Mandriva",
                                             "Fedora", "Arch", "Gentoo"])
        self.parent.combo_subjects.resize(480, 30)
        self.parent.combo_subjects.move(self.parent.geometry.width() // 2 - 140,
                                        self.parent.geometry.height() // 2 - 180)

        self.parent.combo_lesson_type = QComboBox(self.parent)
        self.parent.combo_lesson_type.addItems(["Ubuntu", "Mandriva",
                                                "Fedora", "Arch", "Gentoo"])
        self.parent.combo_lesson_type.resize(480, 30)
        self.parent.combo_lesson_type.move(self.parent.geometry.width() // 2 - 140,
                                           self.parent.geometry.height() // 2 - 100)

        self.parent.combo_class = QComboBox(self.parent)
        self.parent.combo_class.addItems(["Ubuntu", "Mandriva",
                                          "Fedora", "Arch", "Gentoo"])
        self.parent.combo_class.resize(480, 30)
        self.parent.combo_class.move(self.parent.geometry.width() // 2 - 140, self.parent.geometry.height() // 2 - 20)

        self.parent.combo_class_characteristic = QComboBox(self.parent)
        self.parent.combo_class_characteristic.addItems(["Ubuntu", "Mandriva",
                                                         "Fedora", "Arch", "Gentoo"])
        self.parent.combo_class_characteristic.resize(480, 30)
        self.parent.combo_class_characteristic.move(self.parent.geometry.width() // 2 - 140,
                                                    self.parent.geometry.height() // 2 + 60)

        self.parent.edit_lesson_duration = QLineEdit("40", self.parent)
        self.parent.edit_lesson_duration.resize(80, 30)
        self.parent.edit_lesson_duration.move(self.parent.geometry.width() // 2 - 130,
                                              self.parent.geometry.height() // 2 + 140)
        self.parent.edit_lesson_duration.setStyleSheet('''
            .QLineEdit {
            font: bold 16px;
        }''')

        self.parent.radio_btn_yes = QRadioButton('Да', self.parent)
        self.parent.radio_btn_yes.move(self.parent.geometry.width() // 2 + 200,
                                       self.parent.geometry.height() // 2 + 145)
        self.parent.radio_btn_yes.setStyleSheet('''
            .QRadioButton {
            font: bold 16px;
        }''')
        self.parent.radio_btn_no = QRadioButton('Нет', self.parent)
        self.parent.radio_btn_no.move(self.parent.geometry.width() // 2 + 260,
                                      self.parent.geometry.height() // 2 + 145)
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
        self.parent.check_communication.move(self.parent.geometry.width() // 2 - 140,
                                             self.parent.geometry.height() // 2 + 200)
        self.parent.check_communication.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')

        self.parent.check_literacy = QCheckBox('Грамотность', self.parent)
        self.parent.check_literacy.resize(200, 30)
        self.parent.check_literacy.move(self.parent.geometry.width() // 2 - 140,
                                        self.parent.geometry.height() // 2 + 220)
        self.parent.check_literacy.setStyleSheet('''
            .QCheckBox {
            font: bold 14px;
        }''')

        self.parent.check_cooperation = QCheckBox('Кооперация', self.parent)
        self.parent.check_cooperation.resize(200, 30)
        self.parent.check_cooperation.move(self.parent.geometry.width() // 2 - 140,
                                           self.parent.geometry.height() // 2 + 240)
        self.parent.check_cooperation.setStyleSheet('''
            .QCheckBox {
            font: bold 14px;
        }''')

        self.parent.check_creative_thinking = QCheckBox('Креативное мышление', self.parent)
        self.parent.check_creative_thinking.resize(200, 30)
        self.parent.check_creative_thinking.move(self.parent.geometry.width() // 2 + 60,
                                                 self.parent.geometry.height() // 2 + 200)
        self.parent.check_creative_thinking.setStyleSheet('''
                    .QCheckBox {
                    font: bold 14px;
                }''')

        self.parent.check_critical_thinking = QCheckBox('Критическое мышление', self.parent)
        self.parent.check_critical_thinking.resize(200, 30)
        self.parent.check_critical_thinking.move(self.parent.geometry.width() // 2 + 60,
                                                 self.parent.geometry.height() // 2 + 220)
        self.parent.check_critical_thinking.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')

        self.parent.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки', self.parent)
        self.parent.check_metacognitive_skills.resize(200, 30)
        self.parent.check_metacognitive_skills.move(self.parent.geometry.width() // 2 + 60,
                                                    self.parent.geometry.height() // 2 + 240)
        self.parent.check_metacognitive_skills.setStyleSheet('''
                .QCheckBox {
                font: bold 14px;
            }''')

        self.parent.value_lesson = QListView(self.parent)
        self.parent.value_lesson.resize(415, 200)
        self.parent.value_lesson.move(self.parent.geometry.width() - 435, 5)

        self.parent.text_lesson_topic_constructor = QLabel(self.parent)
        self.parent.text_lesson_topic_constructor.resize(self.parent.text_lesson_topic_constructor.sizeHint())
        self.parent.text_lesson_topic_constructor.move(self.parent.geometry.width() - 430, 250)
        self.parent.text_lesson_topic_constructor.setStyleSheet('''
            .QLabel {
            font: bold 16px;
            min-width: 22em;
        }''')
        # -----------------------------------------
        #                Кнопки
        # -----------------------------------------

        self.parent.btn_back_valid = QPushButton(self.parent)
        self.parent.btn_back_valid.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                 '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.parent.btn_back_valid.move(self.parent.geometry.width() // 2 + 390,
                                        self.parent.geometry.height() // 2 - 350)
        self.parent.btn_back_valid.resize(55, 40)

        self.parent.btn_ok_valid = QPushButton(self.parent)
        self.parent.btn_ok_valid.setStyleSheet('.QPushButton {border-image: url(data/image/ок.png);}'
                                               '.QPushButton:hover {border-image: url(data/image/ок2.png);}')
        self.parent.btn_ok_valid.move(self.parent.geometry.width() // 2 + 350, self.parent.geometry.height() - 310)
        self.parent.btn_ok_valid.resize(63, 60)

        # -----------------------------------------

        self.parent.btn_back_constructor = QPushButton(self.parent)
        self.parent.btn_back_constructor.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                       '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.parent.btn_back_constructor.move(self.parent.geometry.width() - 600, 12)
        self.parent.btn_back_constructor.resize(55, 40)

        self.parent.btn_ok_constructor = QPushButton(self.parent)
        self.parent.btn_ok_constructor.setStyleSheet('.QPushButton {border-image: url(data/image/ок.png);}'
                                                     '.QPushButton:hover {border-image: url(data/image/ок2.png);}')
        self.parent.btn_ok_constructor.move(self.parent.geometry.width() - 530, 3)
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
        self.parent.setStyleSheet('.QWidget {background-image: url(data/image/фоны/общий_фон.jpg);}')
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
        self.parent.setStyleSheet('.QWidget {background-image: url(data/image/фоны/фон_конструктора.jpg);}')
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
        self.parent.text_lesson_topic_constructor.setText(self.parent.edit_lesson_topic.text())
        self.parent.text_lesson_topic_constructor.setWordWrap(True)
        self.parent.text_lesson_topic_constructor.resize(self.parent.text_lesson_topic_constructor.sizeHint())

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
        self.parent.text_lesson_topic_constructor.show()

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
        self.parent.text_lesson_topic_constructor.hide()

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
