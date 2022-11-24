from view_controller import ViewController
from serial_port import SerialPort
import parser
import protocol
from protocol import CommandType, ReplyCode


class App:
    """Посредник для компонентов программы."""
    def __init__(self):
        self.vc = ViewController(self)
        self.serial = SerialPort(self)
        self.reset_melody()

    def update_available_ports(self):
        self.vc.set_available_ports_list(SerialPort.get_available_ports())

    def serial_connect(self):
        port_name = self.vc.get_selected_port_name()
        if not port_name:
            self.vc.set_status_msg("Ну порт же надо выбрать сначала...")
            return

        if self.serial.open(port_name):
            self.vc.set_status_msg("Соединение установлено")
        else:
            self.vc.set_status_msg("Ой, порт {} не открывается!".format(port_name))

    def serial_disconnect(self):
        self.serial.close()
        self.vc.set_status_msg("Соединение закрыто")

    def connection_established(self):
        return self.serial.is_open()

    def reset_melody(self):
        self.__melody = zip()
        self.__playing = False

    def process_packet(self):
        status, reply = self.serial.read()
        if status == SerialPort.ErrorStatus.OK:
            reply_code = protocol.parse_reply(reply)
            if reply_code == ReplyCode.WRONG_CMD:
                self.vc.set_status_msg("Пьезоколонка нас не понимает")
                self.reset_melody()
            elif reply_code == ReplyCode.OK:
                pass
            elif reply_code == ReplyCode.READY:
                if self.__playing:
                    try:
                        success, command = protocol.build_command(CommandType.PLAY_FINITE_TONE, next(self.__melody))
                        if success:
                            self.serial.write(command)
                        else:
                            self.vc.set_status_msg("Привет, меня зовут БАГ#2!")
                    except StopIteration:
                        self.__playing = False
            elif reply_code == ReplyCode.BUSY:
                self.vc.set_status_msg("Пьезоколонка подавилась, сворачиваем тусу")
                self.reset_melody()
            else:  # UNRECOGNIZABLE или приветственное сообщение
                self.vc.set_status_msg("Пьезоколонка что-то говорит")
                print(reply)
                self.reset_melody()
        elif status == SerialPort.ErrorStatus.DECODING_ERROR:
            self.vc.set_status_msg("Пьезоколонку штырит походу")
            self.reset_melody()
        else:  # NO_PACKET
            self.vc.set_status_msg("Пьезоколонка недоговаривает")
            self.reset_melody()

    def play_frequency(self):
        frequency = self.vc.get_frequency()
        if self.connection_established():
            if parser.valid_frequency(frequency):
                self.reset_melody()
                success, cmd = protocol.build_command(CommandType.PLAY_INFINITE_TONE, frequency)
                if success:
                    self.serial.write(cmd)
                else:
                    self.vc.set_status_msg("Привет, меня зовут БАГ#1!")
            else:
                self.vc.set_status_msg("Введённая частота не поддерживается")
        else:
            self.vc.set_status_msg("Куда слать то? Порт закрыт...")

    def play_frequencies(self):
        if not self.connection_established():
            self.vc.set_status_msg("Куда слать то? Порт закрыт...")
            return

        frequencies = []
        durations = []

        raw_frequencies = self.vc.get_raw_frequencies()
        raw_frequencies = parser.split_sequence(raw_frequencies)
        for f in raw_frequencies:
            success, frequency = parser.parse_frequency(f)
            if not success or not parser.valid_frequency(frequency):
                self.vc.set_status_msg("Не похоже на частоту: {}".format(f[:8]))
                return
            frequencies.append(frequency)

        raw_durations = self.vc.get_raw_durations()
        raw_durations = parser.split_sequence(raw_durations)
        for f in raw_durations:
            success, duration = parser.parse_duration(f)
            if not success or not parser.valid_duration(duration):
                self.vc.set_status_msg("Не похоже на длительность: {}".format(f[:8]))
                return
            durations.append(duration)

        lf, ld = len(frequencies), len(durations)
        if lf != ld:
            self.vc.set_status_msg("Частот и длительностей должно быть поровну, а не {} и {}.".format(lf, ld))
            return
        if lf == 0:
            self.vc.set_status_msg("Классная мелодия! Даже играть не надо")
            return

        self.__melody = zip(frequencies, durations)
        success, command = protocol.build_command(CommandType.PLAY_FINITE_TONE, next(self.__melody))
        if success:
            self.__playing = True
            self.serial.write(command)

