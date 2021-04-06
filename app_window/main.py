# -*- coding: utf-8 -*-

import sys
import time
import random

from PyQt5 import QtGui, QtCore, QAxContainer
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QDesktopWidget, QLabel, QWidget, QPushButton, \
    QGridLayout, QLineEdit, QCheckBox, QButtonGroup, QComboBox, QRadioButton, QMessageBox, QVBoxLayout, \
    QScrollArea, QFrame, QHBoxLayout, QDialog, QListWidget, QTextEdit, QSpinBox, QFileDialog

from sqlalchemy import or_

from app_window.const import *
from app_window.data import db_session
from app_window.data.methods import Methods
from app_window.data.save_lesson import SaveLesson
from app_window.data.documents_lesson import DocumentsLesson
from app_window.document_file import get_document_result_word

id_current_user = None


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
        self.menu.create_my_methods_event.connect(self.close_menu_on_my_method)
        self.menu.create_my_constructor_event.connect(self.close_menu_on_constructor)
        self.menu.create_my_lessons_menu_event.connect(self.close_menu_on_my_lessons_menu)
        self.menu.show()

    def run_constructor(self, data):
        self.constructor = Constructor(self, data)
        self.constructor.setAttribute(Qt.WA_DeleteOnClose)
        self.constructor.back_menu_event.connect(self.close_constructor_on_menu)
        self.constructor.create_result_event.connect(self.close_constructor_on_result)
        self.constructor.show()

    def run_result(self, data):
        self.result = ResultLesson(self, data)
        self.result.setAttribute(Qt.WA_DeleteOnClose)
        self.result.back_constructor_event.connect(self.close_result_on_constructor)
        self.result.back_menu_event.connect(self.close_result_on_menu)
        self.result.show()

    def run_my_method_menu(self):
        self.my_method_menu = MyMethodMenu(self)
        self.my_method_menu.setAttribute(Qt.WA_DeleteOnClose)
        self.my_method_menu.back_menu_event.connect(self.close_my_method_on_menu)
        self.my_method_menu.show()

    def run_my_lessons_menu(self):
        self.my_lessons_menu = MyLessonsMenu(self)
        self.my_lessons_menu.setAttribute(Qt.WA_DeleteOnClose)
        self.my_lessons_menu.back_menu_event.connect(self.close_my_lessons_menu_on_menu)
        self.my_lessons_menu.show()

    def close_my_lessons_menu_on_menu(self):
        self.my_lessons_menu.close()
        self.my_lessons_menu = None
        self.run_menu()

    def close_menu_on_my_lessons_menu(self):
        self.menu.close()
        self.menu = None
        self.run_my_lessons_menu()

    def close_menu_on_constructor(self, data):
        self.menu.close()
        self.menu = None
        self.run_constructor(data)

    def close_my_method_on_menu(self):
        self.my_method_menu.close()
        self.my_method_menu = None
        self.run_menu()

    def close_new_method_on_my_method(self):
        self.new_method.close()
        self.new_method = None
        self.run_my_method_menu()

    def close_menu_on_my_method(self):
        self.menu.close()
        self.menu = None
        self.run_my_method_menu()

    def close_result_on_constructor(self, data):
        self.result.close()
        self.result = None
        self.run_constructor(data)

    def close_constructor_on_result(self, data):
        self.constructor.close()
        self.constructor = None
        self.run_result(data)

    def close_constructor_on_menu(self):
        self.constructor.close()
        self.constructor = None
        self.run_menu()

    def close_result_on_menu(self):
        self.result.close()
        self.result = None
        self.run_menu()


class Menu(QWidget):
    create_my_methods_event = pyqtSignal()
    create_my_lessons_menu_event = pyqtSignal()
    create_my_constructor_event = pyqtSignal(dict)

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
        layout_btn_menu.setContentsMargins(int(self.window().width() / 20.5), int(self.window().width() / 18.5),
                                           int(self.window().width() / 6.5), int(self.window().width() / 6.5))

        self.btn_profile_login = QPushButton("Войти", self)
        self.btn_profile_login.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.normal.normal_xy(200, 0)[0]}px;'
            'background-color: #FFA25F;'
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
        layout_btn_menu.addWidget(self.btn_profile_login, 0, 0)
        self.btn_profile_login.clicked.connect(self.login_user)

        self.btn_profile_exit = QPushButton("Выйти", self)
        self.btn_profile_exit.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.normal.normal_xy(200, 0)[0]}px;'
            'background-color: #FFA25F;'
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
        layout_btn_menu.addWidget(self.btn_profile_exit, 0, 0)
        self.btn_profile_exit.clicked.connect(self.exit_user)

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
        layout_btn_menu.addWidget(self.btn_new_lesson, 1, 0)
        self.btn_new_lesson.clicked.connect(self.create_new_lesson)

        self.btn_my_methods = QPushButton("Мои методики", self)
        self.btn_my_methods.setStyleSheet(
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
        layout_btn_menu.addWidget(self.btn_my_methods, 2, 0)
        self.btn_my_methods.clicked.connect(self.create_my_methods)

        self.btn_my_lessons = QPushButton("Мои уроки", self)
        self.btn_my_lessons.setStyleSheet(
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
        layout_btn_menu.addWidget(self.btn_my_lessons, 3, 0)
        self.btn_my_lessons.clicked.connect(self.create_my_lessons_menu)

        if id_current_user is None:
            self.btn_my_lessons.hide()
            self.btn_my_methods.hide()
            self.btn_profile_exit.hide()
            self.btn_profile_login.show()

        widget_btn = QWidget()
        widget_btn.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        widget_btn.setLayout(layout_btn_menu)
        layout_menu.addWidget(widget_btn, 0, 0, 0, 3)

        # Цитата в главном меню
        session = db_session.create_session()
        self.quote = QLabel(random.choice(session.query(Quote).all()).text, self)
        self.quote.setWordWrap(True)
        self.quote.setStyleSheet(
            '.QLabel {font-family: "Impact";'
            'font: ' + self.normal.normal_font(55) + 'px}'
        )
        layout_menu.addWidget(self.quote, 0, 3, 3, 5)
        self.setLayout(layout_menu)

    def create_new_lesson(self):
        self.hide()
        self.new_lesson = NewLesson(self.main_window)
        if self.new_lesson.exec_() == QDialog.Accepted:
            self.create_my_constructor_event.emit(self.new_lesson.data)
        else:
            self.show()

    def create_my_methods(self):
        self.create_my_methods_event.emit()

    def create_my_lessons_menu(self):
        self.create_my_lessons_menu_event.emit()

    def login_user(self):
        self.hide()
        self.login = Login(self.main_window)
        if self.login.exec_() == QDialog.Accepted:
            self.btn_profile_login.hide()
            self.btn_profile_exit.show()

            self.btn_my_lessons.show()
            self.btn_my_methods.show()

            global id_current_user
            id_current_user = self.login.id_user
        self.show()

    def exit_user(self):
        global id_current_user
        id_current_user = None
        self.btn_my_lessons.hide()
        self.btn_my_methods.hide()
        self.btn_profile_exit.hide()
        self.btn_profile_login.show()


class MyLessonsMenu(QWidget):
    back_menu_event = pyqtSignal()

    def __init__(self, main_window):
        super(MyLessonsMenu, self).__init__(main_window)
        self.main_window = main_window
        self.setGeometry(0, 0, self.main_window.geometry.width(), self.main_window.geometry.height())
        self.initUI()

    def initUI(self):
        layout_my_lessons_menu = QGridLayout()
        layout_my_lessons_menu.setContentsMargins(int(self.window().width() / 10.5), int(self.window().width() / 35.5),
                                                  int(self.window().width() / 10.5), int(self.window().width() / 25.5))
        # -----------------------------------------

        # -----------------------------------------
        layout_my_lessons_menu_head = QHBoxLayout()
        self.btn_back = QPushButton()
        self.btn_back.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        layout_my_lessons_menu_head.addWidget(self.btn_back)
        self.btn_back.clicked.connect(self.back)
        # -----------------------------------------
        layout_found = QHBoxLayout()

        self.line_edit_found_my_lessons_menu = QLineEdit()
        self.line_edit_found_my_lessons_menu.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(22)}px;"
            "}"
        )
        self.line_edit_found_my_lessons_menu.setFixedHeight(int(self.window().width() / 30.5))
        self.line_edit_found_my_lessons_menu.textChanged.connect(self.found)
        layout_found.addWidget(self.line_edit_found_my_lessons_menu)

        self.btn_found = QPushButton()
        self.btn_found.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_FOUND});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_FOUND_HOVER});'
            '}'
        )
        self.btn_found.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_found.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        self.btn_found.clicked.connect(self.found)
        layout_found.addWidget(self.btn_found)

        widget_found = QWidget()
        widget_found.setLayout(layout_found)
        widget_found.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )

        layout_my_lessons_menu_head.addWidget(widget_found)
        # -----------------------------------------

        widget_my_lessons_menu_head = QWidget()
        widget_my_lessons_menu_head.setLayout(layout_my_lessons_menu_head)
        widget_my_lessons_menu_head.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )

        layout_my_lessons_menu.addWidget(widget_my_lessons_menu_head, 0, 0)
        # -----------------------------------------

        # -----------------------------------------

        self.scroll_my_lessons_menu = QScrollArea(self)
        self.scroll_my_lessons_menu.setStyleSheet(
            ".QScrollArea {"
            "background-color:transparent;"
            "}"
        )
        self.scroll_my_lessons_menu.setFrameShape(QFrame.NoFrame)
        self.scroll_my_lessons_menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_my_lessons_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout_my_lessons_menu.addWidget(self.scroll_my_lessons_menu, 1, 0)

        self.setLayout(layout_my_lessons_menu)
        session = db_session.create_session()
        self.filter_my_lessons_menu = session.query(DocumentsLesson).filter(
            DocumentsLesson.id_user.like(id_current_user)).all()
        self.show_my_lessons_menu()

    def show_my_lessons_menu(self):
        object_my_lessons = []

        layout = QVBoxLayout()
        for i in range(len(self.filter_my_lessons_menu)):
            object_my_lessons.append(MyLesson(self, self.filter_my_lessons_menu[i]))
            layout.addWidget(object_my_lessons[i])

        self.widget_list_my_lessons = QWidget(self)
        self.widget_list_my_lessons.setGeometry(0, 0, int(self.window().width() / 1.25),
                                                116 * len(self.filter_my_lessons_menu))
        self.widget_list_my_lessons.setLayout(layout)
        self.widget_list_my_lessons.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        self.scroll_my_lessons_menu.setWidget(self.widget_list_my_lessons)
        self.scroll_my_lessons_menu.show()

    def found(self):
        session = db_session.create_session()
        self.filter_my_lessons_menu = session.query(DocumentsLesson).filter(
            DocumentsLesson.lesson_topic.like(f"%{self.line_edit_found_my_lessons_menu.text().lower()}%") |
            DocumentsLesson.subject.like(f"%{self.line_edit_found_my_lessons_menu.text().lower()}%")).all()
        self.show_my_lessons_menu()

    def back(self):
        self.back_menu_event.emit()


