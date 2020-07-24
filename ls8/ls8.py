#!/usr/bin/env python3

"""Main."""
import sys
from cpu import *

cpu = CPU()


try:
    # cpu.load(f"examples/{sys.argv[1]}")
    cpu.load("examples/call.ls8")
    cpu.run()
    # print(cpu.ram)

except FileNotFoundError:
    print(f"Could not find {sys.argv[1]}")

except IndexError:
    print(f"Could not find {sys.argv[1]}")


