from machine import UART


class MidiReceiver:
    def __init__(self, uart_number):
        self.uart = UART(uart_number, baudrate=31250)
        self.uart.init(31250, bits=8, parity=None, stop=1)
        self.note_on_callback = None
        self.note_off_callback = None
        self.cc_callback = None

        self.message_exe = {
            8: self.__note_off,  # hex: 8
            9: self.__note_on,  # hex: 9
            11: self.__cc  # hex: C
        }

    def __read_data_block(self, amount):
        data = []
        for i in range(amount):
            dt = self.uart.read(1)
            while dt is None:
                dt = self.uart.read(1)
            data.append(dt)
        return data

    def __note_off(self, channel):
        data = self.__read_data_block(2)
        return self.note_off_callback(channel, data[0], data[1])

    def __note_on(self, channel):
        data = self.__read_data_block(2)
        return self.note_on_callback(channel, data[0], data[1])

    def __cc(self, channel):
        data = self.__read_data_block(2)
        return self.cc_callback(channel, data[0], data[1])

    def set_note_off_callback(self, fun):
        self.note_off_callback = fun

    def set_note_on_callback(self, fun):
        self.note_on_callback = fun

    def set_cc_callback(self, fun):
        self.cc_callback = fun

    def next_msg(self):
        msg = self.uart.read(1)
        if msg is None:
            return
        # print("Command: " + str(msg[0]))
        command = self.message_exe.get(msg[0] >> 4)
        if command is None:
            return
        channel = msg[0] & 15  # 00001111 mask
        command(channel)
