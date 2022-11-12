import sys

from PyQt5.QtWidgets import QApplication

from view_controller import ViewController

print('На сообщения вида QTextCursor::setPosition: Position X out of range\n'
      'не обращаем внимание - это баг Qt')
qApp = QApplication([])
vc = ViewController(None)
sys.exit(qApp.exec())