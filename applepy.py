#!/usr/bin/env python3

# ApplePy - an Apple ][ emulator in Python
# James Tauber / http://jtauber.com/
# originally written 2001, updated 2011

import pygame
import sys

from cpu import CPU
from memory import Memory
from display import Display

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=str, default="apple2plus.rom", help="ROM image file")
    parser.add_argument("--load", type=str, help="program  image file")
    parser.add_argument("--address", type=int, default=0x1000, help="load address")
    parser.add_argument("--rom_address", type=int, default=0xd000, help="ROM load address")
    parser.add_argument("--log", type=str, help="log file")
    options = parser.parse_args()
    display = Display()
    mem = Memory(options, display)
    cpu = CPU(options, mem)
    cpu.run()
