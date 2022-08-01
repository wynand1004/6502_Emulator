from cpu6502 import *


ram = [x for x in range(0, 65536)]
cpu = CPU(ram)

cpu.show_state()
