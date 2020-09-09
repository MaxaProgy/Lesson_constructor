from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QSplashScreen, QPushButton
from PyQt5 import uic
from .main import Menu


class NewLesson(QMainWindow):
    def __init__(self):
        super().__init__(self, Menu)
        uic.loadUi('data/ui_file/ui_new_lesson.ui', self)

    def a(self):
        pass