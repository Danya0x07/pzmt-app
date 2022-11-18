from enum import IntEnum

from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice


class SerialPort:
    """Адаптер для класса последовательного порта из используемой библиотеки."""

    class ErrorStatus(IntEnum):
        """Возможные ошибки последовательного порта"""
        OK = 0
        DECODING_ERROR = 1
        ENCODING_ERROR = 2
        WRITING_ERROR = 3
        NO_PACKET = 4

    def __init__(self, app):
        self.app = app
        self.port = QSerialPort()
        self.port.setBaudRate(9600)
        self.port.readyRead.connect(self.__on_byte_recv_callback)

    def open(self, port_name):
        self.port.setPortName(port_name)
        return self.port.open(QIODevice.ReadWrite)

    def is_open(self):
        return self.port.isOpen()

    def close(self):
        self.port.close()

    def __packet_ready(self):
        return self.port.canReadLine()

    def __on_byte_recv_callback(self):
        if self.__packet_ready():
            self.app.process_packet()

    def read(self):
        status = SerialPort.ErrorStatus.NO_PACKET
        reply = '\n'

        if self.__packet_ready():
            raw_reply = self.port.readLine()
            try:
                reply = str(raw_reply, 'ascii')
            except UnicodeDecodeError:
                reply = '\n'
                status = SerialPort.ErrorStatus.DECODING_ERROR
            else:
                status = SerialPort.ErrorStatus.OK

        return status, reply

    def write(self, data: str):
        status = SerialPort.ErrorStatus.OK
        try:
            data = data.encode('ascii')
        except UnicodeEncodeError:
            status = SerialPort.ErrorStatus.ENCODING_ERROR
        else:
            if self.port.write(data) == -1:
                status = SerialPort.ErrorStatus.WRITING_ERROR
        return status

    @staticmethod
    def get_available_ports():
        return [p.portName() for p in QSerialPortInfo().availablePorts()]