class MyLesson(QWidget):
    def __init__(self, main_window, data):
        super(MyLesson, self).__init__(main_window.main_window)
        self.main_window = main_window
        self.data = data
        self.initUI()

    def initUI(self):
        self.background = QLabel(self)
        self.background.setStyleSheet(
            '.QLabel {'
            f'min-height: {100}px;'
            f'min-width: {int(self.main_window.window().width() / 1.29)}px;'
            'margin-bottom: 16px;'
            'background-color: #FFA25F;'
            'border-radius: 14px'
            '}'
        )
        layout = QHBoxLayout(self)

        self.label_date = QLabel(QDateTime().fromTime_t(self.data.date).toString("dd-MM-yyyy hh:mm"), self)
        self.label_date.setWordWrap(True)
        self.label_date.setStyleSheet(
            ".QLabel {"
            f"margin-left: {int(self.main_window.window().width() / 25.5)};"
            f"font: bold {self.main_window.main_window.normal.normal_font(24)}px;"
            "}"
        )
        layout.addWidget(self.label_date)

        self.label_lesson_topic = QLabel(self.data.lesson_topic[0].upper() + self.data.lesson_topic[1:].lower(), self)
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"margin-left: {int(self.main_window.window().width() / 25.5)};"
            f"font: bold {self.main_window.main_window.normal.normal_font(24)}px;"
            "}"
        )
        layout.addWidget(self.label_lesson_topic)

        self.btn_more_details = QPushButton(self)
        self.btn_more_details.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_PADROBNEE_HOVER});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_PADROBNEE});'
            '}'
        )
        self.btn_more_details.setMinimumSize(*self.main_window.main_window.normal.normal_proportion(175, 60))
        self.btn_more_details.setFixedWidth(self.main_window.main_window.normal.normal_proportion(175, 0)[0])
        layout.addWidget(self.btn_more_details)

        self.btn_del = QPushButton(self)
        self.btn_del.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_DEL});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_DEL_HOVER});'
            '}'
        )
        self.btn_del.setMinimumSize(*self.main_window.main_window.normal.normal_proportion(40, 40))
        self.btn_del.setFixedWidth(self.main_window.main_window.normal.normal_proportion(40, 0)[0])
        layout.addWidget(self.btn_del)

        self.btn_del.clicked.connect(self.del_lesson)
        self.btn_more_details.clicked.connect(self.more_details)

    def del_lesson(self):
        session = db_session.create_session()
        lesson = session.query(DocumentsLesson).filter(DocumentsLesson.id == self.data.id).first()
        session.delete(lesson)
        session.commit()
        self.main_window.filter_my_lessons_menu = session.query(DocumentsLesson).filter(
            DocumentsLesson.id_user.like(id_current_user)).all()
        self.main_window.show_my_lessons_menu()

    def more_details(self):
        self.main_window.setDisabled(True)
        self.document_lesson = DocumentLesson(self.main_window, self.data)
        if self.document_lesson.exec_() == QDialog.Accepted:
            pass
        self.main_window.setDisabled(False)


