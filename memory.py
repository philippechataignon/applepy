import numpy as np
from intelhex import IntelHex

class SoftSwitches:
    def __init__(self, display):
        self.kbd = 0x00
        self.display = display

    def read_byte(self, cycle, address):
        assert 0xC000 <= address <= 0xCFFF
        if address == 0xC000:
            return self.kbd
        elif address == 0xC010:
            self.kbd = self.kbd & 0x7F
        elif address == 0xC050:
            self.display.txtclr()
        elif address == 0xC051:
            self.display.txtset()
        elif address == 0xC052:
            self.display.mixclr()
        elif address == 0xC053:
            self.display.mixset()
        elif address == 0xC054:
            self.display.lowscr()
        elif address == 0xC055:
            self.display.hiscr()
        elif address == 0xC056:
            self.display.lores()
        elif address == 0xC057:
            self.display.hires()
        else:
            pass # print "%04X" % address
        return 0x00


class Memory:
    def __init__(self, display=None):
        self.size = 65536
        self.start = 0
        self.end = self.start + self.size - 1
        self._mem = np.zeros(self.size, dtype=np.int_)
        self.display = display
        self.softswitches = SoftSwitches(display)

    def store(self, address, data):
        for offset, datum in enumerate(data):
            self._mem[address - self.start + offset] = datum

    def read_byte(self, cycle, address):
        assert self.start <= address <= self.end
        if 0xC000 <= address < 0xD000:
            return self.softswitches.read_byte(cycle, address)
        else:
            return self._mem[address - self.start]

    def write_byte(self, address, value):
        if address < 0xC000 or address >= 0xD000:
            self._mem[address] = value
        if 0x400 <= address < 0x800 and self.display:
            self.display.update(address, value)
        if 0x2000 <= address < 0x5FFF and self.display:
            self.display.update(address, value)

    def load_file(self, filename):
        ih = IntelHex(filename)
        d = ih.todict()
        if "start_addr" in d:
            del d["start_addr"]
        for addr, v in d.items():
            self.write_byte(addr, v)

    def read_word(self, cycle, address):
        return self.read_byte(cycle, address) + (self.read_byte(cycle + 1, address + 1) << 8)

    def read_word_bug(self, cycle, address):
        if address % 0x100 == 0xFF:
            return self.read_byte(cycle, address) + (self.read_byte(cycle + 1, address & 0xFF00) << 8)
        else:
            return self.read_word(cycle, address)

    def write_byte(self, address, value):
        self._mem[address] = value
        if 0x400 <= address < 0x800 and self.display:
            self.display.update(address, value)
        if 0x2000 <= address < 0x5FFF and self.display:
            self.display.update(address, value)
