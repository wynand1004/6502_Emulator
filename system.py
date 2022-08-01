import os
import time
from cpu6502 import *
from display import *

ram = [x for x in range(0, 65536)]
cpu = CPU(ram)

cpu.show_state()
display = TextDisplay(ram, 16384, 80, 2)

# Fill character memory with test values
c = 65
for i in range(16384, 16544):
    ram[i] = c
    c += 1
    if c > 91:
        c = 65

while True:
    cpu.inc()
    cpu.inx()
    cpu.inx()
    cpu.iny()
    cpu.iny()
    cpu.iny()
    
    os.system("clear")
    
    
    display.tick()
    time.sleep(0.1)
