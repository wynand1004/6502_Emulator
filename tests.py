# cpu6502 Tests

# Test CPU Creation
from cpu6502 import *

# Create system ram
ram = [0 for x in range(0, 65536)]

# Create CPU and pass ram reference
cpu = CPU(ram)

# Check default settings
print("Accumulator = 0", end='')
if cpu.a == 0:
    print("\tPassed")
else:
    print("\tFailed")
    
print("X = 0", end='')
if cpu.x == 0:
    print("\tPassed")
else:
    print("\tFailed")
    
# TEST: LDA #1 IMMEDIATE
