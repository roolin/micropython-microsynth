import pcd8544
from machine import Pin, SPI, PWM


class NokiaLCD:
    def __init__(self):
        self.next_line = 0
        self.lcd = None

    def setup_lcd(self):
        spi = SPI(-1, baudrate=2000000, polarity=0, phase=0, sck=Pin(19), mosi=Pin(23), miso=Pin(13))  # D5-14, D1-5, D0-16
        spi.init(baudrate=2000000, polarity=0, phase=0)
        cs = Pin(5)  # D4 CE
        dc = Pin(18)  # D2 DC
        rst = Pin(4)  # D3 RST
        bl = Pin(22, Pin.OUT, value=1)  # D6 LIGHT

        bl_pwm = PWM(bl)
        bl_pwm.freq(500)
        bl_pwm.duty(512)  # dim

        self.lcd = pcd8544.PCD8544_FRAMEBUF(spi, cs, dc, rst)

        self.lcd.contrast(60, pcd8544.BIAS_1_48, pcd8544.TEMP_COEFF_2)

        # fill(color)
        self.lcd.fill(0)
        self.lcd.show()

    def write_next_line(self, line):
        if self.next_line > 40:
            self.next_line = 0
        self.lcd.fill_rect(0, self.next_line, 84, 10, 0)
        self.lcd.text(line, 0, self.next_line, 1)
        self.next_line += 10
        self.lcd.show()
