from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox, QPushButton, QLineEdit, QMessageBox, QWidget


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

        self.parent.text_lesson_duration_2 = QLabel("Минут", self.parent)
        self.parent.text_lesson_duration_2.resize(self.parent.text_lesson_duration_2.sizeHint())
        self.parent.text_lesson_duration_2.move(self.parent.geometry.width() // 2 - 50,
                                                self.parent.geometry.height() // 2 + 150)
        self.parent.text_lesson_duration_2.setStyleSheet('''
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
        self.parent.edit_lesson_duration.move(self.parent.geometry.width() // 2 - 140,
                                              self.parent.geometry.height() // 2 + 140)
        self.parent.edit_lesson_duration.setStyleSheet('''
            .QLineEdit {
            font: bold 16px;
        }''')

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

        self.parent.btn_back = QPushButton(self.parent)
        self.parent.btn_back.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                           '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.parent.btn_back.move(self.parent.geometry.width() // 2 + 390, self.parent.geometry.height() // 2 - 350)
        self.parent.btn_back.resize(55, 40)

        self.parent.btn_ok = QPushButton(self.parent)
        self.parent.btn_ok.setStyleSheet('.QPushButton {border-image: url(data/image/ок.png);}'
                                         '.QPushButton:hover {border-image: url(data/image/ок2.png);}')
        self.parent.btn_ok.move(self.parent.geometry.width() // 2 + 350, self.parent.geometry.height() - 310)
        self.parent.btn_ok.resize(63, 60)

        self.parent.btn_ok.clicked.connect(self.valid_new_lesson_and_show_info)
        self.parent.btn_back.clicked.connect(self.open_main_menu)

        self.parent.btn_new_lesson.hide()
        self.show_object_new_lesson()

    def open_main_menu(self):
        self.hide_object_new_lesson()
        self.parent.main_menu()

    def valid_new_lesson_and_show_info(self):
        if self.parent.edit_lesson_topic.text() != "" and \
                int(self.parent.edit_lesson_duration.text()) >= 20 and \
                (self.parent.check_creative_thinking.isChecked() or
                 self.parent.check_literacy.isChecked() or
                 self.parent.check_communication.isChecked() or
                 self.parent.check_cooperation.isChecked() or
                 self.parent.check_critical_thinking.isChecked() or
                 self.parent.check_metacognitive_skills.isChecked()):
            pass
        else:
            QMessageBox.critical(self.parent, "Ошибка", "Вы заполните все поля", QMessageBox.Ok)

    def show_object_new_lesson(self):
        self.parent.background_new_lesson.show()

        self.parent.text_lesson_topic.show()
        self.parent.text_subjects.show()
        self.parent.text_lesson_type.show()
        self.parent.text_class.show()
        self.parent.text_class_characteristic.show()
        self.parent.text_lesson_duration.show()
        self.parent.text_lesson_duration_2.show()
        self.parent.text_competence.show()
        self.parent.edit_lesson_topic.show()
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

        self.parent.btn_back.show()
        self.parent.btn_ok.show()

    def hide_object_new_lesson(self):
        self.parent.background_new_lesson.hide()

        self.parent.text_lesson_topic.hide()
        self.parent.text_subjects.hide()
        self.parent.text_lesson_type.hide()
        self.parent.text_class.hide()
        self.parent.text_class_characteristic.hide()
        self.parent.text_lesson_duration.hide()
        self.parent.text_lesson_duration_2.hide()
        self.parent.text_competence.hide()
        self.parent.edit_lesson_topic.hide()
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

        self.parent.btn_back.hide()
        self.parent.btn_ok.hide()
