from pyb import Pin, ADC
import time
from micropython import const


FIRST_PIN = const(3)
PINS_NUMBER = const(7)
MAX_V_LEVEL = const(127)


def string_to_int_list(val):
    t = []
    for v in val:
        t.append(int(v))
    return t


class DacR2R:
    def __init__(self):
        self.pin_names = ['B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']
        self.pins = []
        self.binary_table = {}
        self.pin_value_f = []
        self.setup()

    def setup(self):
        for i in range(PINS_NUMBER):
            p_out = Pin(self.pin_names[i], Pin.OUT_PP)
            p_out.low()
            self.pins.append(p_out)

    @micropython.viper
    def set(self, v: int):
        p = ptr16(stm.GPIOB + stm.GPIO_BSRR)
        p[1] = MAX_V_LEVEL << FIRST_PIN
        p[0] = v << FIRST_PIN


@micropython.native
def runs():
    dac = DacR2R()
    adc = ADC(Pin('A4'))
    out = []
    start = time.ticks_us()
    set_f = dac.set
    for i in range(MAX_V_LEVEL + 1):
        set_f(i)
        # read = adc.read()
        # out.append((i, read))
    stop = time.ticks_us()
    print("Czas: " + str(stop - start))
    print("Per zmiana: " + str((stop - start)/(MAX_V_LEVEL + 1)))
    print(out)
