from view_controller import ViewController
from serial_port import SerialPort


class App:
    """Посредник для компонентов программы."""
    def __init__(self):
        self.vc = ViewController(self)
        self.serial = SerialPort(self)

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

    def process_packet(self):
        pass
