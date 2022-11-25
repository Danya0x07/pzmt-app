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
        self.__ready_for_next_frequency = True

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
        self.__last_frequency_played = 0

    def process_packet(self):
        status, reply = self.serial.read()
        if status == SerialPort.ErrorStatus.OK:
            reply_code = protocol.parse_reply(reply)
            if reply_code == ReplyCode.WRONG_CMD:
                self.vc.set_status_msg("Пьезоколонка нас не понимает")
                self.reset_melody()
            elif reply_code == ReplyCode.OK:
                self.__ready_for_next_frequency = True
            elif reply_code == ReplyCode.READY:
                if self.__playing:
                    try:
                        frequency, duration = next(self.__melody)
                        success, command = protocol.build_command(CommandType.PLAY_FINITE_TONE, (frequency, duration))
                        if success:
                            self.serial.write(command)
                            self.vc.set_current_frequency(self.__last_frequency_played)
                            self.__last_frequency_played = frequency
                        else:
                            self.vc.set_status_msg("Привет, меня зовут БАГ#2!")
                    except StopIteration:
                        self.vc.set_current_frequency(self.__last_frequency_played)
                        self.reset_melody()
            elif reply_code == ReplyCode.BUSY:
                self.vc.set_status_msg("Пьезоколонка подавилась, сворачиваем тусу")
                self.reset_melody()
            else:  # UNRECOGNIZABLE или приветственное сообщение
                self.vc.set_status_msg("Пьезоколонка что-то говорит")
                print(reply, end='')
                self.reset_melody()
        elif status == SerialPort.ErrorStatus.DECODING_ERROR:
            self.vc.set_status_msg("Пьезоколонку штырит походу")
            self.reset_melody()
        else:  # NO_PACKET
            self.vc.set_status_msg("Пьезоколонка недоговаривает")
            self.reset_melody()

    def play_frequency(self, frequency=None):
        if frequency is None:
            frequency = self.vc.get_frequency()
        if self.connection_established():
            if parser.valid_frequency(frequency):
                self.reset_melody()
                success, cmd = protocol.build_command(CommandType.PLAY_INFINITE_TONE, frequency)
                if success:
                    if self.__ready_for_next_frequency:
                        self.serial.write(cmd)
                        self.vc.set_current_frequency(frequency)
                        self.__ready_for_next_frequency = False
                    else:
                        self.vc.set_status_msg("Уоуоуоуоу! Полегче! Она не может так быстро принимать!")
                else:
                    self.vc.set_status_msg("Привет, меня зовут БАГ#1!")
            else:
                self.vc.set_status_msg("Введённая частота не поддерживается")
        else:
            self.vc.set_status_msg("Куда слать то? Порт закрыт...")

    def play_frequencies(self):
        frequencies = []
        durations = []

        raw_frequencies = self.vc.get_raw_frequencies()
        raw_frequencies = parser.split_sequence(raw_frequencies)
        for f in raw_frequencies:
            success, frequency = parser.parse_frequency(f)
            if success and parser.valid_frequency(frequency):
                frequencies.append(frequency)
            else:
                self.vc.set_status_msg("Не похоже на частоту: {}".format(f[:8]))
                return

        raw_durations = self.vc.get_raw_durations()
        raw_durations = parser.split_sequence(raw_durations)
        for f in raw_durations:
            success, duration = parser.parse_duration(f)
            if success and parser.valid_duration(duration):
                durations.append(duration)
            else:
                self.vc.set_status_msg("Не похоже на длительность: {}".format(f[:8]))
                return
        self.start_playing(frequencies, durations)

    def play_note(self, note):
        frequency = parser.note_to_frequency(note)
        self.play_frequency(frequency)

    def play_notes(self):
        frequencies = []
        durations = []

        raw_notes = self.vc.get_raw_frequencies()
        raw_notes = parser.split_sequence(raw_notes)
        for n in raw_notes:
            if parser.valid_note(n):
                frequencies.append(parser.note_to_frequency(n))
            else:
                self.vc.set_status_msg("Не похоже на допустимую ноту: {}".format(n[:8]))
                return

        beat_duration = self.vc.get_beat()
        if beat_duration == 0 or beat_duration > 20000:
            self.vc.set_status_msg("Необходимо указать допустимую длительность такта")
            return

        raw_intervals = self.vc.get_raw_durations()
        raw_intervals = parser.split_sequence(raw_intervals)
        for i in raw_intervals:
            success, interval = parser.parse_duration(i)
            if success and parser.valid_interval(interval):
                durations.append(beat_duration // interval)
            else:
                self.vc.set_status_msg("Не похоже на длительность: {}".format(i[:8]))
                return
        self.start_playing(frequencies, durations)

    def start_playing(self, frequencies, durations):
        if not self.connection_established():
            self.vc.set_status_msg("Куда слать то? Порт закрыт...")
            return

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
            #self.vc.set_current_frequency(frequencies[0])
            self.__last_frequency_played = frequencies[0]
        else:
            self.vc.set_status_msg("Привет, меня зовут БАГ#3!")

    def stop_playing(self):
        self.reset_melody()
        success, command = protocol.build_command(CommandType.STOP_PLAYING)
        if success:
            self.serial.write(command)
            self.vc.set_current_frequency(0)
        else:
            self.vc.set_status_msg("Привет, меня зовут БАГ#4!")

    def record(self, note, convert: bool):
        to_record = parser.note_to_frequency(note) if convert else note
        txt = self.vc.get_raw_frequencies()
        self.vc.set_raw_frequencies(txt + ' {}'.format(to_record))

    def remove_last_recorded(self):
        txt = self.vc.get_raw_frequencies()
        sequence = parser.split_sequence(txt)
        if sequence:
            sequence.pop()
        self.vc.set_raw_frequencies(' '.join(sequence))


