import ubinascii
import utime

from midiReceiver import MidiReceiver
# from nokiaLCD import NokiaLCD


def main():
    # lcd = NokiaLCD()
    # lcd.setup_lcd()
    mr = MidiReceiver(2)
    mr.set_note_off_callback(note_off)
    mr.set_note_on_callback(note_on)
    mr.set_cc_callback(cc)

    while True:
        # t1 = utime.ticks_us()
        mr.next_msg()
        # t2 = utime.ticks_us()
        # if msg is not None:
        #     print("Time: " + str(utime.ticks_diff(t1, t2)))
        # if msg is not None:
        #     info = str(ubinascii.hexlify(msg[0])) + "" \
        #            + str(ubinascii.hexlify(msg[1])) + "" \
        #            + str(ubinascii.hexlify(msg[2]))
        #     info = str(lp) + "." + info.replace("b'", "").replace("'", "")
        #     # lcd.write_next_line(info)
        #     print(info)
        #     lp += 1


def note_off(channel, note, velocity):
    print("OFF: " + str(channel) + " "
          + str(ubinascii.hexlify(note)) + " "
          + str(ubinascii.hexlify(velocity)))


def note_on(channel, note, velocity):
    print("ON : " + str(channel) + " "
          + str(ubinascii.hexlify(note)) + " "
          + str(ubinascii.hexlify(velocity)))


def cc(channel, device, value):
    print("CC : " + str(channel) + " "
          + str(ubinascii.hexlify(device)) + " "
          + str(ubinascii.hexlify(value)))
