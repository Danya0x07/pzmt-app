from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class ViewController(QMainWindow):
    """Класс визуального представления приложения.
    Предназначен для взаимодействия с пользователем и с Qt.
    """
    KEYBOARD = {Qt.Key_A: 'C', Qt.Key_W: 'C#', Qt.Key_S: 'D', Qt.Key_E: 'D#', Qt.Key_D: 'E',
                Qt.Key_F: 'F', Qt.Key_T: 'F#', Qt.Key_Space: '_',
                Qt.Key_J: 'G', Qt.Key_I: 'G#', Qt.Key_K: 'A', Qt.Key_O: 'A#', Qt.Key_L: 'B'}
    _NOTE_LBL_STYLE = 'color: rgb(255, 0, 255);'
    _NOTE_SHARP_LBL_STYLE = 'color: rgb(255, 0, 127);'

    def __init__(self, app):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.app = app
        self.__keys_stack = []
        self.__record_enabled = False
        self.NOTE_LABELS = {
            'C': self.lblNoteC, 'C#': self.lblNoteCs, 'D': self.lblNoteD, 'D#': self.lblNoteDs,
            'E': self.lblNoteE, 'F': self.lblNoteF, 'F#': self.lblNoteFs,
            'G': self.lblNoteG, 'G#': self.lblNoteGs, 'A': self.lblNoteA, 'A#': self.lblNoteAs,
            'B': self.lblNoteB
        }
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
        if not self.chbEnableKeyboard.checkState():
            self.set_status_msg('Клавиатура не включена')
            return

        self.__record_enabled = not self.__record_enabled
        if self.__record_enabled:
            self.btnRecordKeys.setText('Стоп')
            self.btnRecordKeys.setIcon(QIcon('assets/stopRec.ico'))
        else:
            self.btnRecordKeys.setText('Запись')
            self.btnRecordKeys.setIcon(QIcon('assets/rec.ico'))
        self.setFocus()

    def __btnVolumeSwitchClicked(self):
        print("__btnVolumeSwitchClicked")

    def __chbEnableKeyboardStateChanged(self):
        self.__record_enabled = False
        self.btnRecordKeys.setText('Запись')
        self.btnRecordKeys.setIcon(QIcon('assets/rec.ico'))
        self.setFocus()

    def __actOpenFileTriggered(self):
        print("__actOpenFileTriggered")

    def __actSaveFileTriggered(self):
        print("__actSaveFileTriggered")

    def __actShowAboutTriggered(self):
        print("__actShowAboutTriggered")

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        key = event.key()
        if not event.isAutoRepeat() and self.chbEnableKeyboard.checkState():
            if key in ViewController.KEYBOARD:
                note = ViewController.KEYBOARD[key]
                lbl = self.NOTE_LABELS.get(note, None)
                note = str(self.spbOctave.value()) * (key != Qt.Key_Space) + note
                self.app.play_note(note)
                self.__keys_stack.append(key)
                if self.__record_enabled:
                    self.app.record(note, self.rdInputHz.isChecked())
                if '#' in note:
                    lbl.setStyleSheet(self._NOTE_SHARP_LBL_STYLE + 'font-weight: bold')
                else:
                    lbl.setStyleSheet(self._NOTE_LBL_STYLE + 'font-weight: bold')
            elif key == Qt.Key_G:
                self.spbOctave.setValue(self.spbOctave.value() - 1)
            elif key == Qt.Key_H:
                self.spbOctave.setValue(self.spbOctave.value() + 1)
            elif key == Qt.Key_Backspace and self.__record_enabled:
                self.app.remove_last_recorded()

    def keyReleaseEvent(self, event):
        super().keyPressEvent(event)
        key = event.key()
        if not event.isAutoRepeat() and self.chbEnableKeyboard.checkState() and key in ViewController.KEYBOARD:
            if self.__keys_stack:
                self.__keys_stack.pop()
                note = ViewController.KEYBOARD[key]
                lbl = self.NOTE_LABELS.get(note, None)
                lbl.setStyleSheet(self._NOTE_SHARP_LBL_STYLE if '#' in note else self._NOTE_LBL_STYLE)
                if len(self.__keys_stack) == 0:
                    self.app.stop_playing()

    def set_status_msg(self, msg):
        self.statusBar().showMessage(msg, 1500)

    def set_available_ports_list(self, port_names):
        self.cbbSerialPortName.clear()
        self.cbbSerialPortName.addItems(port_names)

    def set_current_frequency(self, frequency):
        self.lcdOutHz.display(frequency)

    def set_raw_frequencies(self, txt):
        self.txtFrequencies.setPlainText(txt)

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
