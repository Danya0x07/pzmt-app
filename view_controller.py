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
        self.lcdOutHz.display(0)
        self.show()

    def connect_signals(self):
        self.rdInputHz.clicked.connect(self.__rdInputHzClicked)
        self.rdInputNotes.clicked.connect(self.__rdInputNotesClicked)

        self.btnConnect.clicked.connect(self.__btnConnectClicked)
        self.btnPlayFrequency.clicked.connect(self.__btnPlayFrequencyClicked)
        self.btnNoSound.clicked.connect(self.__btnNoSoundClicked)
        self.btnPlayMelody.clicked.connect(self.__btnPlayMelodyClicked)
        self.btnClearTxt.clicked.connect(self.__btnClearTxtClicked)
        self.btnRecordKeys.clicked.connect(self.__btnRecordKeysClicked)
        self.btnVolumeSwitch.clicked.connect(self.__btnVolumeSwitchClicked)

        self.chbEnableKeyboard.stateChanged.connect(self.__chbEnableKeyboardStateChanged)

        self.actOpenFile.triggered.connect(self.__actOpenFileTriggered)
        self.actSaveFile.triggered.connect(self.__actSaveFileTriggered)
        self.actShowAbout.triggered.connect(self.__actShowAboutTriggered)

    def __rdInputHzClicked(self):
        print("__rdInputHzClicked")

    def __rdInputNotesClicked(self):
        print("__rdInputNotesClicked")

    def __btnConnectClicked(self):
        print("__btnConnectClicked")

    def __btnPlayFrequencyClicked(self):
        print("__btnPlayFrequencyClicked")

    def __btnNoSoundClicked(self):
        print("__btnNoSoundClicked")

    def __btnPlayMelodyClicked(self):
        print("__btnPlayMelodyClicked")

    def __btnClearTxtClicked(self):
        print("__btnClearTxtClicked")

    def __btnRecordKeysClicked(self):
        print("__btnRecordKeysClicked")

    def __btnVolumeSwitchClicked(self):
        print("__btnVolumeSwitchClicked")

    def __chbEnableKeyboardStateChanged(self):
        print("__chbEnableKeyboardStateChanged")

    def __actOpenFileTriggered(self):
        print("__actOpenFileTriggered")

    def __actSaveFileTriggered(self):
        print("__actSaveFileTriggered")

    def __actShowAboutTriggered(self):
        print("__actShowAboutTriggered")
