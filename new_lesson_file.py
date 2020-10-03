from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox, QPushButton, QLineEdit, QMessageBox, QListView, QRadioButton, \
    QButtonGroup, QScrollArea, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, \
    QAbstractItemView, QFrame, QListWidget
from PyQt5.QtCore import Qt
from data.stage import Stage
from data.cards import Cards
from data.save_lesson import SaveLesson
from data.class_characteristic import ClassCharacteristic
from data.subject import Subject
from data.lesson_type import LessonType
from sqlalchemy import or_


class CardMoreDetails(QDialog):
    def __init__(self, info_card):
        super(QDialog, self).__init__()
        self.setModal(True)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle(info_card.name_method)
        self.info_card = info_card
        self.setFixedSize(700, 500)
        self.label = QLabel(self)
        self.label.setStyleSheet('.QLabel {background-color: #ffa163}')
        self.label.resize(700, 500)

        self.fgos = QLabel(self)
        pixmap = QPixmap('data/image/fgos.png')
        self.fgos.setPixmap(pixmap)
        self.fgos.move(370, 200)

        self.text_card = QLabel(info_card.text, self)
        self.text_card.move(20, 20)
        self.text_card.setMinimumSize(320, 200)
        self.text_card.setStyleSheet('''
            .QLabel {
            font: 20px;
        }''')

        list_compet = [(info_card.creative_thinking, "- Креативное мышление"),
                       (info_card.critical_thinking, "- Критическое мышление"),
                       (info_card.literacy, "- Грамотность"),
                       (info_card.cooperation, "- Кооперация"),
                       (info_card.cooperation, "- Коммуникация"),
                       (info_card.metacognitive_skills, "- Метакогнитивные навыки")]
        list_compet = [i[1] for i in list_compet if i[0]]

        if info_card.fgos.name_fgos != "-":
            list_compet.append("- " + info_card.fgos.name_fgos + " навыки ФГОС")
        self.text_card.setWordWrap(True)
        self.text_card = QLabel('\n'.join(list_compet), self)
        self.text_card.move(370, 20)
        self.text_card.setMinimumSize(320, 200)
        self.text_card.setStyleSheet('''
            .QLabel {
            font: bold  20px;
        }''')
        self.text_card.setWordWrap(True)


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
                                 'margin-right: 4px;'
                                 'margin-left: 4px;'
                                 'margin-bottom: 16px;'
                                 '}')
        pixmap = QPixmap('data/image/фоны/cards1.png')
        self.label.setPixmap(pixmap)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox)

        self.label_lesson_topic = QLabel(self.info_card.name_method, self)
        self.label_lesson_topic.setMinimumSize(320, 100)
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet('''
            .QLabel {
            font: bold 40px;
        }''')
        self.label_lesson_topic.move(60, 60)

        self.label_type_card = QLabel(self)
        if self.info_card.id_type_method_card == 1:
            self.label_type_card.setStyleSheet('.QLabel {border-image: url(data/image/индивид_тип.png);}')
            self.label_type_card.resize(40, 40)
            self.label_type_card.move(430, 40)

        elif self.info_card.id_type_method_card == 2:
            self.label_type_card.setStyleSheet('.QLabel {border-image: url(data/image/групп_тип.png);}')
            self.label_type_card.resize(40, 40)
            self.label_type_card.move(430, 40)

        elif self.info_card.id_type_method_card == 3:
            self.label_type_card.setStyleSheet('.QLabel {border-image: url(data/image/индивид_групп_тип.png);}')
            self.label_type_card.resize(60, 60)
            self.label_type_card.move(410, 40)

        self.label_time = QLabel(self.info_card.time + "'", self)
        self.label_time.setStyleSheet('.QLabel {font-family: "Impact";'
                                      'font: 30px }')

        self.label_time.resize(70, 80)
        self.label_time.setWordWrap(True)
        self.label_time.move(435, 100)

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

        self.btn_more_details = QPushButton(self)
        self.btn_more_details.setStyleSheet('.QPushButton {border-image: url(data/image/Podtobnee.png);}'
                                            '.QPushButton:hover {border-image: url(data/image/Podtobnee2.png);}')
        self.btn_more_details.move(50, 275)
        self.btn_more_details.resize(175, 60)

        self.btn_add.clicked.connect(self.add_card)
        self.btn_del.clicked.connect(self.del_card)
        self.btn_more_details.clicked.connect(self.more_details)

    def show_time_cards(self):
        for card in self.parent.my_list_card:
            card.label_time.setText(card.info_card.time + "'")

        sum_1 = sum([int(card.label_time.text()[:-1]) for card in self.parent.my_list_card])
        if sum_1 > int(self.parent.parent.edit_lesson_duration.text()):
            count = 0
            k = int(self.parent.parent.edit_lesson_duration.text()) / sum_1
            for card in self.parent.my_list_card:
                cur_time = int(round(int(card.label_time.text()[:-1]) * k, 0))
                count += cur_time
                card.label_time.setText(str(cur_time) + "'")

            self.parent.my_list_card[-1].label_time.setText(
                str(int(self.parent.my_list_card[-1].label_time.text()[:-1])
                    + int(self.parent.parent.edit_lesson_duration.text())
                    - count) + "'")
            sum_1 = sum([int(card.label_time.text()[:-1]) for card in self.parent.my_list_card])

        self.parent.parent.time_lesson.setText(
            "Время урока: " + str(int(self.parent.parent.edit_lesson_duration.text()) - sum_1) + " минут")

    def add_card(self):
        list_time_my_cards = [int(card.info_card.time) for card in self.parent.my_list_card]
        if sum(list_time_my_cards) + int(self.info_card.time) <= int(
                self.parent.parent.edit_lesson_duration.text()) + 20:
            self.parent.my_list_card.append(self)
            self.show_my_cards()
            self.btn_add.hide()
            self.btn_del.show()
            self.parent.show_cards_stage()
            self.show_time_cards()

        else:
            QMessageBox.critical(self.parent.parent, "Ошибка", "Превышен лимит времени", QMessageBox.Ok)
            return

    def del_card(self):
        del self.parent.my_list_card[self.parent.my_list_card.index(self)]
        self.show_my_cards()
        self.parent.show_cards_stage()

        self.show_time_cards()

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

    def more_details(self):
        self.card_info = CardMoreDetails(self.info_card)
        self.card_info.show()