class DocumentLesson(QDialog):
    def __init__(self, main_window, data):
        QDialog.__init__(self)
        self.main_window = main_window.main_window
        self.data = data
        self.setParent(self.main_window)
        self.setGeometry(int(self.main_window.geometry.width() / 6), int(self.main_window.geometry.height() / 6),
                         int(self.main_window.geometry.width() / 1.5), int(self.main_window.geometry.height() / 1.5))
        self.initUI()

    def initUI(self):
        self.background_form_options_document_lesson = QLabel(self)
        self.background_form_options_document_lesson.setStyleSheet(
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
        self.background_form_options_document_lesson.resize(self.geometry().width(), self.geometry().height())

        layout_document_lesson = QGridLayout()
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
        self.btn_save_lesson.clicked.connect(self.save_lesson)
        layout_document_lesson.addWidget(self.btn_save_lesson, 0, 0)

        self.document_result = QTextEdit(self)
        layout_document_lesson.addWidget(self.document_result, 0, 1, 0, 3)

        self.setLayout(layout_document_lesson)

        # -----------------------------------------
        self.btn_back = QPushButton(self)
        self.btn_back.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back.move(15, 5)
        self.btn_back.clicked.connect(self.back_my_lessons_menu)
        # -----------------------------------------

    def back_my_lessons_menu(self):
        self.reject()

    def save_lesson(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение файла", None, "Text files (*.docx *doc)")[0]
        if file_name != "":

            teacher = session.query(User).filter(User.id == id_current_user).first().name_user
            methods = []
            for id_method in self.data.ids.split(";"):
                method = session.query(Methods).filter(Methods.id == id_method).first()
                methods.append(
                    [session.query(TypeMethod).filter(
                        TypeMethod.id == method.id_type_method).first().name_method,
                     method.name_method, method.text, method.time])

            document = get_document_result_word(self.data.lesson_topic, teacher, self.data.subject,
                                                self.data.class_lesson, self.data.lesson_duration,
                                                self.data.competence.split(';'), methods)

            document.save(f'{file_name}')
            QMessageBox.information(self, "Ок", "Урок сохранен", QMessageBox.Ok)
            self.accept()


class Login(QDialog):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.main_window = main_window
        self.setParent(self.main_window)
        self.setGeometry(self.main_window.geometry.width() // 3.5, self.main_window.geometry.height() // 3.5,
                         self.main_window.geometry.width() // 2.5, self.main_window.geometry.height() // 2.5)
        self.initUI()

    def initUI(self):
        self.background_form = QLabel(self)
        self.background_form.setStyleSheet(
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
        self.background_form.resize(self.geometry().width(), self.geometry().height())

        self.text_login = QLabel("Email")
        self.text_login.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_password = QLabel("Пароль")
        self.text_password.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )

        # Поля ввода значений
        # -----------------------------------------
        self.edit_email = QLineEdit()
        self.edit_email.setFixedHeight(int(self.window().width() / 35.5))
        self.edit_email.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )

        self.edit_password = QLineEdit()
        self.edit_password.setFixedHeight(int(self.window().width() / 35.5))
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )

        self.btn_registration = QPushButton("Регистрация", self)
        self.btn_registration.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.main_window.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.main_window.normal.normal_xy(200, 0)[0]}px;'
            'background-color: #FFA25F;'
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
        self.btn_registration.clicked.connect(self.registration_user)

        # -----------------------------------------
        self.btn_back = QPushButton(self)
        self.btn_back.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back.move(15, 5)
        self.btn_back.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok = QPushButton("Войти")
        self.btn_ok.setStyleSheet(
            '.QPushButton {'
            f'min-height: {self.main_window.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.main_window.normal.normal_xy(200, 0)[0]}px;'
            'background-color: #30B713;'
            'border-style: outset;'
            'border-width: 2px;'
            'border-radius: 10px;'
            'border-color: beige;'
            'font: bold ' + self.main_window.normal.normal_font(17) + 'px;'
                                                                      'min-width: 10em;'
                                                                      'padding: 6px;'
                                                                      '}'
                                                                      '.QPushButton:hover {'
                                                                      'background-color: #26960B;'
                                                                      'border-style: inset;'
                                                                      '}'
        )
        self.btn_ok.clicked.connect(self.valid_options)
        # -----------------------------------------

        layout_new_method = QGridLayout()
        layout_new_method.setContentsMargins(int(self.window().width() / 25.5), int(self.window().width() / 25.5),
                                             int(self.window().width() / 25.5), int(self.window().width() / 35.5))
        layout_new_method.addWidget(self.text_login, 0, 0)
        layout_new_method.addWidget(self.edit_email, 0, 1)

        layout_new_method.addWidget(self.text_password, 1, 0)
        layout_new_method.addWidget(self.edit_password, 1, 1)

        layout_new_method.addWidget(self.btn_ok, 2, 0, 1, 2)
        layout_new_method.addWidget(self.btn_registration, 3, 0, 1, 2)

        self.setLayout(layout_new_method)

    def back_menu(self):
        self.reject()

    def valid_options(self):
        session = db_session.create_session()
        user = session.query(User).filter(User.email == self.edit_email.text()).first()
        if self.edit_email.text() == "" or self.edit_password.text() == "":
            QMessageBox.critical(self, "Ошибка", "Вы заполнили не все поля", QMessageBox.Ok)
        elif user is None:
            QMessageBox.critical(self, "Ошибка", "Учителя с таким email не существует", QMessageBox.Ok)
        elif User.validation_email(self.edit_email.text()):
            QMessageBox.critical(self, "Ошибка", "Неверный email", QMessageBox.Ok)
        elif not user.check_password(self.edit_password.text()):
            QMessageBox.critical(self, "Ошибка", "Неверный пароль", QMessageBox.Ok)
        else:
            self.id_user = user.id
            self.accept()

    def registration_user(self):
        self.hide()
        self.registration = Registration(self.main_window)
        if self.registration.exec_() == QDialog.Accepted:
            self.id_user = self.registration.id_user
            self.accept()
        else:
            self.back_menu()


class Registration(QDialog):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.main_window = main_window
        self.setParent(self.main_window)
        self.setGeometry(self.main_window.geometry.width() // 4, self.main_window.geometry.height() // 4,
                         self.main_window.geometry.width() // 2, self.main_window.geometry.height() // 2)
        self.initUI()

    def initUI(self):
        self.background_form = QLabel(self)
        self.background_form.setStyleSheet(
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
        self.background_form.resize(self.geometry().width(), self.geometry().height())

        self.text_name = QLabel("ФИО")
        self.text_name.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_login = QLabel("Email")
        self.text_login.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_password = QLabel("Пароль")
        self.text_password.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )
        # -----------------------------------------
        self.text_repeat_password = QLabel("Повторите пароль")
        self.text_repeat_password.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 12em;"
            "}"
        )

        # -----------------------------------------
        # Поля ввода значений
        # -----------------------------------------
        self.edit_name = QLineEdit()
        self.edit_name.setFixedHeight(int(self.window().width() / 35.5))
        self.edit_name.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.edit_email = QLineEdit()
        self.edit_email.setFixedHeight(int(self.window().width() / 35.5))
        self.edit_email.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.edit_password = QLineEdit()
        self.edit_password.setFixedHeight(int(self.window().width() / 35.5))
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.edit_password.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.edit_repeat_password = QLineEdit()
        self.edit_repeat_password.setFixedHeight(int(self.window().width() / 35.5))
        self.edit_repeat_password.setEchoMode(QLineEdit.Password)
        self.edit_repeat_password.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.btn_back = QPushButton(self)
        self.btn_back.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back.move(15, 5)
        self.btn_back.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok = QPushButton(self)
        self.btn_ok.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}'
        )
        self.btn_ok.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok.move(self.geometry().width() - self.main_window.normal.normal_proportion(75, 0)[0] - 12, 5)
        self.btn_ok.clicked.connect(self.valid_options)
        # -----------------------------------------

        layout_new_method = QGridLayout()
        layout_new_method.setContentsMargins(int(self.window().width() / 25.5), int(self.window().width() / 20.5),
                                             int(self.window().width() / 25.5), int(self.window().width() / 50.5))
        layout_new_method.addWidget(self.text_name, 0, 0)
        layout_new_method.addWidget(self.edit_name, 0, 1)

        layout_new_method.addWidget(self.text_login, 1, 0)
        layout_new_method.addWidget(self.edit_email, 1, 1)

        layout_new_method.addWidget(self.text_password, 2, 0)
        layout_new_method.addWidget(self.edit_password, 2, 1)

        layout_new_method.addWidget(self.text_repeat_password, 3, 0)
        layout_new_method.addWidget(self.edit_repeat_password, 3, 1)

        self.setLayout(layout_new_method)

    def back_menu(self):
        self.reject()

    def valid_options(self):
        session = db_session.create_session()
        if self.edit_email.text() == "" \
                or self.edit_name.text() == "" \
                or self.edit_repeat_password.text() == "" \
                or self.edit_password.text() == "":
            QMessageBox.critical(self, "Ошибка", "Вы заполнили не все поля", QMessageBox.Ok)

        elif session.query(User).filter(User.email == self.edit_email.text()).first():
            QMessageBox.critical(self, "Ошибка", "Учитель с таким email уже существует", QMessageBox.Ok)
        elif User.validation_email(self.edit_email.text()):
            QMessageBox.critical(self, "Ошибка", "Неверный email", QMessageBox.Ok)
        elif self.edit_password.text() != self.edit_repeat_password.text():
            QMessageBox.critical(self, "Ошибка", "Пароли не совпадают", QMessageBox.Ok)
        elif len(self.edit_password.text()) < 6:
            QMessageBox.critical(self, "Ошибка", "Пароль слишком короткий", QMessageBox.Ok)
        else:
            user = User(
                name_user=self.edit_name.text().lower(),
                email=self.edit_email.text(),
            )
            user.set_password(self.edit_password.text())
            session.add(user)
            session.commit()
            self.id_user = user.id
            self.accept()


class NewLesson(QDialog):
    def __init__(self, main_window):
        QDialog.__init__(self)
        self.main_window = main_window
        self.setParent(self.main_window)
        self.setGeometry(self.main_window.geometry.width() // 4.8, self.main_window.geometry.height() // 4.8,
                         self.main_window.geometry.width() // 1.7, self.main_window.geometry.height() // 1.7)
        self.initUI()

    def initUI(self):
        session = db_session.create_session()

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
        self.combo_subjects.addItems([item.name_subject for item in session.query(Subject).all()])
        self.combo_subjects.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_lesson_type = QComboBox()
        self.combo_lesson_type.addItems([item.name_lesson_type for item in session.query(LessonType).all()])
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
                                                  in session.query(ClassCharacteristic).all()])
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
        self.check_creative_thinking = QCheckBox('Креативное \nмышление')
        self.check_creative_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_critical_thinking = QCheckBox('Критическое \nмышление')
        self.check_critical_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_metacognitive_skills = QCheckBox('Метакогнитивные \nнавыки')
        self.check_metacognitive_skills.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.btn_back = QPushButton(self)
        self.btn_back.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back.move(15, 5)
        self.btn_back.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok = QPushButton(self)
        self.btn_ok.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}'
        )
        self.btn_ok.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok.move(self.geometry().width() - self.main_window.normal.normal_proportion(75, 0)[0] - 12, 5)
        self.btn_ok.clicked.connect(self.valid_options_new_lesson)

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
        self.reject()

    def valid_options_new_lesson(self):
        if self.edit_lesson_topic.text() != "" and \
                self.edit_lesson_duration.value() >= 20 and \
                (self.check_creative_thinking.isChecked() or
                 self.check_literacy.isChecked() or
                 self.check_communication.isChecked() or
                 self.check_cooperation.isChecked() or
                 self.check_critical_thinking.isChecked() or
                 self.check_metacognitive_skills.isChecked()):

            self.data = {
                "lesson_topic": self.edit_lesson_topic.text().lower(),
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
            }
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Вы заполнили не все поля", QMessageBox.Ok)


