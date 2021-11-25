import numpy

class ROM:
    def __init__(self, start, size):
        self.start = start
        self.end = start + size - 1
        self._mem = numpy.zeros(size, dtype=numpy.uint8)
        self.log = open("memory.log", "w")

    def load(self, address, data):
        for offset, datum in enumerate(data):
            self._mem[address - self.start + offset] = datum

    def load_file(self, address, filename):
        with open(filename, "rb") as f:
            self._mem = numpy.fromfile(f, dtype=numpy.uint8)

    def read_byte(self, address):
        assert self.start <= address <= self.end
        a = address - self.start
        v = self._mem[a]
        return v

class RAM(ROM):

    def write_byte(self, address, value):
        self._mem[address] = value
        if address not in (0x4e, 0x4f):
            print(f"[{hex(address)}]<- {hex(value)}]", file=self.log)

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
    def __init__(self, options=None, display=None):
        self.display = display

        self.rom = ROM(0xD000, 0x3000)
        if options.rom:
            self.rom.load_file(0xD000, options.rom)

        self.ram = RAM(0x0000, 0xC000)
        if options.load and options.address:
            with open(options.load, "rb") as f:
                buff = f.read()
                self.ram.load(options.address, buff)

        self.softswitches = SoftSwitches(display)

    def load(self, address, data):
        if address < 0xC000:
            self.ram.load(address, data)

    def read_byte(self, cycle, address):
        if address < 0xC000:
            return self.ram.read_byte(address)
        elif address < 0xD000:
            return self.softswitches.read_byte(cycle, address)
        else:
            return self.rom.read_byte(address)

    def read_word(self, cycle, address):
        return self.read_byte(cycle, address) + (self.read_byte(cycle + 1, address + 1) << 8)

    def read_word_bug(self, cycle, address):
        if address % 0x100 == 0xFF:
            return self.read_byte(cycle, address) + (self.read_byte(cycle + 1, address & 0xFF00) << 8)
        else:
            return self.read_word(cycle, address)

    def write_byte(self, address, value):
        if address < 0xC000:
            self.ram.write_byte(address, value)
        if 0x400 <= address < 0x800 and self.display:
            self.display.update(address, value)
        if 0x2000 <= address < 0x5FFF and self.display:
            self.display.update(address, value)
