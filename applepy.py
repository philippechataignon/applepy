#!/usr/bin/env python3

# ApplePy - an Apple ][ emulator in Python
# James Tauber / http://jtauber.com/
# originally written 2001, updated 2011

import pygame

from cpu import CPU
from memory import Memory
from display import Display

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--hex", type=str, help="data hex file", action="append")
    options = parser.parse_args()
    display = Display()
    mem = Memory(display)
    if options.hex:
        for infile in options.hex:
            mem.load_file(infile)
    cpu = CPU(mem)
    cpu.run()
