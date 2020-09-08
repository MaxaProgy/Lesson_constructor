import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QSplashScreen
from PyQt5 import uic, QtGui, QtCore
import time


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.geometry = QDesktopWidget().availableGeometry()
        self.splash_screen()

    def splash_screen(self):
        self.setMinimumHeight(self.geometry.height() - 150)
        self.setMinimumWidth(self.geometry.width() - 150)
        self.setStyleSheet('.QWidget {background-image: url(image/фоны/меню.jpg);}')


app = QApplication(sys.argv)
ex = MyWidget()
splash = QSplashScreen(QtGui.QPixmap('image/фоны/заставка.png'), QtCore.Qt.WindowStaysOnTopHint)
splash.show()
time.sleep(3)
splash.close()

ex.show()
sys.exit(app.exec_())