class Constructor(QWidget):
    back_menu_event = pyqtSignal()
    create_result_event = pyqtSignal(dict)

    def __init__(self, main_window, data):
        super().__init__(main_window)
        self.data = data
        self.main_window = main_window
        self.setGeometry(0, 0, self.main_window.geometry.width(), self.main_window.geometry.height())

        session = db_session.create_session()
        self.filter_methods = session.query(Methods).filter(
            or_(Methods.is_local == False, Methods.id_user == id_current_user),
            or_(Methods.creative_thinking == self.data['competence']['creative_thinking'],
                Methods.critical_thinking == self.data['competence']['critical_thinking'],
                Methods.communication == self.data['competence']['communication'],
                Methods.cooperation == self.data['competence']['cooperation'],
                Methods.metacognitive_skills == self.data['competence']['metacognitive_skills'],
                Methods.literacy == self.data['competence']['literacy']))

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
        if self.data['acquaintance']:
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
        if self.data['acquaintance']:
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
        if self.data['acquaintance']:
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
        layout_2 = QVBoxLayout()
        layout_found = QHBoxLayout()

        self.line_edit_found_method = QLineEdit()
        self.line_edit_found_method.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(22)}px;"
            "}"
        )
        self.line_edit_found_method.setFixedHeight(int(self.window().width() / 30.5))
        self.line_edit_found_method.textChanged.connect(self.found)
        layout_found.addWidget(self.line_edit_found_method)

        self.btn_found = QPushButton()
        self.btn_found.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_FOUND});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_FOUND_HOVER});'
            '}'
        )
        self.btn_found.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_found.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        self.btn_found.clicked.connect(self.found)
        layout_found.addWidget(self.btn_found)

        layout_2.addLayout(layout_found)

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
        layout_2.addWidget(self.scroll_main_methods)

        widget_2 = QWidget()
        widget_2.setLayout(layout_2)
        widget_2.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        self.layout_constructor_h_3.addWidget(widget_2, 0, 1, 0, 3)

        layout_3_constructor = QVBoxLayout()
        # -------------------------------------------
        layout_time_back_ok = QHBoxLayout()
        self.time_lesson = QLabel(f"Время урока: {self.data['lesson_duration']} минут")
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
        self.btn_ok_constructor.clicked.connect(self.volid_data)

        layout_3_constructor.addLayout(layout_time_back_ok)
        # -------------------------------------------
        self.scroll_my_methods = QScrollArea(self)
        self.scroll_my_methods.setStyleSheet(
            ".QScrollArea {"
            "background-color:transparent;"
            "}"
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
        self.layout_constructor_h_3.addLayout(layout_3_constructor, 0, 4, 0, 2)

    def button_stage_flag(self, button):
        session = db_session.create_session()
        self.flag_stage = session.query(Stage).filter(Stage.name_stage == button.text()).first().id
        self.filter_stage_methods = self.filter_methods.filter(Methods.id_stage_method.like(self.flag_stage)).all()
        self.show_methods_stage()

    def save_lesson(self):
        session = db_session.create_session()
        if id_current_user is None:
            QMessageBox.critical(self, "Ошибка", "Вы не авторизированы", QMessageBox.Ok)

        elif int(self.time_lesson.text().split()[2]) != 0:
            QMessageBox.critical(self, "Ошибка", "Вы не использовали все время урока", QMessageBox.Ok)

        else:
            if self.data["lesson_topic"] in [item.name for item in session.query(SaveLesson).filter(
                    SaveLesson.id_user == id_current_user).all()]:
                reply = QMessageBox.question(self, "Предупреждение",
                                             "Урок с таким названием уже сущестует. Вы хотите перезаписать?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    lesson = session.query(SaveLesson).filter(
                        SaveLesson.name == self.data["lesson_topic"],
                        SaveLesson.id_user == id_current_user).first()
                    session.delete(lesson)
                    session.commit()
                    save_lesson = SaveLesson(
                        name=self.data["lesson_topic"],
                        ids=';'.join([str(method.data.id) for method in self.my_methods]),
                        id_user=id_current_user,
                    )
                    session.add(save_lesson)
                    session.commit()
                    QMessageBox.information(self, "Ок", "Урок сохранен", QMessageBox.Ok)
            else:
                save_lesson = SaveLesson(
                    name=self.data["lesson_topic"],
                    ids=';'.join([str(method.data.id) for method in self.my_methods]),
                    id_user=id_current_user,
                )
                session.add(save_lesson)
                session.commit()
                QMessageBox.information(self, "Ок", "Урок сохранен", QMessageBox.Ok)

    def open_lesson(self):
        if not id_current_user is None:
            self.open = QDialog()
            self.open.setWindowTitle("Открыть")
            self.open.resize(*self.main_window.normal.normal_proportion(300, 150))
            self.list_view = QListWidget(self.open)
            self.list_view.resize(*self.main_window.normal.normal_proportion(300, 150))
            session = db_session.create_session()
            self.list_view.addItems([item.name for item in session.query(SaveLesson).filter(
                SaveLesson.id_user == id_current_user).all()])
            self.list_view.doubleClicked.connect(self.open_select_lesson)
            self.open.exec()
        else:
            QMessageBox.critical(self, "Ошибка", "Вы не авторизированы", QMessageBox.Ok)

    def open_select_lesson(self):
        self.open.close()
        self.my_methods = []
        session = db_session.create_session()
        for id_method in session.query(SaveLesson).filter(
                SaveLesson.name == self.list_view.currentItem().text(),
                SaveLesson.id_user == id_current_user).first().ids.split(";"):
            self.my_methods.append(Method(self, session.query(Methods).filter(Methods.id == id_method).first()))
            self.my_methods[-1].btn_add.hide()
            self.my_methods[-1].btn_del.show()
            self.my_methods[-1].background.setStyleSheet(
                '.QLabel {'
                f'min-height: {100}px;'
                f'min-width: {int(self.my_methods[-1].main_window.scroll_my_methods.size().width())}px;'
                'margin-bottom: 16px;'
                'background-color: #FFA25F;'
                '}'
            )
        self.my_methods[0].show_my_methods()
        self.my_methods[0].show_time_methods()
        self.filter_stage_methods = self.filter_methods.filter(Methods.id_stage_method.like(self.flag_stage)).all()
        self.show_methods_stage()

    def del_lesson(self):
        if not id_current_user is None:
            self.delete = QDialog()
            self.delete.setWindowTitle("Удалить")
            self.delete.resize(*self.main_window.normal.normal_proportion(300, 150))
            self.list_view = QListWidget(self.delete)
            self.list_view.resize(*self.main_window.normal.normal_proportion(300, 150))
            session = db_session.create_session()
            self.list_view.addItems([item.name for item in session.query(SaveLesson).filter(
                SaveLesson.id_user == id_current_user).all()])
            self.list_view.doubleClicked.connect(self.del_select_lesson)
            self.delete.exec()
        else:
            QMessageBox.critical(self, "Ошибка", "Вы не авторизированы", QMessageBox.Ok)

    def del_select_lesson(self):
        self.delete.close()
        reply = QMessageBox.question(self, "Удаление", "Вы хотите удалить урок?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            session = db_session.create_session()
            lesson = session.query(SaveLesson).filter(
                SaveLesson.name == self.list_view.currentItem().text(),
                SaveLesson.id_user == id_current_user).first()
            session.delete(lesson)
            session.commit()

    def back_new_lesson(self):
        self.back_menu_event.emit()

    def volid_data(self):
        if int(self.time_lesson.text().split()[2]) == 0:
            self.create_result_event.emit(
                {
                    "methods": self.my_methods,
                    "lesson_topic": self.data["lesson_topic"],
                    "subject": self.data["subject"],
                    "lesson_type": self.data["lesson_type"],
                    "class": self.data["class"],
                    "class_characteristic": self.data["class_characteristic"],
                    "lesson_duration": self.data["lesson_duration"],
                    "acquaintance": self.data["acquaintance"],
                    "competence": {
                        "creative_thinking": self.data["competence"]["creative_thinking"],
                        "literacy": self.data["competence"]["literacy"],
                        "communication": self.data["competence"]["communication"],
                        "cooperation": self.data["competence"]["cooperation"],
                        "critical_thinking": self.data["competence"]["critical_thinking"],
                        "metacognitive_skills": self.data["competence"]["metacognitive_skills"]
                    }
                })
        else:
            QMessageBox.critical(self, "Ошибка", "Вы не использовали все время урока", QMessageBox.Ok)

    def show_methods_stage(self):
        # Удаление всех элементов из прошлого списка обектов методов
        for i in reversed(range(len(self.object_methods))):
            del self.object_methods[i]

        # Список id выбранных мной методов
        id_my_methods = [method.data.id for method in self.my_methods]

        # Удаляем все методы, входящие в список моих методов из общего списка
        # Чтобы повторно не отображать методы в панели
        for i in reversed(range(len(self.filter_stage_methods))):
            if self.filter_stage_methods[i].id in id_my_methods:
                del self.filter_stage_methods[i]

        # Создаем обекты-методы вносим их в лейаут
        layout = QVBoxLayout()
        for i in range(len(self.filter_stage_methods)):
            self.object_methods.append(Method(self, self.filter_stage_methods[i]))
            layout.addWidget(self.object_methods[i])

        widget = QWidget()
        widget.setGeometry(0, 0, int(self.main_window.geometry.height() / 1.1), 116 * len(self.filter_stage_methods))
        widget.setLayout(layout)
        widget.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        self.scroll_main_methods.setWidget(widget)
        self.scroll_main_methods.show()

    def found(self):
        self.filter_stage_methods = self.filter_methods.filter(
            Methods.id_stage_method.like(self.flag_stage),
            (Methods.name_method.like(f"%{self.line_edit_found_method.text().lower()}%") |
             Methods.text.like(f"%{self.line_edit_found_method.text().lower()}%"))).all()
        self.show_methods_stage()


class Method(QWidget):
    def __init__(self, main_window, data):
        super(Method, self).__init__(main_window.main_window)
        self.main_window = main_window
        self.data = data
        self.setGeometry(0, 0,
                         self.main_window.scroll_main_methods.size().width(), 100)
        self.initUI()

    def initUI(self):
        self.background = QLabel(self)
        self.background.setStyleSheet(
            '.QLabel {'
            f'min-height: {100}px;'
            f'min-width: {int(self.main_window.scroll_main_methods.size().width() / 1.1)}px;'
            'margin-bottom: 16px;'
            'background-color: #FFA25F;'
            'border-radius: 14px'
            '}'
        )
        layout = QHBoxLayout()

        self.method_time = QLabel(self.data.time + "'   ")
        self.method_time.setStyleSheet(
            '.QLabel {'
            'font-family: "Impact";'
            f"font: bold {self.main_window.main_window.normal.normal_font(24)}px;"
            '}'
        )
        self.method_time.setWordWrap(True)
        layout.addWidget(self.method_time, 0)

        self.label_lesson_topic = QLabel(self.data.name_method[0].upper() + self.data.name_method[1:].lower())
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.main_window.normal.normal_font(24)}px;"
            "}"
        )
        layout.addWidget(self.label_lesson_topic, 1)

        self.setLayout(layout)

        self.btn_more_details = QPushButton(self)
        self.btn_more_details.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_PADROBNEE});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_PADROBNEE_HOVER});'
            '}'
        )
        self.btn_more_details.setFixedSize(*self.main_window.main_window.normal.normal_proportion(175, 60))
        self.btn_more_details.move(int(self.main_window.scroll_main_methods.size().width() / 1.15) -
                                   self.main_window.main_window.normal.normal_proportion(205, 0)[0],
                                   (100 - self.main_window.main_window.normal.normal_proportion(40, 0)[0]) // 2)

        self.btn_add = QPushButton(self)
        self.btn_add.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_ADD});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_ADD_HOVER});'
            '}'
        )
        self.btn_add.setFixedSize(*self.main_window.main_window.normal.normal_proportion(40, 40))
        self.btn_add.move(int(self.main_window.scroll_main_methods.size().width() / 1.1) -
                          self.main_window.main_window.normal.normal_proportion(20, 0)[0],
                          (100 - self.main_window.main_window.normal.normal_proportion(40, 0)[0]) // 2)

        self.btn_del = QPushButton(self)
        self.btn_del.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_DEL});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_DEL_HOVER});'
            '}'
        )
        self.btn_del.setFixedSize(*self.main_window.main_window.normal.normal_proportion(40, 40))
        self.btn_del.move(int(self.main_window.scroll_main_methods.size().width() / 1.1) -
                          self.main_window.main_window.normal.normal_proportion(20, 0)[0],
                          (100 - self.main_window.main_window.normal.normal_proportion(60, 0)[0]) // 2)
        self.btn_del.hide()

        self.btn_add.clicked.connect(self.add_method)
        self.btn_del.clicked.connect(self.del_method)
        self.btn_more_details.clicked.connect(self.details)

    def add_method(self):
        time_my_methods = [int(method.data.time) for method in self.main_window.my_methods]
        if sum(time_my_methods) + int(self.data.time) <= self.main_window.data['lesson_duration'] + 20:
            self.main_window.my_methods.append(self)

            self.show_my_methods()
            self.btn_add.hide()
            self.btn_del.show()
            self.main_window.filter_stage_methods = self.main_window.filter_methods.filter(
                Methods.id_stage_method.like(self.main_window.flag_stage)).all()
            self.main_window.show_methods_stage()
            self.show_time_methods()

        else:
            QMessageBox.critical(self.main_window, "Ошибка", "Превышен лимит времени", QMessageBox.Ok)
            return

    def del_method(self):
        del self.main_window.my_methods[self.main_window.my_methods.index(self)]
        self.show_my_methods()
        self.main_window.filter_stage_methods = self.main_window.filter_methods.filter(
            Methods.id_stage_method.like(self.main_window.flag_stage)).all()
        self.main_window.show_methods_stage()
        self.show_time_methods()

    def show_my_methods(self):
        layout = QGridLayout()
        for method in self.main_window.my_methods:
            method.setFixedHeight(80)
            method.background.setStyleSheet(
                '.QLabel {'
                f'min-height: {80}px;'
                f'min-width: {int(method.main_window.scroll_my_methods.size().width() / 1.1)}px;'
                'margin-bottom: 16px;'
                'background-color: #FFA25F;'
                '}'
            )
            method.background.setFixedWidth(int(self.main_window.scroll_my_methods.size().width() / 1.1))

            method.btn_more_details.move(int(method.main_window.scroll_my_methods.size().width() / 1.15) -
                                         method.main_window.main_window.normal.normal_proportion(205, 0)[0],
                                         (80 - method.main_window.main_window.normal.normal_proportion(40, 0)[0]) // 2)

            method.btn_del.move(int(method.main_window.scroll_my_methods.size().width() / 1.1) -
                                self.main_window.main_window.normal.normal_proportion(20, 0)[0],
                                (100 - method.main_window.main_window.normal.normal_proportion(60, 0)[0]) // 2)

            layout.addWidget(method)

        widget = QWidget()

        widget.setLayout(layout)
        widget.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        widget.setGeometry(0, 0, int(self.main_window.window().height() / 1.1), 96 * len(self.main_window.my_methods))
        self.main_window.scroll_my_methods.setWidget(widget)

    def show_time_methods(self):
        for method in self.main_window.my_methods:
            method.method_time.setText(method.data.time + "'")

        sum_1 = sum([int(method.data.time) for method in self.main_window.my_methods])
        if sum_1 > self.main_window.data['lesson_duration']:
            count = 0
            k = self.main_window.data['lesson_duration'] / sum_1
            for method in self.main_window.my_methods:
                cur_time = int(round(int(method.method_time.text()[:-1]) * k, 0))
                count += cur_time
                method.method_time.setText(str(cur_time) + "'")

            self.main_window.my_methods[-1].method_time.setText(str(
                int(self.main_window.my_methods[-1].method_time.text()[:-1]) + self.main_window.data[
                    'lesson_duration'] - count) + "'")
            sum_1 = sum([int(method.method_time.text()[:-1]) for method in self.main_window.my_methods])

        self.main_window.time_lesson.setText(
            "Время урока: " + str(self.main_window.data['lesson_duration'] - sum_1) + " минут")

    def details(self):
        self.method_info = MethodMoreDetails(self.data, self.main_window)
        self.method_info.show()


class MethodMoreDetails(QDialog):
    def __init__(self, data, main_window):
        super(QDialog, self).__init__()
        self.setWindowIcon(QIcon(PATH_SPLASH_SCREEN))
        self.setModal(True)
        self.setWindowTitle(data.name_method[0].upper() + data.name_method[1:].lower())
        self.setFixedSize(int(main_window.main_window.geometry.width() / 1.9),
                          int(main_window.main_window.geometry.height() / 1.9))
        self.main_window = main_window
        self.data = data
        self.initUI()

    def initUI(self):
        self.background = QLabel(self)
        self.background.setStyleSheet(
            '.QLabel {'
            'background-color: #76b7c7;'
            '}'
        )
        self.background.resize(int(self.main_window.main_window.geometry.width() / 1.9),
                               int(self.main_window.main_window.geometry.height() / 1.9))

        layout = QGridLayout(self)

        self.title_method = QLabel(self.data.name_method[0].upper() + self.data.name_method[1:].lower(), self)
        self.title_method.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.main_window.normal.normal_font(42)}px;"
            "}"
        )
        self.title_method.setWordWrap(True)
        layout.addWidget(self.title_method, 0, 0, 1, 4)

        session = db_session.create_session()
        classes = session.query(Classes).filter(Classes.id == self.data.id_classes_number).first().name_class
        author = session.query(User).filter(User.id == self.data.id_user).first().name_user
        self.time_and_сlass_method = QLabel(
            "\n   " + self.data.time + "' минут;    " + classes + " Класс   \n\n" +
            "   Автор: " + ' '.join([elem[0].upper() + elem[1:].lower() for elem in author.split()]) + "    \n", self)
        self.time_and_сlass_method.setStyleSheet(
            ".QLabel {"
            'background-color: #FFA25F;'
            f"font: bold {self.main_window.main_window.normal.normal_font(32)}px;"
            "}"
        )
        layout.addWidget(self.time_and_сlass_method, 1, 1, 1, 4)

        text = ''
        if self.data.text:
            for word in self.data.text.split():
                if word[-1] == ")" and word[-2].isdigit():
                    text += "\n"
                text += word + " "
        self.text_method = QLabel(text, self)
        self.text_method.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.main_window.normal.normal_font(18)}px;"
            "margin-bottom: 10%"
            "}"
        )
        self.text_method.setWordWrap(True)
        layout.addWidget(self.text_method, 2, 0)

        list_compet = [(self.data.creative_thinking, "- Креативное мышление"),
                       (self.data.critical_thinking, "- Критическое мышление"),
                       (self.data.literacy, "- Грамотность"),
                       (self.data.cooperation, "- Кооперация"),
                       (self.data.cooperation, "- Коммуникация"),
                       (self.data.metacognitive_skills, "- Метакогнитивные навыки")]
        list_compet = [i[1] for i in list_compet if i[0]]
        name_fgos = session.query(Fgos).filter(Fgos.id == self.data.id_fgos).first().name_fgos
        if name_fgos != "-":
            list_compet.append("- " + name_fgos + " навыки ФГОС")
        self.competence = QLabel("\n".join(list_compet), self)
        self.competence.setStyleSheet(
            ".QLabel {"
            f"font: bold {self.main_window.main_window.normal.normal_font(22)}px;"
            "margin-right: 20%;"
            "}"
        )
        layout.addWidget(self.competence, 2, 3)


