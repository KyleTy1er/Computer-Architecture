#!/usr/bin/env python3

"""Main."""

from cpu import *

cpu = CPU()


try:
    cpu.load(sys.argv[1])
    cpu.run()
except IndexError:
    print("Please provide a file name.")