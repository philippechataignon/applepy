# ApplePy - an Apple ][ emulator in Python
# James Tauber / http://jtauber.com/
# originally written 2001, updated 2011

import pygame
import sys

from cpu import CPU
from memory import Memory
from display import Display


def usage():
    print("ApplePy - an Apple ][ emulator in Python", file=sys.stderr)
    print("James Tauber / http://jtauber.com/", file=sys.stderr)
    print(file=sys.stderr)
    print("Usage: applepy.py [options]", file=sys.stderr)
    print(file=sys.stderr)
    print("    -R, --rom      ROM file to use (default A2ROM.BIN)", file=sys.stderr)
    print("    -r, --ram      RAM file to load (default none)", file=sys.stderr)
    print("    -q, --quiet    Quiet mode, no sounds (default sounds)", file=sys.stderr)
    sys.exit(1)


def get_options():
    class Options:
        def __init__(self):
            self.rom = "A2ROM.BIN"
            self.ram = None
            self.quiet = False

    options = Options()
    a = 1
    while a < len(sys.argv):
        if sys.argv[a].startswith("-"):
            if sys.argv[a] in ("-R", "--rom"):
                a += 1
                options.rom = sys.argv[a]
            elif sys.argv[a] in ("-r", "--ram"):
                a += 1
                options.ram = sys.argv[a]
            elif sys.argv[a] in ("-q", "--quiet"):
                options.quiet = True
            else:
                usage()
        else:
            usage()
        a += 1

    return options


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=str, default="A2ROM.BIN", help="ROM image file")
    parser.add_argument("--load", type=str, help="program  image file")
    parser.add_argument("--address", type=int, default=0x1000, help="load address")
    options = parser.parse_args()
    display = Display()
    mem = Memory(options, display)
    cpu = CPU(mem)
    cpu.run()
