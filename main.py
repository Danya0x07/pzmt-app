# Copyright (C) 2022 Danya0x07 & dmPetrov
#     The "MeanderSounds" project group.
#
# This software is a part of PiezoMaestro project.
#

import sys

from PyQt5.QtWidgets import QApplication

from app import App

print('На сообщения вида QTextCursor::setPosition: Position X out of range\n'
      'не обращаем внимание - это баг Qt')
qApp = QApplication([])
app = App()

sys.exit(qApp.exec())