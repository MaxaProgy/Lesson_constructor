import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QSplashScreen, QPushButton
from PyQt5 import uic, QtGui, QtCore
import time


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.geometry = QDesktopWidget().availableGeometry()

        # Кнопка создания нового урока
        btn_new_lesson = QPushButton("Новый урок", self)
        btn_new_lesson.resize(200, 50)
        btn_new_lesson.move(175, 200)
        # 548490 - темный голубой  76b7c7 - светлый голубой
        btn_new_lesson.setStyleSheet('''
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

        self.splash_screen()

    def splash_screen(self):
        self.setMinimumHeight(self.geometry.height() - 150)
        self.setMinimumWidth(self.geometry.width() - 150)
        self.setStyleSheet('.QWidget {background-image: url(image/фоны/меню.jpg);}')


app = QApplication(sys.argv)
ex = Menu()

# Заставка
splash = QSplashScreen(QtGui.QPixmap('image/фоны/заставка.png'), QtCore.Qt.WindowStaysOnTopHint)
splash.show()
time.sleep(1)
splash.close()

ex.show()
sys.exit(app.exec_())
