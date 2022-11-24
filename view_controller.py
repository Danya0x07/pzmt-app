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
        self.lnBeatMs.setEnabled(False)
        self.show()

    def connect_signals(self):
        self.rdInputHz.clicked.connect(self.__rdInputHzClicked)
        self.rdInputNotes.clicked.connect(self.__rdInputNotesClicked)

        self.btnConnect.clicked.connect(self.__btnConnectClicked)
        self.btnPlayFrequency.clicked.connect(self.__btnPlayFrequencyClicked)
        self.btnNoSound.clicked.connect(self.__btnNoSoundClicked)
        self.btnPlayMelody.clicked.connect(self.__btnPlayMelodyClicked)
        self.btnRecordKeys.clicked.connect(self.__btnRecordKeysClicked)
        self.btnVolumeSwitch.clicked.connect(self.__btnVolumeSwitchClicked)
        self.btnRefreshPorts.clicked.connect(self.__btnRefreshPortsClicked)

        self.chbEnableKeyboard.stateChanged.connect(self.__chbEnableKeyboardStateChanged)

        self.actOpenFile.triggered.connect(self.__actOpenFileTriggered)
        self.actSaveFile.triggered.connect(self.__actSaveFileTriggered)
        self.actShowAbout.triggered.connect(self.__actShowAboutTriggered)

    def __rdInputHzClicked(self):
        self.lnBeatMs.setEnabled(False)
        self.lblTopTxtMeaning.setText("Частоты:")
        self.lblBottomTxtMeaning.setText("Длительности:")

    def __rdInputNotesClicked(self):
        self.lnBeatMs.setEnabled(True)
        self.lblTopTxtMeaning.setText("Ноты:")
        self.lblBottomTxtMeaning.setText("Интервалы:")

    def __btnRefreshPortsClicked(self):
        self.app.update_available_ports()

    def __btnConnectClicked(self):
        # Если соединение уже открыто, закрываем его, иначе открываем.
        if self.app.connection_established():
            self.app.serial_disconnect()
            self.btnConnect.setText("Подключить")
        else:
            self.app.serial_connect()
            if self.app.connection_established():
                self.btnConnect.setText("Отключить")

    def __btnPlayFrequencyClicked(self):
        self.app.play_frequency()

    def __btnNoSoundClicked(self):
        self.app.stop_playing()

    def __btnPlayMelodyClicked(self):
        if self.rdInputNotes.isChecked():
            self.app.play_notes()
        else:
            self.app.play_frequencies()

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

    def set_status_msg(self, msg):
        self.statusBar().showMessage(msg)

    def set_available_ports_list(self, port_names):
        self.cbbSerialPortName.clear()
        self.cbbSerialPortName.addItems(port_names)

    def get_selected_port_name(self):
        return self.cbbSerialPortName.currentText()

    def get_frequency(self):
        txt_frequency = self.lnFrequency.text()
        return int(txt_frequency) if txt_frequency.isnumeric() else 0

    def get_raw_frequencies(self):
        return self.txtFrequencies.toPlainText()

    def get_raw_durations(self):
        return self.txtDurations.toPlainText()

    def get_beat(self):
        txt_beat = self.lnBeatMs.text()
        return int(txt_beat) if txt_beat.isnumeric() else 0
