import sys

from PyQt5.QtWidgets import QApplication

from app import App

print('На сообщения вида QTextCursor::setPosition: Position X out of range\n'
      'не обращаем внимание - это баг Qt')
qApp = QApplication([])
app = App()

sys.exit(qApp.exec())