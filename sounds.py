import utime
from machine import Pin
from dacR2R import DacR2R
from micropython import const

MAX_LEVEL = const(127)


class Synth:
    def __init__(self):
        self.dac = DacR2R()
        self.dac.set(0)
        self.interval = 1000000 / 420
        self.curr_note = None
        self.hist = []
        self.saw_f = None

    def start(self, freq):
        self.curr_note = Note(freq)
        self.curr_note.begin()
        self.saw_f = self.curr_note.next_level_saw

    def stop(self):
        self.curr_note = None

    @micropython.native
    def sound(self):
        if self.curr_note is not None:
            level = self.saw_f()
            if level is not None:
                l = int(level)
                # self.hist.append(l)
                # print(l)
                self.dac.set(l)


class Note:
    def __init__(self, freq):
        self.interval = 1000000 / freq
        self.phase_start = None
        self.time_old = None
        self.level = None
        self.next_change = None
        self.time_us = utime.ticks_us
        self.time_diff = utime.ticks_diff

    def begin(self):
        self.level = MAX_LEVEL
        self.next_change = utime.ticks_us() + self.interval
        self.phase_start = utime.ticks_us()
        self.time_old = self.phase_start

    @micropython.native
    def next_level_saw(self):
        time_new = self.time_us()
        phase_went = self.time_diff(time_new, self.phase_start)
        if phase_went > self.interval:
            self.level = MAX_LEVEL
            self.phase_start = time_new
        else:
            self.level = MAX_LEVEL * ((self.interval - phase_went) / self.interval)
        # print(level)
        self.time_old = time_new
        return self.level

    @micropython.native
    def next_level_square(self):
        if utime.ticks_us() > self.next_change and self.level == MAX_LEVEL:
            self.level = 0
            self.next_change = self.next_change + self.interval
            return self.level
        if utime.ticks_us() > self.next_change and self.level == 0:
            self.level = MAX_LEVEL
            self.next_change = self.next_change + self.interval
            return self.level
        return None


@micropython.native
def test(freq):
    s = Synth()
    s.start(freq)
    s_f = s.sound
    changes = 10000
    r = range(changes)
    start_time = utime.ticks_us()
    for i in r:
        s_f()
    stop_time = utime.ticks_us()
    s.stop()
    sample_time = (stop_time - start_time)/changes
    print("Sample time: " + str(sample_time))
    print("Sample per Sec: " + str(1000000 / sample_time))

# def bench():

