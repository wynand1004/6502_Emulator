# Parser Stuff
# Just testing ideas

from enum import Enum, auto

class Mode(Enum):
    IMPLIED = auto()
    IMMEDIATE = auto()
    ZP = auto()
    ZPX = auto()
    ZPY = auto()
    ABS = auto()
    ABX = auto()
    ABY = auto()
    INDX = auto()
    INDY = auto()

class Instruction():
    def __init__(self, name, mode, opcode, length):
        self.name = name
        self.mode = mode
        self.opcode = opcode
        self.length = length

lda = Instruction("LDA", Mode.IMMEDIATE, 0xA9, 2)

instructions = {
    "LDA": lda
}

assembly = """
LDA #1
STA 1050
LDX #0
STA 1050,X
INX
JMP 1024
"""

lines = assembly.split("\n")
print(lines)

commands = ["LDA", "STA", "LDX", "INX", "JMP"]

for line in lines:
    
    line = line.strip()
    
    # Skip blank lines
    if len(line) == 0:
        continue
        
    # Remember Labels
    elif line[-1] == ":":
        print(f"Label: {line}") 
        continue
        
    elif line[:3] in commands:
        print(f"Commmand: {line[:3]}")
        
        instruction_address = line.split(" ")
        
        if len(instruction_address) > 1:
            address = instruction_address[1]
            
            if address[0] == "#":
                address_number = int(address[1:])
                print(f"Immediate: {address_number}")
                
            elif address[-2:] == ",X":
                address_number = int(address[:len(address)-2])
                print(f"ABX: {address_number}")
            
            elif address[-2:] == ",Y":
                address_number = int(address[:len(address)-2])
                print(f"ABY: {address_number}")
                
            else:
                address_number = int(address)
                print(f"ABS: {address_number}")
        
        else:
            print(f"Implied")
        
        print(instruction_address)
        print()