class NewLesson:
    def __init__(self, parent):
        self.parent = parent
        self.flag_stage = 0
        self.list_card = []
        self.my_list_card = []
        self.time_sum = 0

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
        self.parent.combo_class.addItems([str(class_) for class_ in range(1, 12)])
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
        self.parent.value_lesson.resize(540, 200)
        self.parent.value_lesson.move(self.parent.width_windows - 550, 5)

        self.scroll_main = QScrollArea(self.parent)
        self.scroll_main.setStyleSheet(".QScrollArea {background-color:transparent;"
                                       "}")
        self.scroll_main.move(270, 80)
        self.scroll_main.resize(self.parent.width_windows - 820, self.parent.height_windows - 150)
        self.scroll_main.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_main.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_main.setFrameShape(QFrame.NoFrame)

        self.scroll_my_lesson_card = QScrollArea(self.parent)
        self.scroll_my_lesson_card.setStyleSheet(".QScrollArea {background-color:transparent;"
                                                 "}")
        self.scroll_my_lesson_card.move(self.parent.width_windows - 550, 204)
        self.scroll_my_lesson_card.resize(540, 730)
        self.scroll_my_lesson_card.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_my_lesson_card.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.parent.time_lesson = QLabel(f"Время урока: {self.parent.edit_lesson_duration.text()} минут", self.parent)
        self.parent.time_lesson.resize(100, 50)
        self.parent.time_lesson.move(300, 25)
        self.parent.time_lesson.setStyleSheet('''
            .QLabel {
            font: bold 25px;
            min-width: 20em;
        }''')

        self.parent.btn_save_lesson = QPushButton("Сохранить урок", self.parent)
        self.parent.btn_save_lesson.resize(175, 70)
        self.parent.btn_save_lesson.move(self.parent.width_windows - 365, 894)
        self.parent.btn_save_lesson.setStyleSheet('''
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

        self.parent.btn_open_lesson = QPushButton("Открыть урок", self.parent)
        self.parent.btn_open_lesson.resize(175, 70)
        self.parent.btn_open_lesson.move(self.parent.width_windows - 550, 894)
        self.parent.btn_open_lesson.setStyleSheet('''
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

        self.parent.btn_del_lesson = QPushButton("Удалить урок", self.parent)
        self.parent.btn_del_lesson.resize(175, 70)
        self.parent.btn_del_lesson.move(self.parent.width_windows - 180, 894)
        self.parent.btn_del_lesson.setStyleSheet('''
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

        self.parent.table_result_constructor = QTableWidget(self.parent)
        self.parent.table_result_constructor.setColumnCount(11)
        self.parent.table_result_constructor.resize(1800, 700)
        self.parent.table_result_constructor.move(70, 100)
        self.parent.table_result_constructor.setRowCount(len(self.my_list_card))

        self.parent.table_result_constructor.setColumnCount(11)
        self.parent.table_result_constructor.setColumnWidth(10, 520)
        self.parent.table_result_constructor.setHorizontalHeaderLabels(
            ["Назвние", "Время", "Этап", "Креативное мышление",
             "Критическое мышление", "Грамотность", "Кооперация",
             "Коммуникация", "Метакогнитивные навыки", "ФГОС навыки",
             "Содержание"])
        self.parent.table_result_constructor.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.parent.table_result_constructor.setSelectionMode(QAbstractItemView.NoSelection)
        self.parent.table_result_constructor.setFocusPolicy(Qt.NoFocus)
        for i in range(11):
            self.parent.table_result_constructor.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)

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

        self.parent.btn_back_result = QPushButton(self.parent)
        self.parent.btn_back_result.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                  '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.parent.btn_back_result.move(self.parent.width_windows - 150, 25)
        self.parent.btn_back_result.resize(65, 50)
        # -----------------------------------------

        self.parent.btn_print = QPushButton("Печать", self.parent)
        self.parent.btn_print.resize(400, 100)
        self.parent.btn_print.move(self.parent.width_windows // 2 - 600, 800)
        self.parent.btn_print.setStyleSheet('''
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

        self.parent.btn_menu = QPushButton("Сохранить и закончить", self.parent)
        self.parent.btn_menu.resize(400, 100)
        self.parent.btn_menu.move(self.parent.width_windows // 2 + 150, 800)
        self.parent.btn_menu.setStyleSheet('''
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
        self.parent.btn_ok_constructor.clicked.connect(self.valid_constructor_field_and_result_lesson)
        self.parent.btn_back_result.clicked.connect(self.valid_new_lesson_and_show_info)
        self.parent.btn_print.clicked.connect(self.print)
        self.parent.btn_save_lesson.clicked.connect(self.save_lesson)
        self.parent.btn_open_lesson.clicked.connect(self.open_lesson)
        self.parent.btn_del_lesson.clicked.connect(self.del_lesson)

        self.parent.btn_new_lesson.hide()
        self.open_new_lesson()

    def save_lesson(self):
        if int(self.parent.time_lesson.text().split()[2]) == 0:
            if self.parent.edit_lesson_topic.text() in [item.name for item in self.parent.session.query(SaveLesson).all()]:
                reply = QMessageBox.question(self.parent, "Предупреждение",
                                             "Урок с таким названием уже сущестует. Вы хотите перезаписать?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    lesson = self.parent.session.query(SaveLesson).filter(
                        SaveLesson.name == self.parent.edit_lesson_topic.text()).first()
                    self.parent.session.delete(lesson)
                    self.parent.session.commit()

            save_lesson = SaveLesson(
                name=self.parent.edit_lesson_topic.text(),
                ids=';'.join([str(card.info_card.id) for card in self.my_list_card]),
            )
            self.parent.session.add(save_lesson)
            self.parent.session.commit()
            QMessageBox.information(self.parent, "Ок", "Урок сохранен", QMessageBox.Ok)
        else:
            QMessageBox.critical(self.parent, "Ошибка", "Вы не использовали все время урока", QMessageBox.Ok)

    def dialog_lesson(self, del_or_open):
        self.open = QDialog()
        self.open.resize(300, 150)
        self.list_view = QListWidget(self.open)
        self.list_view.resize(300, 150)
        self.list_view.addItems([item.name for item in self.parent.session.query(SaveLesson).all()])
        self.list_view.doubleClicked.connect(del_or_open)
        self.open.exec()

    def del_lesson(self):
        self.dialog_lesson(self.del_select_lesson)

    def open_lesson(self):
        self.dialog_lesson(self.open_select_lesson)

    def del_select_lesson(self):
        self.open.close()
        reply = QMessageBox.question(self.parent, "Удаление", "Вы хотите удалить урок?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            lesson = self.parent.session.query(SaveLesson).filter(
                SaveLesson.name == self.list_view.currentItem().text()).first()
            self.parent.session.delete(lesson)
            self.parent.session.commit()

    def open_select_lesson(self):
        self.open.close()
        self.my_list_card = []
        for id in self.parent.session.query(SaveLesson).filter(SaveLesson.name ==
                                                               self.list_view.currentItem().text()).first().ids.split(
            ";"):
            self.my_list_card.append(Card(self, self.parent.session.query(Cards).filter(Cards.id == id).first()))
            self.my_list_card[-1].btn_add.hide()
            self.my_list_card[-1].btn_del.show()
        self.my_list_card[0].show_my_cards()
        self.my_list_card[0].show_time_cards()
        self.show_cards_stage()

    def print(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("Test.pdf")

        painter = QPainter(printer)
        """
        xscale = printer.pageRect().width() / self.width()
        yscale = printer.pageRect().height() / self.height()
        scale = min(xscale, yscale)
        painter.translate(printer.paperRect().center())
        painter.scale(scale, scale)
        painter.translate((self.width() / 2) * -1, (self.height() / 2) * -1)
        """
        self.parent.table_result_constructor.render(painter)
        painter.end()

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
        self.filter_card = self.parent.session.query(Cards).filter(
            Cards.id_lesson_type == self.parent.combo_lesson_type.currentIndex() + 1,
            or_(Cards.creative_thinking == self.parent.check_creative_thinking.isChecked(),
                Cards.critical_thinking == self.parent.check_critical_thinking.isChecked(),
                Cards.communication == self.parent.check_communication.isChecked(),
                Cards.cooperation == self.parent.check_cooperation.isChecked(),
                Cards.metacognitive_skills == self.parent.check_metacognitive_skills.isChecked(),
                Cards.literacy == self.parent.check_literacy.isChecked())
        )
        pixmap = QPixmap('data/image/фоны/фон_конструктора.jpg')
        self.parent.background.setPixmap(pixmap)
        self.hide_object_new_lesson()
        self.show_object_constructor_field()
        self.hide_object_result_lesson()
        self.parent.table_result_constructor.setRowCount(0)
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
                       ('Критическое мышление', self.parent.check_critical_thinking.isChecked()),
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
        list_cards = self.filter_card.filter(Cards.id_stage_card.like(self.flag_stage)).all()
        layout = QGridLayout()

        for i in reversed(range(len(self.list_card))):
            del self.list_card[i]

        list_id_my_card = [card.info_card.id for card in self.my_list_card]

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

    def valid_constructor_field_and_result_lesson(self):
        if int(self.parent.time_lesson.text().split()[2]) != 0:
            QMessageBox.critical(self.parent, "Ошибка", "Вы не задействовали все время", QMessageBox.Ok)
            return
        self.hide_object_constructor_field()

        for i in range(len(self.my_list_card)):
            list_skills = [self.my_list_card[i].info_card.creative_thinking,
                           self.my_list_card[i].info_card.critical_thinking,
                           self.my_list_card[i].info_card.literacy, self.my_list_card[i].info_card.cooperation,
                           self.my_list_card[i].info_card.cooperation,
                           self.my_list_card[i].info_card.metacognitive_skills]
            list_skills_gk = []
            for j in list_skills:
                if j:
                    list_skills_gk.append('\u2611')
                else:
                    list_skills_gk.append('\u2716')
            self.parent.table_result_constructor.insertRow(i)
            self.parent.table_result_constructor.setItem(i, 0,
                                                         QTableWidgetItem(self.my_list_card[i].info_card.name_method))
            self.parent.table_result_constructor.setItem(i, 1, QTableWidgetItem(
                self.my_list_card[i].label_time.text()[:-1] + " минут"))
            self.parent.table_result_constructor.setItem(i, 2, QTableWidgetItem(
                self.my_list_card[i].info_card.stage.name_stage))
            self.parent.table_result_constructor.setItem(i, 3, QTableWidgetItem(list_skills_gk[0]))
            self.parent.table_result_constructor.setItem(i, 4, QTableWidgetItem(list_skills_gk[1]))
            self.parent.table_result_constructor.setItem(i, 5, QTableWidgetItem(list_skills_gk[2]))
            self.parent.table_result_constructor.setItem(i, 6, QTableWidgetItem(list_skills_gk[3]))
            self.parent.table_result_constructor.setItem(i, 7, QTableWidgetItem(list_skills_gk[4]))
            self.parent.table_result_constructor.setItem(i, 8, QTableWidgetItem(list_skills_gk[5]))
            self.parent.table_result_constructor.setItem(i, 9, QTableWidgetItem(
                self.my_list_card[i].info_card.fgos.name_fgos))
            self.parent.table_result_constructor.setItem(i, 10, QTableWidgetItem(self.my_list_card[i].info_card.text))
        self.parent.table_result_constructor.resizeRowsToContents()

        self.show_object_result_lesson()

    def show_object_result_lesson(self):
        self.parent.table_result_constructor.show()
        self.parent.btn_back_result.show()
        self.parent.btn_print.show()
        self.parent.btn_menu.show()

    def hide_object_result_lesson(self):
        self.parent.table_result_constructor.hide()
        self.parent.btn_back_result.hide()
        self.parent.btn_print.hide()
        self.parent.btn_menu.hide()

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
        self.parent.time_lesson.show()
        self.parent.btn_save_lesson.show()
        self.parent.btn_del_lesson.show()
        self.parent.btn_open_lesson.show()

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
        self.parent.time_lesson.hide()
        self.parent.btn_save_lesson.hide()
        self.parent.btn_del_lesson.hide()
        self.parent.btn_open_lesson.hide()

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
