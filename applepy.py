#!/usr/bin/env python3

# ApplePy - an Apple ][ emulator in Python
# James Tauber / http://jtauber.com/
# originally written 2001, updated 2011
# updated 2021 Philippe Chataignon

import pygame
import sys

from cpu import CPU
from memory import Memory
from display import Display

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=str, default="apple2plus.rom", help="ROM image file")
    parser.add_argument("--hex", type=str, help="program hex file")
    parser.add_argument("--bin", type=str, help="program bin file")
    parser.add_argument("--addr", type=int, help="start address of program bin file")
    parser.add_argument("--log", type=str, help="log file")
    options = parser.parse_args()
    display = Display()
    mem = Memory(options, display)
    cpu = CPU(options, mem)
    cpu.run()
