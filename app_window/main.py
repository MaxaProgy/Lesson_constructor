# -*- coding: utf-8 -*-

import sys
import time

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplashScreen, QDesktopWidget

from const import *


class Normalize:
    def __init__(self, width, height):
        self.init_width = 1920
        self.init_height = 1080

        self.window_width_now = width
        self.window_height_now = height

    def normal_xy(self, x, y):
        return int(self.window_width_now / self.init_width * x), int(self.window_height_now / self.init_height * y)

    def normal_prop_xy(self, x, y):
        return int(self.window_width_now / self.init_width * x), int(self.window_width_now / self.init_width * y)

    def normal_font(self, font):
        return str(int(self.window_width_now / self.init_width * font))


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

        self.initUI()

    def initUI(self):
        # Заставка
        splash = QSplashScreen(QtGui.QPixmap(PATH_SPLASH_SCREEN).scaled(*self.normal.normal_prop_xy(1544, 900)),
                               QtCore.Qt.WindowStaysOnTopHint)
        splash.show()
        time.sleep(1)
        splash.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()

    main_window.show()
    sys.exit(app.exec_())
