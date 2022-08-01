import os
import time
from cpu6502 import *
from display import TextDisplay
from display import GraphicDisplay

# Create system ram
ram = [0 for x in range(0, 65536)]

# Create CPU and pass ram reference
cpu = CPU(ram)

# Create text display using ram, starting character memory, columns and rows
text_display = TextDisplay(ram, 16384, 80, 2)

# Create graphics display using ram, starting graphics memory, columns and rows
# This will eventually become actual graphics
graphic_display = GraphicDisplay(ram, 32768, 5, 5)

# Fill character memory with test values
c = 65
for i in range(16384, 16544):
    ram[i] = c
    c += 1
    if c > 91:
        c = 65

# LDA with 65 (A)
cpu.lda(65)
# Store at start of character memory
cpu.sta(16384)

while True:
    cpu.inc()
    cpu.sta(16384)
    
    cpu.ldx(1)
    cpu.stx(32768)
    cpu.stx(32774)
    cpu.stx(32780)
    cpu.stx(32786)
    cpu.stx(32792)

    os.system("clear")
    
    text_display.tick()
    
    graphic_display.tick()
    
    # cpu.show_state()
    time.sleep(0.05)
