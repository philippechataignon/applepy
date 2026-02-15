import numpy as np
from intelhex import IntelHex

class Memory:
    def __init__(self, display=None):
        self.mem = np.zeros(0x10000, dtype=np.int32)
        self.display = display
        self.kbd = 0

    def store(self, address, data):
        for offset, datum in enumerate(data):
            self.mem[address + offset] = datum

    def read_byte(self, address):
        if address == 0xC000:
            return self.kdb
        if address == 0xC010:
            self.kdb = self.kbd & 0x7F
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
        return self.mem[address]

    def write_byte(self, address, value):
        self.mem[address] = value
        if self.display and 0x400 <= address < 0x800:
            self.display.update(address, value)
        if self.display and 0x2000 <= address < 0x5FFF:
            self.display.update(address, value)

    def load_file(self, filename):
        ih = IntelHex(filename)
        d = ih.todict()
        if "start_addr" in d:
            del d["start_addr"]
        for addr, v in d.items():
            self.write_byte(addr, v)

    def read_word(self, address):
        return self.read_byte(address) + (self.read_byte(address + 1) << 8)

    def read_word_bug(self, address):
        if address & 0xff == 0xff:
            return self.read_byte(address) + (self.read_byte(address & 0xff00) << 8)
        else:
            return self.read_word(address)
