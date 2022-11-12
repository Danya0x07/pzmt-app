from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class ViewController(QMainWindow):
    """Класс визуального представления приложения.
    Предназначен для взаимодействия с пользователем и с Qt.
    """

    def __init__(self, app):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.app = app
        self.connect_signals()
        self.show()

    def connect_signals(self):
        pass