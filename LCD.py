import smbus
import sys
from time import sleep


class LCD():
    def __init__(self, contrast=32, address=0x3e, bus_number=1, chars_per_line=8, display_lines=2):
        self.bus = smbus.SMBus(bus_number)
        self.address = address
        self.contrast = contrast
        self.register_setting = 0x00
        self.register_display = 0x40
        self.chars_per_line = chars_per_line
        self.display_lines = display_lines
        self.display_chars = chars_per_line * display_lines
        self.position = 0
        self.line = 0

        self.setup_st7032()

    def setup_st7032(self):
        trials = 5
        for i in range(trials):
            try:
                c_lower = (self.contrast & 0xf)
                c_upper = (self.contrast & 0x30)>>4
                self.bus.write_i2c_block_data(self.address, self.register_setting, [0x38, 0x39, 0x14, 0x70|c_lower, 0x54|c_upper, 0x6c])
                sleep(0.2)
                self.bus.write_i2c_block_data(self.address, self.register_setting, [0x38, 0x0d, 0x01])
                sleep(0.001)
                break
            except IOError:
                if i==trials-1:
                    sys.exit()

    def clear(self):
        self.position = 0
        self.line = 0
        self.bus.write_byte_data(self.address, self.register_setting, 0x01)
        sleep(0.001)

    def newline(self):
        if self.line == self.display_lines-1:
            self.clear()
        else:
            self.line += 1
            self.position = self.chars_per_line * self.line
            self.bus.write_byte_data(self.address, self.register_setting, 0xc0)
            sleep(0.001)

    def write_string(self, s):
        for c in list(s):
            self.write_char(ord(c))

    def write_char(self, c):
        byte_data = self.check_writable(c)
        if self.position == self.display_chars:
            self.clear()
        elif self.position == self.chars_per_line*(self.line+1):
            self.newline()
        self.bus.write_byte_data(self.address, self.register_display, byte_data)
        self.position += 1

    def check_writable(self, c):
        if 0x06 <= c <= 0xff :
            return c
        else:
            return 0x20 


if (__name__ == "__main__"):
    lcd = LCD()
    lcd.write_string("Hello World")