class ResultLesson(QWidget):
    back_constructor_event = pyqtSignal(dict)
    back_menu_event = pyqtSignal()

    def __init__(self, main_window, data):
        super().__init__(main_window)
        self.data = data
        self.main_window = main_window
        self.setGeometry(0, 0, self.main_window.geometry.width(), self.main_window.geometry.height())

        self.initUI()

    def initUI(self):
        layout_result = QGridLayout(self)
        layout_result.setContentsMargins(int(self.window().width() / 10.5), int(self.window().width() / 25.5),
                                         int(self.window().width() / 15.5), int(self.window().width() / 25.5))

        layout_v_btn_result = QGridLayout(self)
        layout_v_btn_result.setContentsMargins(0, 0, int(self.window().width() / 15.5), 10)

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
        self.btn_save_lesson.clicked.connect(self.save_lesson)
        layout_v_btn_result.addWidget(self.btn_save_lesson, 1, 0, 1, 3)

        self.btn_menu = QPushButton("Меню", self)
        self.btn_menu.setStyleSheet(
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
        self.btn_menu.clicked.connect(self.back_menu)
        layout_v_btn_result.addWidget(self.btn_menu, 2, 0, 1, 3)

        widget_btn_result = QWidget(self)
        widget_btn_result.setLayout(layout_v_btn_result)
        widget_btn_result.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        layout_result.addWidget(widget_btn_result, 0, 0, 1, 2)

        competence = [(self.data["competence"]["creative_thinking"], "Креативное мышление"),
                      (self.data["competence"]["critical_thinking"], "Критическое мышление"),
                      (self.data["competence"]["literacy"], "Грамотность"),
                      (self.data["competence"]["cooperation"], "Кооперация"),
                      (self.data["competence"]["communication"], "Коммуникация"),
                      (self.data["competence"]["metacognitive_skills"], "Метакогнитивные навыки")]
        competence = [i[1] for i in competence if i[0]]

        methods = []
        session = db_session.create_session()
        for method in self.data["methods"]:
            methods.append(
                [session.query(TypeMethod).filter(
                    TypeMethod.id == method.data.id_type_method).first().name_method,
                 method.data.name_method, method.data.text, method.data.time])

        if id_current_user is None:
            teacher = " - "
        else:
            teacher = session.query(User).filter(User.id == id_current_user).first().name_user

        self.document = get_document_result_word(self.data["lesson_topic"], teacher, self.data["subject"],
                                                 self.data["class"],
                                                 self.data["lesson_duration"], competence, methods)

        self.document.save("auxiliary_file.doc")
        widget = QWidget()
        widget.setStyleSheet(".QWidget {background-color: white}")
        layout = QGridLayout()

        self.wordDocument = QAxWidget("Word.Document")
        path = os.path.join(os.path.abspath(os.curdir), "auxiliary_file.doc")
        self.wordDocument.setControl(path)
        os.remove(path)
        """pStandart = self.wordDocument.querySubObject( "CommandBars( const QVariant & )", "Standard" )
        pStandart.dynamicCall( "Enabled", True )
        pStandart.dynamicCall( "Visible", True )"""


        layout.addWidget(self.wordDocument)
        layout.setContentsMargins(5,5,5,5)
        widget.setLayout(layout)
        layout_result.addWidget(widget, 0, 2, 3, 5)

        self.setLayout(layout_result)

    def back_constructor(self):
        self.back_constructor_event.emit(
            {
                "lesson_topic": self.data["lesson_topic"],
                "subject": self.data["subject"],
                "lesson_type": self.data["lesson_type"],
                "class": self.data["class"],
                "class_characteristic": self.data["class_characteristic"],
                "lesson_duration": self.data["lesson_duration"],
                "acquaintance": self.data["acquaintance"],
                "competence": {
                    "creative_thinking": self.data["competence"]["creative_thinking"],
                    "literacy": self.data["competence"]["literacy"],
                    "communication": self.data["competence"]["communication"],
                    "cooperation": self.data["competence"]["cooperation"],
                    "critical_thinking": self.data["competence"]["critical_thinking"],
                    "metacognitive_skills": self.data["competence"]["metacognitive_skills"]
                }
            })

    def save_lesson(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранение файла", None, "Text files (*.docx *doc)")[0]
        if file_name != "":
            session = db_session.create_session()

            competence = [(self.data["competence"]["creative_thinking"], "Креативное мышление"),
                          (self.data["competence"]["critical_thinking"], "Критическое мышление"),
                          (self.data["competence"]["literacy"], "Грамотность"),
                          (self.data["competence"]["cooperation"], "Кооперация"),
                          (self.data["competence"]["communication"], "Коммуникация"),
                          (self.data["competence"]["metacognitive_skills"], "Метакогнитивные навыки")]
            competence = [i[1] for i in competence if i[0]]
            methods = [str(method.data.id) for method in self.data["methods"]]

            documents_lesson = DocumentsLesson(
                id_user=id_current_user,
                date=QDateTime.currentDateTime().toTime_t(),
                lesson_topic=self.data["lesson_topic"].lower(),
                class_lesson=self.data["class"],
                subject=self.data["subject"].lower(),
                lesson_duration=self.data["lesson_duration"],
                competence=';'.join(competence),
                ids=';'.join(methods),
            )
            session.add(documents_lesson)
            session.commit()
            self.wordDocument.dynamicCall("SaveAs(string)", file_name)
            QMessageBox.information(self, "Ок", "Урок сохранен", QMessageBox.Ok)




    def back_menu(self):
        self.back_menu_event.emit()


class MyMethodMenu(QWidget):
    back_menu_event = pyqtSignal()

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setGeometry(0, 0,
                         int(self.main_window.geometry.width()), int(self.main_window.geometry.height()))
        self.initUI()

    def initUI(self):
        layout_my_method_menu = QGridLayout()
        layout_my_method_menu.setContentsMargins(int(self.window().width() / 10.5), int(self.window().width() / 35.5),
                                                 int(self.window().width() / 10.5), int(self.window().width() / 25.5))
        # -----------------------------------------

        # -----------------------------------------
        layout_my_method_menu_head = QHBoxLayout()
        self.btn_back = QPushButton()
        self.btn_back.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        layout_my_method_menu_head.addWidget(self.btn_back)
        self.btn_back.clicked.connect(self.back)
        # -----------------------------------------
        layout_found = QHBoxLayout()

        self.line_edit_found_method = QLineEdit()
        self.line_edit_found_method.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(22)}px;"
            "}"
        )
        self.line_edit_found_method.setFixedHeight(int(self.window().width() / 30.5))
        self.line_edit_found_method.textChanged.connect(self.found)
        layout_found.addWidget(self.line_edit_found_method)

        self.btn_found = QPushButton()
        self.btn_found.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_FOUND});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_FOUND_HOVER});'
            '}'
        )
        self.btn_found.setMinimumSize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_found.setFixedWidth(self.main_window.normal.normal_proportion(75, 0)[0])
        self.btn_found.clicked.connect(self.found)
        layout_found.addWidget(self.btn_found)

        widget_found = QWidget()
        widget_found.setLayout(layout_found)
        widget_found.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )

        layout_my_method_menu_head.addWidget(widget_found)
        # -----------------------------------------
        self.btn_new_method = QPushButton("Новый метод", self)
        self.btn_new_method.setStyleSheet(
            ".QPushButton {"
            "background-color: #76b7c7;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 10px;"
            "border-color: beige;"
            f'min-height: {self.main_window.normal.normal_xy(50, 0)[0]}px;'
            f'min-width: {self.main_window.normal.normal_xy(200, 0)[0]}px;'
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "min-width: 10em;"
            "padding: 6px;"
            "}"
            ".QPushButton:hover {"
            "background-color: #548490;"
            "border-style: inset;"
            "}"
        )
        layout_my_method_menu_head.addWidget(self.btn_new_method)
        self.btn_new_method.clicked.connect(self.create_new_method)

        widget_my_method_menu_head = QWidget()
        widget_my_method_menu_head.setLayout(layout_my_method_menu_head)
        widget_my_method_menu_head.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )

        layout_my_method_menu.addWidget(widget_my_method_menu_head, 0, 0)
        # -----------------------------------------

        # -----------------------------------------

        self.scroll_my_method_menu = QScrollArea(self)
        self.scroll_my_method_menu.setStyleSheet(
            ".QScrollArea {"
            "background-color:transparent;"
            "}"
        )
        self.scroll_my_method_menu.setFrameShape(QFrame.NoFrame)
        self.scroll_my_method_menu.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_my_method_menu.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout_my_method_menu.addWidget(self.scroll_my_method_menu, 1, 0)

        self.setLayout(layout_my_method_menu)
        session = db_session.create_session()
        self.filter_my_method_menu = session.query(Methods).filter(Methods.id_user.like(id_current_user)).all()
        self.show_methods_stage()

    def show_methods_stage(self):
        object_methods = []

        layout = QVBoxLayout()
        for i in range(len(self.filter_my_method_menu)):
            object_methods.append(MyMethod(self, self.filter_my_method_menu[i]))
            layout.addWidget(object_methods[i])

        self.widget_list_methods = QWidget(self)
        self.widget_list_methods.setGeometry(0, 0, int(self.window().width() / 1.25),
                                             116 * len(self.filter_my_method_menu))
        self.widget_list_methods.setLayout(layout)
        self.widget_list_methods.setStyleSheet(
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        self.scroll_my_method_menu.setWidget(self.widget_list_methods)
        self.scroll_my_method_menu.show()

    def create_new_method(self):
        self.setDisabled(True)
        self.new_method = NewMethod(self)
        if self.new_method.exec_() == QDialog.Accepted:
            session = db_session.create_session()
            session.add(self.new_method.data)
            session.commit()
            self.filter_my_method_menu = session.query(Methods).filter(Methods.id_user.like(id_current_user)).all()
            self.show_methods_stage()
        self.setDisabled(False)

    def back(self):
        self.back_menu_event.emit()

    def found(self):
        session = db_session.create_session()
        self.filter_my_method_menu = session.query(Methods).filter(
            Methods.id_user == id_current_user,
            (Methods.name_method.like(f"%{self.line_edit_found_method.text().lower()}%") |
             Methods.text.like(f"%{self.line_edit_found_method.text().lower()}%"))).all()
        self.show_methods_stage()


class MyMethod(QWidget):
    def __init__(self, main_window, data):
        super(MyMethod, self).__init__(main_window.main_window)
        self.main_window = main_window
        self.data = data
        self.initUI()

    def initUI(self):
        self.background = QLabel(self)
        self.background.setStyleSheet(
            '.QLabel {'
            f'min-height: {100}px;'
            f'min-width: {int(self.main_window.window().width() / 1.29)}px;'
            'margin-bottom: 16px;'
            'background-color: #FFA25F;'
            'border-radius: 14px'
            '}'
        )
        layout = QHBoxLayout(self)

        self.label_lesson_topic = QLabel(self.data.name_method[0].upper() + self.data.name_method[1:].lower(), self)
        self.label_lesson_topic.setWordWrap(True)
        self.label_lesson_topic.setStyleSheet(
            ".QLabel {"
            f"margin-left: {int(self.main_window.window().width() / 25.5)};"
            f"font: bold {self.main_window.main_window.normal.normal_font(24)}px;"
            "}"
        )
        layout.addWidget(self.label_lesson_topic)

        self.btn_edit = QPushButton(self)
        self.btn_edit.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_EDIT});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_EDIT_HOVER});'
            '}'
        )
        self.btn_edit.setMinimumSize(*self.main_window.main_window.normal.normal_proportion(175, 60))
        self.btn_edit.setFixedWidth(self.main_window.main_window.normal.normal_proportion(175, 0)[0])
        layout.addWidget(self.btn_edit)

        self.btn_del = QPushButton(self)
        self.btn_del.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_DEL});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_DEL_HOVER});'
            '}'
        )
        self.btn_del.setMinimumSize(*self.main_window.main_window.normal.normal_proportion(40, 40))
        self.btn_del.setFixedWidth(self.main_window.main_window.normal.normal_proportion(40, 0)[0])
        layout.addWidget(self.btn_del)

        self.btn_del.clicked.connect(self.del_method)
        self.btn_edit.clicked.connect(self.edit)

    def del_method(self):
        session = db_session.create_session()
        method = session.query(Methods).filter(Methods.id == self.data.id).first()
        session.delete(method)
        session.commit()
        self.main_window.filter_my_method_menu = session.query(Methods).filter(
            Methods.id_user.like(id_current_user)).all()
        self.main_window.show_methods_stage()

    def edit(self):
        self.main_window.setDisabled(True)
        data = {
            "name_method": self.data.name_method[0].upper() + self.data.name_method[1:].lower(),
            "time": int(self.data.time),
            "id_classes_number": self.data.id_classes_number,
            "id_type_method": self.data.id_type_method,
            "id_stage_method": self.data.id_stage_method,
            "id_fgos": self.data.id_fgos,
            "competence": {
                "communication": self.data.communication,
                "literacy": self.data.literacy,
                "cooperation": self.data.cooperation,
                "creative_thinking": self.data.creative_thinking,
                "critical_thinking": self.data.critical_thinking,
                "metacognitive_skills": self.data.metacognitive_skills,

            },
            "is_local": self.data.is_local,
            "text": self.data.text,
        }
        self.new_method = NewMethod(self.main_window, data)
        if self.new_method.exec_() == QDialog.Accepted:
            session = db_session.create_session()
            method = session.query(Methods).filter(Methods.id == self.data.id).first()
            session.delete(method)
            session.add(self.new_method.data)
            session.commit()
            self.main_window.filter_my_method_menu = session.query(Methods).filter(
                Methods.id_user.like(id_current_user)).all()
            self.main_window.show_methods_stage()
        self.main_window.setDisabled(False)


