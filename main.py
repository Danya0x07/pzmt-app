import sys

from PyQt5.QtWidgets import QApplication

from view_controller import ViewController

qApp = QApplication([])
vc = ViewController(None)
sys.exit(qApp.exec())