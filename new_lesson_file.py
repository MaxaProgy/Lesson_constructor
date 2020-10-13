from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QPainter
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QLabel, QCheckBox, QComboBox, QPushButton, QLineEdit, QMessageBox, QListView, QRadioButton, \
    QButtonGroup, QScrollArea, QWidget, QGridLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QDialog, \
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
        self.text_card.setStyleSheet(
            ".QLabel {"
            f"font: 20px;"
        "}")

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
        super(Card, self).__init__(parent.main_window)
        self.parent = parent
        self.info_card = info_card
        self.controls()

    def controls(self):
        self.label = QLabel()
        self.label.setStyleSheet('.QLabel {'
                                 f'min-height: { str(self.parent.main_window.normal.normal_prop_xy(300, 300)[0]) }px;'
                                 f'min-width: { str(self.parent.main_window.normal.normal_prop_xy(500, 500)[0]) }px;'
                                 'margin-right: 4px;'
                                 'margin-left: 4px;'
                                 'margin-bottom: 16px;'
                                 '}')
        pixmap = QPixmap('data/image/фоны/cards1.png').scaled(*self.parent.main_window.normal.normal_prop_xy(500, 300))
        self.label.setPixmap(pixmap)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox)

        self.label_lesson_topic = QLabel(self.info_card.name_method, self)
        self.label_lesson_topic.setMinimumSize(*self.parent.main_window.normal.normal_prop_xy(320, 100))
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.parent.main_window.normal.normal_font(40)}px;"
        "}")
        self.label_lesson_topic.move(*self.parent.main_window.normal.normal_prop_xy(60, 60))

        self.label_type_card = QLabel(self)
        if self.info_card.id_type_method_card == 1:
            self.label_type_card.setStyleSheet('.QLabel {border-image: url(data/image/индивид_тип.png);}')
            self.label_type_card.resize(*self.parent.main_window.normal.normal_prop_xy(40, 40))
            self.label_type_card.move(*self.parent.main_window.normal.normal_prop_xy(430, 40))

        elif self.info_card.id_type_method_card == 2:
            self.label_type_card.setStyleSheet('.QLabel {border-image: url(data/image/групп_тип.png);}')
            self.label_type_card.resize(*self.parent.main_window.normal.normal_prop_xy(40, 40))
            self.label_type_card.move(*self.parent.main_window.normal.normal_prop_xy(430, 40))

        elif self.info_card.id_type_method_card == 3:
            self.label_type_card.setStyleSheet('.QLabel {border-image: url(data/image/индивид_групп_тип.png);}')
            self.label_type_card.resize(*self.parent.main_window.normal.normal_prop_xy(60, 60))
            self.label_type_card.move(*self.parent.main_window.normal.normal_prop_xy(410, 40))

        self.label_time = QLabel(self.info_card.time + "'", self)
        self.label_time.setStyleSheet('.QLabel {font-family: "Impact";'
                                      'font: 30px }')

        self.label_time.resize(*self.parent.main_window.normal.normal_prop_xy(70, 80))
        self.label_time.setWordWrap(True)
        self.label_time.move(*self.parent.main_window.normal.normal_prop_xy(435, 100))

        self.btn_add = QPushButton(self)
        self.btn_add.setStyleSheet('.QPushButton {border-image: url(data/image/add.png);}'
                                   '.QPushButton:hover {border-image: url(data/image/add2.png);}')
        self.btn_add.move(*self.parent.main_window.normal.normal_prop_xy(430, 245))
        self.btn_add.resize(*self.parent.main_window.normal.normal_prop_xy(40, 40))
        self.btn_add.show()

        self.btn_del = QPushButton(self)
        self.btn_del.setStyleSheet('.QPushButton {border-image: url(data/image/del.png);}'
                                   '.QPushButton:hover {border-image: url(data/image/del2.png);}')
        self.btn_del.move(*self.parent.main_window.normal.normal_prop_xy(430, 245))
        self.btn_del.resize(*self.parent.main_window.normal.normal_prop_xy(40, 40))
        self.btn_del.hide()

        self.btn_more_details = QPushButton(self)
        self.btn_more_details.setStyleSheet('.QPushButton {border-image: url(data/image/Podtobnee.png);}'
                                            '.QPushButton:hover {border-image: url(data/image/Podtobnee2.png);}')
        self.btn_more_details.move(*self.parent.main_window.normal.normal_prop_xy(50, 275))
        self.btn_more_details.resize(*self.parent.main_window.normal.normal_prop_xy(175, 60))

        self.btn_add.clicked.connect(self.add_card)
        self.btn_del.clicked.connect(self.del_card)
        self.btn_more_details.clicked.connect(self.more_details)

    def show_time_cards(self):
        for card in self.parent.my_list_card:
            card.label_time.setText(card.info_card.time + "'")

        sum_1 = sum([int(card.label_time.text()[:-1]) for card in self.parent.my_list_card])
        if sum_1 > int(self.parent.main_window.edit_lesson_duration.text()):
            count = 0
            k = int(self.parent.main_window.edit_lesson_duration.text()) / sum_1
            for card in self.parent.my_list_card:
                cur_time = int(round(int(card.label_time.text()[:-1]) * k, 0))
                count += cur_time
                card.label_time.setText(str(cur_time) + "'")

            self.parent.my_list_card[-1].label_time.setText(
                str(int(self.parent.my_list_card[-1].label_time.text()[:-1])
                    + int(self.parent.main_window.edit_lesson_duration.text())
                    - count) + "'")
            sum_1 = sum([int(card.label_time.text()[:-1]) for card in self.parent.my_list_card])

        self.parent.main_window.time_lesson.setText(
            "Время урока: " + str(int(self.parent.main_window.edit_lesson_duration.text()) - sum_1) + " минут")

    def add_card(self):
        list_time_my_cards = [int(card.info_card.time) for card in self.parent.my_list_card]
        if sum(list_time_my_cards) + int(self.info_card.time) <= int(
                self.parent.main_window.edit_lesson_duration.text()) + 20:
            self.parent.my_list_card.append(self)
            self.show_my_cards()
            self.btn_add.hide()
            self.btn_del.show()
            self.parent.show_cards_stage()
            self.show_time_cards()

        else:
            QMessageBox.critical(self.parent.main_window, "Ошибка", "Превышен лимит времени", QMessageBox.Ok)
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
    def __init__(self, main_window):
        self.main_window = main_window
        self.flag_stage = 0
        self.list_card = []
        self.my_list_card = []
        self.time_sum = 0

        # ------------------------------
        #  Объекты вкладки нового урока
        # ------------------------------
        # Фон для текстовых полей нового урока
        self.main_window.background_new_lesson = QLabel(self.main_window)
        self.main_window.background_new_lesson.resize(*self.main_window.normal.normal_prop_xy(900, 600))
        self.main_window.background_new_lesson.move(*self.main_window.normal.normal_prop_xy(500, 200))
        self.main_window.background_new_lesson.setStyleSheet(
            ".QLabel {"
            "background-color: #6ca9b9;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}")
        # Тексты
        # -----------------------------------------
        self.main_window.text_lesson_topic = QLabel("Тема урока", self.main_window)
        self.main_window.text_lesson_topic.resize(self.main_window.text_lesson_topic.sizeHint())
        self.main_window.text_lesson_topic.move(*self.main_window.normal.normal_prop_xy(555, 260))
        self.main_window.text_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")

        self.main_window.text_subjects = QLabel("Предмет", self.main_window)
        self.main_window.text_subjects.resize(self.main_window.text_subjects.sizeHint())
        self.main_window.text_subjects.move(*self.main_window.normal.normal_prop_xy(555, 340))
        self.main_window.text_subjects.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")

        self.main_window.text_lesson_type = QLabel("Тип урока", self.main_window)
        self.main_window.text_lesson_type.resize(self.main_window.text_lesson_type.sizeHint())
        self.main_window.text_lesson_type.move(*self.main_window.normal.normal_prop_xy(555, 420))
        self.main_window.text_lesson_type.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")

        self.main_window.text_class = QLabel("Класс", self.main_window)
        self.main_window.text_class.resize(self.main_window.text_class.sizeHint())
        self.main_window.text_class.move(*self.main_window.normal.normal_prop_xy(555, 500))
        self.main_window.text_class.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")
        self.main_window.text_class_characteristic = QLabel("Характеристика класса", self.main_window)
        self.main_window.text_class_characteristic.resize(self.main_window.text_class_characteristic.sizeHint())
        self.main_window.text_class_characteristic.move(*self.main_window.normal.normal_prop_xy(555, 580))
        self.main_window.text_class_characteristic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")

        self.main_window.text_lesson_duration = QLabel("Длительность урока", self.main_window)
        self.main_window.text_lesson_duration.resize(self.main_window.text_lesson_duration.sizeHint())
        self.main_window.text_lesson_duration.move(*self.main_window.normal.normal_prop_xy(555, 660))
        self.main_window.text_lesson_duration.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "min-width: 12em;"
            "}")

        self.main_window.text_acquaintance = QLabel("Требуется знакомство?", self.main_window)
        self.main_window.text_acquaintance.resize(self.main_window.text_acquaintance.sizeHint())
        self.main_window.text_acquaintance.move(*self.main_window.normal.normal_prop_xy(930, 660))
        self.main_window.text_acquaintance.setStyleSheet(".QLabel {"
                                                    f"font: bold {self.main_window.normal.normal_font(16)}px;"
                                                    "min-width: 12em;"
                                                    "}")

        self.main_window.text_competence = QLabel("Компетенции ", self.main_window)
        self.main_window.text_competence.resize(self.main_window.text_competence.sizeHint())
        self.main_window.text_competence.move(*self.main_window.normal.normal_prop_xy(555, 740))
        self.main_window.text_competence.setStyleSheet(".QLabel {"
                                                  f"font: bold {self.main_window.normal.normal_font(16)}px;"
                                                  "min-width: 12em;"
                                                  "}")

        # Поля ввода значений
        # -----------------------------------------

        self.main_window.edit_lesson_topic = QLineEdit(self.main_window)
        self.main_window.edit_lesson_topic.resize(*self.main_window.normal.normal_prop_xy(480, 30))
        self.main_window.edit_lesson_topic.move(*self.main_window.normal.normal_prop_xy(820, 250))
        self.main_window.edit_lesson_topic.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(16)}px;"
            "}")

        self.main_window.combo_subjects = QComboBox(self.main_window)
        self.main_window.combo_subjects.addItems([item.name_subject for item
                                             in self.main_window.session.query(Subject).all()])
        self.main_window.combo_subjects.resize(*self.main_window.normal.normal_prop_xy(480, 30))
        self.main_window.combo_subjects.move(*self.main_window.normal.normal_prop_xy(820, 330))

        self.main_window.combo_lesson_type = QComboBox(self.main_window)
        self.main_window.combo_lesson_type.addItems([item.name_lesson_type for item
                                                in self.main_window.session.query(LessonType).all()])
        self.main_window.combo_lesson_type.resize(*self.main_window.normal.normal_prop_xy(480, 30))
        self.main_window.combo_lesson_type.move(*self.main_window.normal.normal_prop_xy(820, 410))

        self.main_window.combo_class = QComboBox(self.main_window)
        self.main_window.combo_class.addItems([str(class_) for class_ in range(1, 12)])
        self.main_window.combo_class.resize(*self.main_window.normal.normal_prop_xy(480, 30))
        self.main_window.combo_class.move(*self.main_window.normal.normal_prop_xy(820, 490))

        self.main_window.combo_class_characteristic = QComboBox(self.main_window)
        self.main_window.combo_class_characteristic.addItems([item.name_class_characteristic for item
                                                         in self.main_window.session.query(ClassCharacteristic).all()])
        self.main_window.combo_class_characteristic.resize(*self.main_window.normal.normal_prop_xy(480, 30))
        self.main_window.combo_class_characteristic.move(*self.main_window.normal.normal_prop_xy(820, 570))

        self.main_window.edit_lesson_duration = QLineEdit("40", self.main_window)
        self.main_window.edit_lesson_duration.resize(*self.main_window.normal.normal_prop_xy(80, 30))
        self.main_window.edit_lesson_duration.move(*self.main_window.normal.normal_prop_xy(820, 650))
        self.main_window.edit_lesson_duration.setStyleSheet(".QLineEdit {"
                                                       f"font: bold {self.main_window.normal.normal_font(16)}px;"
                                                       "}")

        self.main_window.radio_btn_yes = QRadioButton('Да', self.main_window)
        self.main_window.radio_btn_yes.move(*self.main_window.normal.normal_prop_xy(1160, 650))
        self.main_window.radio_btn_yes.setStyleSheet(".QRadioButton {"
                                                f"font: bold {self.main_window.normal.normal_font(16)}px;"
                                                "}")
        self.main_window.radio_btn_no = QRadioButton('Нет', self.main_window)
        self.main_window.radio_btn_no.move(*self.main_window.normal.normal_prop_xy(1240, 650))
        self.main_window.radio_btn_no.setStyleSheet(".QRadioButton {"
                                               f"font: bold {self.main_window.normal.normal_font(16)}px;"
                                               "}")
        self.main_window.radio_btn_no.setChecked(True)
        self.main_window.btn_radio_group = QButtonGroup()
        self.main_window.btn_radio_group.addButton(self.main_window.radio_btn_yes)
        self.main_window.btn_radio_group.addButton(self.main_window.radio_btn_no)
        self.main_window.check_communication = QCheckBox('Коммуникация', self.main_window)
        self.main_window.check_communication.resize(*self.main_window.normal.normal_prop_xy(200, 30))
        self.main_window.check_communication.move(*self.main_window.normal.normal_prop_xy(820, 710))
        self.main_window.check_communication.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "}")

        self.main_window.check_literacy = QCheckBox('Грамотность', self.main_window)
        self.main_window.check_literacy.resize(*self.main_window.normal.normal_prop_xy(200, 30))
        self.main_window.check_literacy.move(*self.main_window.normal.normal_prop_xy(820, 732))
        self.main_window.check_literacy.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "}")

        self.main_window.check_cooperation = QCheckBox('Кооперация', self.main_window)
        self.main_window.check_cooperation.resize(*self.main_window.normal.normal_prop_xy(200, 30))
        self.main_window.check_cooperation.move(*self.main_window.normal.normal_prop_xy(820, 754))
        self.main_window.check_cooperation.setStyleSheet(".QCheckBox {"
                                                    f"font: bold {self.main_window.normal.normal_font(14)}px;"
                                                    "}")
        self.main_window.check_creative_thinking = QCheckBox('Креативное мышление', self.main_window)
        self.main_window.check_creative_thinking.resize(*self.main_window.normal.normal_prop_xy(200, 30))
        self.main_window.check_creative_thinking.move(*self.main_window.normal.normal_prop_xy(1020, 710))
        self.main_window.check_creative_thinking.setStyleSheet(".QCheckBox {"
                                                          f"font: bold {self.main_window.normal.normal_font(14)}px;"
                                                          "}")

        self.main_window.check_critical_thinking = QCheckBox('Критическое мышление', self.main_window)
        self.main_window.check_critical_thinking.resize(*self.main_window.normal.normal_prop_xy(200, 30))
        self.main_window.check_critical_thinking.move(*self.main_window.normal.normal_prop_xy(1020, 732))
        self.main_window.check_critical_thinking.setStyleSheet(".QCheckBox {"
                                                          f"font: bold {self.main_window.normal.normal_font(14)}px;"
                                                          "}")

        self.main_window.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки', self.main_window)
        self.main_window.check_metacognitive_skills.resize(*self.main_window.normal.normal_prop_xy(200, 30))
        self.main_window.check_metacognitive_skills.move(*self.main_window.normal.normal_prop_xy(1020, 754))
        self.main_window.check_metacognitive_skills.setStyleSheet(".QCheckBox {"
                                                             f"font: bold {self.main_window.normal.normal_font(14)}px;"
                                                             "}")
        self.main_window.value_lesson = QListView(self.main_window)
        self.main_window.value_lesson.resize(*self.main_window.normal.normal_prop_xy(540, 200))
        self.main_window.value_lesson.move(*self.main_window.normal.normal_xy(1370, 5))
        self.scroll_main = QScrollArea(self.main_window)
        self.scroll_main.setStyleSheet(".QScrollArea {background-color:transparent;"
                                       "}")
        self.scroll_main.move(*self.main_window.normal.normal_prop_xy(270, 80))
        self.scroll_main.resize(*self.main_window.normal.normal_prop_xy(1200, 900))
        self.scroll_main.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_main.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_main.setFrameShape(QFrame.NoFrame)
        self.scroll_my_lesson_card = QScrollArea(self.main_window)
        self.scroll_my_lesson_card.setStyleSheet(".QScrollArea {background-color:transparent;"
                                                 "}")
        self.scroll_my_lesson_card.move(*self.main_window.normal.normal_prop_xy(1370, 204))
        self.scroll_my_lesson_card.resize(*self.main_window.normal.normal_prop_xy(540, 730))
        self.scroll_my_lesson_card.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_my_lesson_card.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.main_window.time_lesson = QLabel(f"Время урока: {self.main_window.edit_lesson_duration.text()} минут", self.main_window)
        self.main_window.time_lesson.resize(*self.main_window.normal.normal_prop_xy(100, 50))
        self.main_window.time_lesson.move(*self.main_window.normal.normal_xy(300, 25))
        self.main_window.time_lesson.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(25)}px;"
            "min-width: 20em;"
            "}")
        self.main_window.btn_save_lesson = QPushButton("Сохранить урок", self.main_window)
        self.main_window.btn_save_lesson.resize(*self.main_window.normal.normal_prop_xy(175, 70))
        self.main_window.btn_save_lesson.move(*self.main_window.normal.normal_xy(1553, 894))
        self.main_window.btn_save_lesson.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")

        self.main_window.btn_open_lesson = QPushButton("Открыть урок", self.main_window)
        self.main_window.btn_open_lesson.resize(*self.main_window.normal.normal_prop_xy(175, 70))
        self.main_window.btn_open_lesson.move(*self.main_window.normal.normal_xy(1370, 894))
        self.main_window.btn_open_lesson.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.main_window.btn_del_lesson = QPushButton("Удалить урок", self.main_window)
        self.main_window.btn_del_lesson.resize(*self.main_window.normal.normal_prop_xy(175, 70))
        self.main_window.btn_del_lesson.move(*self.main_window.normal.normal_xy(1737, 894))
        self.main_window.btn_del_lesson.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")

        self.main_window.table_result_constructor = QTableWidget(self.main_window)
        self.main_window.table_result_constructor.setColumnCount(11)
        self.main_window.table_result_constructor.resize(*self.main_window.normal.normal_prop_xy(1800, 550))
        self.main_window.table_result_constructor.move(*self.main_window.normal.normal_xy(70, 100))
        self.main_window.table_result_constructor.setRowCount(len(self.my_list_card))

        self.main_window.table_result_constructor.setColumnCount(11)
        self.main_window.table_result_constructor.setColumnWidth(10, 520)
        self.main_window.table_result_constructor.setHorizontalHeaderLabels(
            ["Назвние", "Время", "Этап", "Креативное мышление",
             "Критическое мышление", "Грамотность", "Кооперация",
             "Коммуникация", "Метакогнитивные навыки", "ФГОС навыки",
             "Содержание"])
        self.main_window.table_result_constructor.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_window.table_result_constructor.setSelectionMode(QAbstractItemView.NoSelection)
        self.main_window.table_result_constructor.setFocusPolicy(Qt.NoFocus)
        for i in range(11):
            self.main_window.table_result_constructor.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)

        # -----------------------------------------
        #                Кнопки
        # -----------------------------------------

        self.main_window.btn_back_valid = QPushButton(self.main_window)
        self.main_window.btn_back_valid.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                 '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.main_window.btn_back_valid.move(*self.main_window.normal.normal_prop_xy(1320, 210))
        self.main_window.btn_back_valid.resize(*self.main_window.normal.normal_prop_xy(55, 40))

        self.main_window.btn_ok_valid = QPushButton(self.main_window)
        self.main_window.btn_ok_valid.setStyleSheet('.QPushButton {border-image: url(data/image/ок.png);}'
                                               '.QPushButton:hover {border-image: url(data/image/ок2.png);}')
        self.main_window.btn_ok_valid.move(*self.main_window.normal.normal_prop_xy(1320, 720))
        self.main_window.btn_ok_valid.resize(*self.main_window.normal.normal_prop_xy(63, 60))
        # -----------------------------------------

        self.main_window.btn_back_constructor = QPushButton(self.main_window)
        self.main_window.btn_back_constructor.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                       '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.main_window.btn_back_constructor.move(*self.main_window.normal.normal_xy(1200, 12))
        self.main_window.btn_back_constructor.resize(*self.main_window.normal.normal_prop_xy(55, 40))
        self.main_window.btn_ok_constructor = QPushButton(self.main_window)
        self.main_window.btn_ok_constructor.setStyleSheet('.QPushButton {border-image: url(data/image/ок.png);}'
                                                     '.QPushButton:hover {border-image: url(data/image/ок2.png);}')
        self.main_window.btn_ok_constructor.move(*self.main_window.normal.normal_xy(1280, 3))
        self.main_window.btn_ok_constructor.resize(*self.main_window.normal.normal_prop_xy(63, 60))

        # -----------------------------------------
        self.main_window.btn_back_result = QPushButton(self.main_window)
        self.main_window.btn_back_result.setStyleSheet('.QPushButton {border-image: url(data/image/назад.png);}'
                                                  '.QPushButton:hover {border-image: url(data/image/назад2.png);}')
        self.main_window.btn_back_result.move(*self.main_window.normal.normal_xy(1700, 25))
        self.main_window.btn_back_result.resize(*self.main_window.normal.normal_prop_xy(65, 50))
        # -----------------------------------------
        self.main_window.btn_print = QPushButton("Печать", self.main_window)
        self.main_window.btn_print.resize(*self.main_window.normal.normal_prop_xy(400, 100))
        self.main_window.btn_print.move(*self.main_window.normal.normal_xy(1200, 800))
        self.main_window.btn_print.setStyleSheet('''
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
        self.main_window.btn_menu = QPushButton("Сохранить и закончить", self.main_window)
        self.main_window.btn_menu.resize(*self.main_window.normal.normal_prop_xy(400, 100))
        self.main_window.btn_menu.move(*self.main_window.normal.normal_xy(450, 800))
        self.main_window.btn_menu.setStyleSheet('''
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

        self.main_window.btn_stage_acquaintance = QPushButton("Знакомство", self.main_window)
        self.main_window.btn_stage_acquaintance.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}")
        self.main_window.btn_team_building = QPushButton("Командообразование", self.main_window)
        self.main_window.btn_team_building.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.main_window.btn_new_material = QPushButton("Новый материал", self.main_window)
        self.main_window.btn_new_material.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.main_window.btn_refreshments = QPushButton("Бодрилки", self.main_window)
        self.main_window.btn_refreshments.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.main_window.btn_test_of_understanding = QPushButton("Проверка понимания", self.main_window)
        self.main_window.btn_test_of_understanding.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.main_window.btn_material_fixing = QPushButton("Закрепление материала", self.main_window)
        self.main_window.btn_material_fixing.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.main_window.btn_assimilation_control = QPushButton("Контроль усвоения", self.main_window)
        self.main_window.btn_assimilation_control.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.main_window.btn_reflection = QPushButton("Рефлексия", self.main_window)
        self.main_window.btn_reflection.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.main_window.btn_homework = QPushButton("Домашнее задание", self.main_window)
        self.main_window.btn_homework.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f"font: bold {self.main_window.normal.normal_font(14)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )

        self.group_button_stage = QButtonGroup(self.main_window)
        self.group_button_stage.addButton(self.main_window.btn_stage_acquaintance)
        self.group_button_stage.addButton(self.main_window.btn_team_building)
        self.group_button_stage.addButton(self.main_window.btn_new_material)
        self.group_button_stage.addButton(self.main_window.btn_refreshments)
        self.group_button_stage.addButton(self.main_window.btn_test_of_understanding)
        self.group_button_stage.addButton(self.main_window.btn_material_fixing)
        self.group_button_stage.addButton(self.main_window.btn_assimilation_control)
        self.group_button_stage.addButton(self.main_window.btn_reflection)
        self.group_button_stage.addButton(self.main_window.btn_homework)

        self.group_button_stage.buttonClicked.connect(self.stage_button_flag)

        # -----------------------------------------
        self.main_window.btn_ok_valid.clicked.connect(self.valid_new_lesson_and_show_info)
        self.main_window.btn_back_valid.clicked.connect(self.open_main_menu)
        self.main_window.btn_back_constructor.clicked.connect(self.open_new_lesson)
        self.main_window.btn_ok_constructor.clicked.connect(self.valid_constructor_field_and_result_lesson)
        self.main_window.btn_back_result.clicked.connect(self.valid_new_lesson_and_show_info)
        self.main_window.btn_print.clicked.connect(self.print)
        self.main_window.btn_save_lesson.clicked.connect(self.save_lesson)
        self.main_window.btn_open_lesson.clicked.connect(self.open_lesson)
        self.main_window.btn_del_lesson.clicked.connect(self.del_lesson)

        self.main_window.btn_new_lesson.hide()
        self.open_new_lesson()


    def save_lesson(self):
        if int(self.main_window.time_lesson.text().split()[2]) == 0:
            if self.main_window.edit_lesson_topic.text() in [item.name for item in
                                                        self.main_window.session.query(SaveLesson).all()]:
                reply = QMessageBox.question(self.main_window, "Предупреждение",
                                             "Урок с таким названием уже сущестует. Вы хотите перезаписать?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    lesson = self.main_window.session.query(SaveLesson).filter(
                        SaveLesson.name == self.main_window.edit_lesson_topic.text()).first()
                    self.main_window.session.delete(lesson)
                    self.main_window.session.commit()

            save_lesson = SaveLesson(
                name=self.main_window.edit_lesson_topic.text(),
                ids=';'.join([str(card.info_card.id) for card in self.my_list_card]),
            )
            self.main_window.session.add(save_lesson)
            self.main_window.session.commit()
            QMessageBox.information(self.main_window, "Ок", "Урок сохранен", QMessageBox.Ok)
        else:
            QMessageBox.critical(self.main_window, "Ошибка", "Вы не использовали все время урока", QMessageBox.Ok)

    def dialog_lesson(self, del_or_open):
        self.open = QDialog()
        self.open.resize(*self.main_window.parent.normal_prop_xy(300, 150))
        self.list_view = QListWidget(self.open)
        self.list_view.resize(*self.main_window.parent.normal_prop_xy(300, 150))
        self.list_view.addItems([item.name for item in self.main_window.session.query(SaveLesson).all()])
        self.list_view.doubleClicked.connect(del_or_open)
        self.open.exec()

    def del_lesson(self):
        self.dialog_lesson(self.del_select_lesson)

    def open_lesson(self):
        self.dialog_lesson(self.open_select_lesson)

    def del_select_lesson(self):
        self.open.close()
        reply = QMessageBox.question(self.main_window, "Удаление", "Вы хотите удалить урок?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            lesson = self.main_window.session.query(SaveLesson).filter(
                SaveLesson.name == self.list_view.currentItem().text()).first()
            self.main_window.session.delete(lesson)
            self.main_window.session.commit()

    def open_select_lesson(self):
        self.open.close()
        self.my_list_card = []
        for id in self.main_window.session.query(SaveLesson).filter(SaveLesson.name ==
                                                               self.list_view.currentItem().text()).first().ids.split(
            ";"):
            self.my_list_card.append(Card(self, self.main_window.session.query(Cards).filter(Cards.id == id).first()))
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
        self.main_window.table_result_constructor.render(painter)
        painter.end()

    def open_main_menu(self):
        self.hide_object_new_lesson()
        self.main_window.main_menu()

    def open_new_lesson(self):
        pixmap = QPixmap('data/image/фоны/общий_фон.jpg')
        self.main_window.background.setPixmap(pixmap)
        self.hide_object_constructor_field()
        self.show_object_new_lesson()

    def valid_new_lesson_and_show_info(self):
        if self.main_window.edit_lesson_topic.text() != "" and \
                int(self.main_window.edit_lesson_duration.text()) >= 20 and \
                (self.main_window.check_creative_thinking.isChecked() or
                 self.main_window.check_literacy.isChecked() or
                 self.main_window.check_communication.isChecked() or
                 self.main_window.check_cooperation.isChecked() or
                 self.main_window.check_critical_thinking.isChecked() or
                 self.main_window.check_metacognitive_skills.isChecked()):
            self.constructor_field()
        else:
            QMessageBox.critical(self.main_window, "Ошибка", "Вы заполните все поля", QMessageBox.Ok)

    def constructor_field(self):
        self.filter_card = self.main_window.session.query(Cards).filter(
            Cards.id_lesson_type == self.main_window.combo_lesson_type.currentIndex() + 1,
            or_(Cards.creative_thinking == self.main_window.check_creative_thinking.isChecked(),
                Cards.critical_thinking == self.main_window.check_critical_thinking.isChecked(),
                Cards.communication == self.main_window.check_communication.isChecked(),
                Cards.cooperation == self.main_window.check_cooperation.isChecked(),
                Cards.metacognitive_skills == self.main_window.check_metacognitive_skills.isChecked(),
                Cards.literacy == self.main_window.check_literacy.isChecked())
        )
        pixmap = QPixmap('data/image/фоны/общий_фон.jpg')
        self.main_window.background.setPixmap(pixmap)
        self.hide_object_new_lesson()
        self.show_object_constructor_field()
        self.hide_object_result_lesson()
        self.main_window.table_result_constructor.setRowCount(0)
        if self.main_window.radio_btn_no.isChecked():
            self.main_window.btn_stage_acquaintance.hide()

            self.main_window.btn_team_building.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_new_material.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_refreshments.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_test_of_understanding.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_material_fixing.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_assimilation_control.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_reflection.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_homework.resize(*self.main_window.normal.normal_prop_xy(200, 85))
            self.main_window.btn_assimilation_control.resize(*self.main_window.normal.normal_prop_xy(200, 85))

            self.main_window.btn_team_building.move(*self.main_window.normal.normal_xy(50, 140))
            self.main_window.btn_new_material.move(*self.main_window.normal.normal_xy(50, 230))
            self.main_window.btn_refreshments.move(*self.main_window.normal.normal_xy(50, 320))
            self.main_window.btn_test_of_understanding.move(*self.main_window.normal.normal_xy(50, 410))
            self.main_window.btn_material_fixing.move(*self.main_window.normal.normal_xy(50, 500))
            self.main_window.btn_assimilation_control.move(*self.main_window.normal.normal_xy(50, 590))
            self.main_window.btn_reflection.move(*self.main_window.normal.normal_xy(50, 680))
            self.main_window.btn_homework.move(*self.main_window.normal.normal_xy(50, 770))
        else:
            self.main_window.btn_stage_acquaintance.show()

            self.main_window.btn_stage_acquaintance.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_team_building.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_new_material.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_refreshments.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_test_of_understanding.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_material_fixing.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_reflection.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_homework.resize(*self.main_window.normal.normal_prop_xy(200, 80))
            self.main_window.btn_assimilation_control.resize(*self.main_window.normal.normal_prop_xy(200, 80))

            self.main_window.btn_stage_acquaintance.move(*self.main_window.normal.normal_xy(50, 140))
            self.main_window.btn_team_building.move(*self.main_window.normal.normal_xy(50, 225))
            self.main_window.btn_new_material.move(*self.main_window.normal.normal_xy(50, 310))
            self.main_window.btn_refreshments.move(*self.main_window.normal.normal_xy(50, 395))
            self.main_window.btn_test_of_understanding.move(*self.main_window.normal.normal_xy(50, 480))
            self.main_window.btn_material_fixing.move(*self.main_window.normal.normal_xy(50, 565))
            self.main_window.btn_assimilation_control.move(*self.main_window.normal.normal_xy(50, 650))
            self.main_window.btn_reflection.move(*self.main_window.normal.normal_xy(50, 735))
            self.main_window.btn_homework.move(*self.main_window.normal.normal_xy(50, 820))

        title_value = [('Тема урока', self.main_window.edit_lesson_topic.text()),
                       ('Предмет', self.main_window.combo_subjects.currentText()),
                       ('Тип урока', self.main_window.combo_lesson_type.currentText()),
                       ('Класс', self.main_window.combo_class.currentText()),
                       ('Характеристика класса', self.main_window.combo_class_characteristic.currentText()),
                       ('Длительность', self.main_window.edit_lesson_duration.text()),
                       ('Креативное мышление', self.main_window.check_creative_thinking.isChecked()),
                       ('Критическое мышление', self.main_window.check_critical_thinking.isChecked()),
                       ('Грамотность', self.main_window.check_literacy.isChecked()),
                       ('Кооперация', self.main_window.check_cooperation.isChecked()),
                       ('Коммуникация', self.main_window.check_communication.isChecked()),
                       ('Метакогнитивные навыки', self.main_window.check_metacognitive_skills.isChecked())]
        model = QStandardItemModel()
        self.main_window.value_lesson.setModel(model)
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
        self.flag_stage = self.main_window.session.query(Stage).filter(Stage.name_stage == button.text()).first().id
        self.show_cards_stage()

    def valid_constructor_field_and_result_lesson(self):
        if int(self.main_window.time_lesson.text().split()[2]) != 0:
            QMessageBox.critical(self.main_window, "Ошибка", "Вы не задействовали все время", QMessageBox.Ok)
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
            self.main_window.table_result_constructor.insertRow(i)
            self.main_window.table_result_constructor.setItem(i, 0,
                                                         QTableWidgetItem(self.my_list_card[i].info_card.name_method))
            self.main_window.table_result_constructor.setItem(i, 1, QTableWidgetItem(
                self.my_list_card[i].label_time.text()[:-1] + " минут"))
            self.main_window.table_result_constructor.setItem(i, 2, QTableWidgetItem(
                self.my_list_card[i].info_card.stage.name_stage))
            self.main_window.table_result_constructor.setItem(i, 3, QTableWidgetItem(list_skills_gk[0]))
            self.main_window.table_result_constructor.setItem(i, 4, QTableWidgetItem(list_skills_gk[1]))
            self.main_window.table_result_constructor.setItem(i, 5, QTableWidgetItem(list_skills_gk[2]))
            self.main_window.table_result_constructor.setItem(i, 6, QTableWidgetItem(list_skills_gk[3]))
            self.main_window.table_result_constructor.setItem(i, 7, QTableWidgetItem(list_skills_gk[4]))
            self.main_window.table_result_constructor.setItem(i, 8, QTableWidgetItem(list_skills_gk[5]))
            self.main_window.table_result_constructor.setItem(i, 9, QTableWidgetItem(
                self.my_list_card[i].info_card.fgos.name_fgos))
            self.main_window.table_result_constructor.setItem(i, 10, QTableWidgetItem(self.my_list_card[i].info_card.text))
        self.main_window.table_result_constructor.resizeRowsToContents()

        self.show_object_result_lesson()

    def show_object_result_lesson(self):
        self.main_window.table_result_constructor.show()
        self.main_window.btn_back_result.show()
        self.main_window.btn_print.show()
        self.main_window.btn_menu.show()

    def hide_object_result_lesson(self):
        self.main_window.table_result_constructor.hide()
        self.main_window.btn_back_result.hide()
        self.main_window.btn_print.hide()
        self.main_window.btn_menu.hide()

    def show_object_constructor_field(self):
        self.main_window.btn_ok_constructor.show()
        self.main_window.btn_back_constructor.show()
        self.main_window.btn_stage_acquaintance.show()
        self.main_window.btn_team_building.show()
        self.main_window.btn_new_material.show()
        self.main_window.btn_refreshments.show()
        self.main_window.btn_test_of_understanding.show()
        self.main_window.btn_material_fixing.show()
        self.main_window.btn_assimilation_control.show()
        self.main_window.btn_reflection.show()
        self.main_window.btn_homework.show()
        self.main_window.value_lesson.show()
        self.scroll_main.show()
        self.scroll_my_lesson_card.show()
        self.main_window.time_lesson.show()
        self.main_window.btn_save_lesson.show()
        self.main_window.btn_del_lesson.show()
        self.main_window.btn_open_lesson.show()

    def hide_object_constructor_field(self):
        self.main_window.btn_ok_constructor.hide()
        self.main_window.btn_back_constructor.hide()
        self.main_window.btn_stage_acquaintance.hide()
        self.main_window.btn_team_building.hide()
        self.main_window.btn_new_material.hide()
        self.main_window.btn_refreshments.hide()
        self.main_window.btn_test_of_understanding.hide()
        self.main_window.btn_material_fixing.hide()
        self.main_window.btn_assimilation_control.hide()
        self.main_window.btn_reflection.hide()
        self.main_window.btn_homework.hide()
        self.main_window.value_lesson.hide()
        self.scroll_main.hide()
        self.scroll_my_lesson_card.hide()
        self.main_window.time_lesson.hide()
        self.main_window.btn_save_lesson.hide()
        self.main_window.btn_del_lesson.hide()
        self.main_window.btn_open_lesson.hide()

    def show_object_new_lesson(self):
        self.main_window.background_new_lesson.show()

        self.main_window.text_lesson_topic.show()
        self.main_window.text_subjects.show()
        self.main_window.text_lesson_type.show()
        self.main_window.text_class.show()
        self.main_window.text_class_characteristic.show()
        self.main_window.text_lesson_duration.show()
        self.main_window.text_acquaintance.show()
        self.main_window.text_competence.show()
        self.main_window.edit_lesson_topic.show()
        self.main_window.radio_btn_no.show()
        self.main_window.radio_btn_yes.show()
        self.main_window.combo_subjects.show()
        self.main_window.combo_lesson_type.show()
        self.main_window.combo_class.show()
        self.main_window.combo_class_characteristic.show()
        self.main_window.edit_lesson_duration.show()
        self.main_window.check_creative_thinking.show()
        self.main_window.check_literacy.show()
        self.main_window.check_cooperation.show()
        self.main_window.check_communication.show()
        self.main_window.check_critical_thinking.show()
        self.main_window.check_metacognitive_skills.show()

        self.main_window.btn_back_valid.show()
        self.main_window.btn_ok_valid.show()

    def hide_object_new_lesson(self):
        self.main_window.background_new_lesson.hide()

        self.main_window.text_lesson_topic.hide()
        self.main_window.text_subjects.hide()
        self.main_window.text_lesson_type.hide()
        self.main_window.text_class.hide()
        self.main_window.text_class_characteristic.hide()
        self.main_window.text_lesson_duration.hide()
        self.main_window.text_acquaintance.hide()
        self.main_window.text_competence.hide()
        self.main_window.edit_lesson_topic.hide()
        self.main_window.radio_btn_no.hide()
        self.main_window.radio_btn_yes.hide()
        self.main_window.combo_subjects.hide()
        self.main_window.combo_lesson_type.hide()
        self.main_window.combo_class.hide()
        self.main_window.combo_class_characteristic.hide()
        self.main_window.edit_lesson_duration.hide()
        self.main_window.check_creative_thinking.hide()
        self.main_window.check_literacy.hide()
        self.main_window.check_cooperation.hide()
        self.main_window.check_communication.hide()
        self.main_window.check_critical_thinking.hide()
        self.main_window.check_metacognitive_skills.hide()

        self.main_window.btn_back_valid.hide()
        self.main_window.btn_ok_valid.hide()