class NewMethod(QDialog):
    def __init__(self, main_window, data=None):
        QDialog.__init__(self)
        self.main_window = main_window.main_window
        if data is None:
            data = {}
        if not data:
            data = {
                "name_method": "",
                "time": 0,
                "id_classes_number": 1,
                "id_type_method": 1,
                "id_stage_method": 1,
                "id_fgos": 1,
                "competence": {
                    "communication": False,
                    "literacy": False,
                    "cooperation": False,
                    "creative_thinking": False,
                    "critical_thinking": False,
                    "metacognitive_skills": False,

                },
                "is_local": True,
                "text": "",
            }
        self.data = data
        self.setParent(self.main_window)
        self.setGeometry(int(self.main_window.geometry.width() / 6), int(self.main_window.geometry.height() / 6),
                         int(self.main_window.geometry.width() / 1.5), int(self.main_window.geometry.height() / 1.5))
        self.initUI()

    def initUI(self):
        session = db_session.create_session()

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
        self.text_local = QLabel("Разместить локально")
        self.text_local.setStyleSheet(
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
        self.edit_method_topic = QLineEdit(self.data["name_method"])
        self.edit_method_topic.setStyleSheet(
            ".QLineEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.edit_method_duration = QSpinBox()
        self.edit_method_duration.setValue(self.data["time"])
        self.edit_method_duration.setStyleSheet(
            ".QSpinBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.combo_class_method = QComboBox()
        self.combo_class_method.setCurrentIndex(self.data["id_classes_number"])
        self.combo_class_method.addItems([item.name_class for item in session.query(Classes).all()])
        self.combo_class_method.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_method_type = QComboBox()
        self.combo_method_type.setCurrentIndex(self.data["id_type_method"])
        self.combo_method_type.addItems([item.name_method for item in session.query(TypeMethod).all()])
        self.combo_method_type.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_stage_method = QComboBox()
        self.combo_stage_method.setCurrentIndex(self.data["id_stage_method"])
        self.combo_stage_method.addItems([item.name_stage for item in session.query(Stage).all()])
        self.combo_stage_method.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.combo_fgos_method = QComboBox()
        self.combo_fgos_method.setCurrentIndex(self.data["id_fgos"])
        self.combo_fgos_method.addItems([item.name_fgos for item in session.query(Fgos).all()])
        self.combo_fgos_method.setStyleSheet(
            ".QComboBox {"
            f"font: {self.main_window.normal.normal_font(18)}px;"
            "background-color: white;"
            "}"
        )
        # -----------------------------------------
        self.check_communication = QCheckBox('Коммуникация')
        self.check_communication.setChecked(self.data["competence"]["communication"])
        self.check_communication.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_literacy = QCheckBox('Грамотность')
        self.check_literacy.setChecked(self.data["competence"]["literacy"])
        self.check_literacy.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_cooperation = QCheckBox('Кооперация')
        self.check_cooperation.setChecked(self.data["competence"]["cooperation"])
        self.check_cooperation.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_creative_thinking = QCheckBox('Креативное мышление')
        self.check_creative_thinking.setChecked(self.data["competence"]["creative_thinking"])
        self.check_creative_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_critical_thinking = QCheckBox('Критическое мышление')
        self.check_critical_thinking.setChecked(self.data["competence"]["critical_thinking"])
        self.check_critical_thinking.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.check_metacognitive_skills = QCheckBox('Метакогнитивные навыки')
        self.check_metacognitive_skills.setChecked(self.data["competence"]["metacognitive_skills"])
        self.check_metacognitive_skills.setStyleSheet(
            ".QCheckBox {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        # -----------------------------------------
        self.radio_btn_local_yes = QRadioButton('Да')
        self.radio_btn_local_yes.setStyleSheet(
            ".QRadioButton {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        self.radio_btn_local_no = QRadioButton('Нет')
        self.radio_btn_local_no.setStyleSheet(
            ".QRadioButton {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )
        self.radio_btn_local_no.setChecked(self.data["is_local"])
        self.radio_btn_local_yes.setChecked(not self.data["is_local"])
        self.btn_radio_group = QButtonGroup()
        self.btn_radio_group.addButton(self.radio_btn_local_yes)
        self.btn_radio_group.addButton(self.radio_btn_local_no)
        # -----------------------------------------
        self.text_method = QTextEdit()
        self.text_method.setText(self.data["text"])
        self.text_method.setStyleSheet(
            ".QTextEdit {"
            f"font: bold {self.main_window.normal.normal_font(18)}px;"
            "}"
        )

        # -----------------------------------------
        self.btn_back = QPushButton(self)
        self.btn_back.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_BACK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_BACK_HOVER});'
            '}'
        )
        self.btn_back.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_back.move(15, 5)
        self.btn_back.clicked.connect(self.back_menu)
        # -----------------------------------------
        self.btn_ok = QPushButton(self)
        self.btn_ok.setStyleSheet(
            '.QPushButton {'
            f'border-image: url({PATH_BUTTON_OK});'
            '}'
            '.QPushButton:hover {'
            f'border-image: url({PATH_BUTTON_OK_HOVER});'
            '}'
        )
        self.btn_ok.resize(*self.main_window.normal.normal_proportion(75, 75))
        self.btn_ok.move(self.geometry().width() - self.main_window.normal.normal_proportion(75, 0)[0] - 12, 5)
        self.btn_ok.clicked.connect(self.valid_options_new_method)
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
            ".QWidget {"
            "background-color:transparent;"
            "}"
        )
        layout_new_method.addWidget(widget_competence, 6, 1)

        layout_new_method.addWidget(self.text_local, 7, 0)
        layout_local = QGridLayout()
        layout_local.addWidget(self.radio_btn_local_yes, 1, 0)
        layout_local.addWidget(self.radio_btn_local_no, 1, 1)
        layout_new_method.addLayout(layout_local, 7, 1)

        layout_new_method.addWidget(self.text_method_text, 8, 0)
        layout_new_method.addWidget(self.text_method, 8, 1)

        self.setLayout(layout_new_method)

    def back_menu(self):
        self.reject()

    def valid_options_new_method(self):
        if self.edit_method_topic.text() != "" and self.text_method.toPlainText() != "":
            session = db_session.create_session()
            self.data = Methods(
                name_method=self.edit_method_topic.text().lower(),
                time=self.edit_method_duration.value(),
                id_user=id_current_user,
                id_classes_number=session.query(Classes).filter(
                    Classes.name_class == self.combo_class_method.currentText()).first().id,
                id_type_method=session.query(TypeMethod).filter(
                    TypeMethod.name_method == self.combo_method_type.currentText()).first().id,
                id_stage_method=session.query(Stage).filter(
                    Stage.name_stage == self.combo_stage_method.currentText()).first().id,
                creative_thinking=self.check_creative_thinking.isChecked(),
                critical_thinking=self.check_critical_thinking.isChecked(),
                communication=self.check_communication.isChecked(),
                cooperation=self.check_cooperation.isChecked(),
                metacognitive_skills=self.check_metacognitive_skills.isChecked(),
                literacy=self.check_literacy.isChecked(),
                is_local=self.radio_btn_local_yes.isChecked(),
                id_fgos=session.query(Fgos).filter(Fgos.name_fgos == self.combo_fgos_method.currentText()).first().id,
                text=self.text_method.toPlainText(),
            )
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "Вы заполнили не все поля", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
