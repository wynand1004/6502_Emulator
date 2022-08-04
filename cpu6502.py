# 6502 CPU Emulator
# By @TokyoEdtech
# Minimum Python Version: 3.4

from enum import Enum, auto

class Mode(Enum):
    IMPLIED = auto()
    IMMEDIATE = auto()
    ZP = auto()
    ZPX = auto()
    ABS = auto()
    ABX = auto()
    ABY = auto()
    INDX = auto()
    INDY = auto()
    
class CPU():
    def __init__(self, ram=[0 for x in range(0, 65536)]):
        self.a = 0
        self.x = 0
        self.y = 0
        
        # flags
        # Negative
        self.n = False
        # Overflow
        self.v = False
        # Reserved (Unused)
        self.r = True # This is always set to True
        # Break
        self.b = False
        # Decimal
        self.d = False
        # Interrupt
        self.i = False
        # Zero
        self.z = False
        # Carry
        self.c = False
        
        self.pc = 1024
        
        self.opcodes = {
            0xA9: (self.lda, Mode.IMMEDIATE, 2),
            0xE8: (self.inx, Mode.IMPLIED, 1),
            0xC8: (self.iny, Mode.IMPLIED, 1),
            0xAA: (self.tax, Mode.IMPLIED, 1),
            0x8A: (self.txa, Mode.IMPLIED, 1),
            0xCA: (self.dex, Mode.IMPLIED, 1),
            0xA8: (self.tay, Mode.IMPLIED, 1),
            0x98: (self.tya, Mode.IMPLIED, 1),
            0x88: (self.dey, Mode.IMPLIED, 1),
            0xEA: (self.nop, Mode.IMPLIED, 1),
            0x18: (self.clc, Mode.IMPLIED, 1),
            0x38: (self.sec, Mode.IMPLIED, 1),
            0x58: (self.cli, Mode.IMPLIED, 1),
            0x78: (self.sei, Mode.IMPLIED, 1),
            0xB8: (self.clv, Mode.IMPLIED, 1),
            0xD8: (self.cld, Mode.IMPLIED, 1),
            0xF8: (self.sed, Mode.IMPLIED, 1),
            0x4C: (self.jmp, Mode.ABS, 0),
        }    
        
        # Set up RAM
        # Note, a real 6502 would not have default RAM
        self.ram = ram

    # Returns the related value depending on the mode
    # This is for the functions
    def get_value(self, value, mode):
        if(mode == Mode.IMPLIED):
            return None
            
        elif(mode == Mode.IMMEDIATE):
            return value
            
        elif(mode == Mode.ZP):
            return self.ram[value]
            
        elif(mode == Mode.ZPX):
            return self.ram[value+self.x]
            
        elif(mode == Mode.ABS):
            return value
            
        elif(mode == Mode.ABX):
            return self.ram[value+self.x]
            
        elif(mode == Mode.ABY):
            return self.ram[value+self.y]
    
    # This is for the decoder
    def get_memory_value(self, mode):
        if(mode == Mode.IMPLIED):
            return None
            
        elif(mode == Mode.IMMEDIATE):
            address = self.pc + 1
            return self.ram[address]
            
        elif(mode == Mode.ZP):
            address = self.ram[self.pc+1]
            return self.ram[address]
            
        elif(mode == Mode.ZPX):
            address = self.ram[self.pc+1]+self.x
            return self.ram[address]
            
        elif(mode == Mode.ABS):
            address = self.ram[self.pc+1] + self.ram[self.pc+2] * 16
            return address
            
        elif(mode == Mode.ABX):
            address = (self.ram[self.pc+1] + self.ram[self.pc+2] * 16) + self.x
            return self.ram[address]
            
        elif(mode == Mode.ABY):
            address = (self.ram[self.pc+1] + self.ram[self.pc+2] * 16) + self.y
            return self.ram[address]
        
    # Note: INC in implied mode (accumulator) is not part of the orginal 6502 spec
    def inc(self, value = None, mode = Mode.IMPLIED):
        # Increment accumulator by 1
        self.a += 1
        
        # Roll over 255 -> 0
        if self.a == 256:
            self.a = 0
        
    def inx(self, value = None, mode = Mode.IMPLIED):
        # Increment X by 1
        self.x += 1
        
        # Roll over 255 -> 0
        if self.x == 256:
            self.x = 0
    
    def iny(self, value = None, mode = Mode.IMPLIED):
        # Increment y by 1
        self.y += 1
        
        # Roll over 255 -> 0
        if self.y == 256:
            self.y = 0
        
    def tax(self, value = None, mode = Mode.IMPLIED):
        self.x = self.a
        
    def txa(self, value = None, mode = Mode.IMPLIED):
        self.a = self.x
        
    def dex(self, value = None, mode = Mode.IMPLIED):
        self.x -= 1
        
        # Roll over 0 -> 255
        if self.x < 0:
            self.x = 255
            
    def tay(self, value = None, mode = Mode.IMPLIED):
        self.y = self.a
        
    def tya(self, value = None, mode = Mode.IMPLIED):
        self.a = self.y
        
    def dey(self, value = None, mode = Mode.IMPLIED):
        self.y -= 1
        
        # Roll over 0 -> 255
        if self.y < 0:
            self.y = 255    
        
    def clc(self, value = None, mode = Mode.IMPLIED):
        self.c = False
        
    def sec(self, value = None, mode = Mode.IMPLIED):
        self.c = True
        
    def cli(self, value = None, mode = Mode.IMPLIED):
        self.i = False
        
    def sei(self, value = None, mode = Mode.IMPLIED):
        self.i = True
        
    def cld(self, value = None, mode = Mode.IMPLIED):
        self.d = False
        
    def sed(self, value = None, mode = Mode.IMPLIED):
        self.d = True

    def clv(self, value = None, mode = Mode.IMPLIED):
        self.v = False

    def nop(self, value = None, mode = Mode.IMPLIED):
        pass
        
    def lda(self, value, mode=Mode.IMMEDIATE):
        # Convert value based on mode
        value = self.get_value(value, mode)
        self.a = value
        
    def sta(self, value, mode=Mode.ABS):
        value = self.get_value(value, mode)
        self.ram[value] = self.a

    def ldx(self, value, mode=Mode.IMMEDIATE):
        # Convert value based on mode
        value = self.get_value(value, mode)
        self.x = value
        
    def stx(self, value, mode=Mode.ABS):
        value = self.get_value(value, mode)
        self.ram[value] = self.x
        
    def jmp(self, value, mode=Mode.ABS):
        value = self.get_value(value, mode)
        self.pc = value
        
    def show_state(self):
        print(f"A: {self.a}")
        print(f"X: {self.x}")
        print(f"Y: {self.y}")
        print(f"PC: {self.pc}")
        
    def tick(self):
        # Note, for this emulator, we are ignoring the timing 
        # Each command will take the same amount of time
        # May implement later
        # Fetch
        opcode = self.ram[self.pc]
        
        # Decode
        if opcode in self.opcodes:
            fn = self.opcodes[opcode][0]
            mode = self.opcodes[opcode][1]
            length = self.opcodes[opcode][2]
        
            # Execute
            # Get the value from memory and execute with function
            fn(self.get_memory_value(mode), mode)
            # Update the program counter to the next opcode
            # Note, 0 is used for jmp as it resets the pc directly
            self.pc += length

# Basic testing / example code
if __name__ == "__main__":
    import time
    import os
    
    cpu = CPU()
    cpu.ram[1024] = 0xA9 # LDA IMMEDIATE
    cpu.ram[1025] = 0xFF # FF
    cpu.ram[1026] = 0xCA # DEX
    cpu.ram[1027] = 0x88 # DEY
    cpu.ram[1028] = 0x8A # TXA
    
    cpu.ram[1029] = 0xEA # NOP
    cpu.ram[1030] = 0xEA # NOP
    cpu.ram[1031] = 0xEA # NOP
    cpu.ram[1032] = 0xEA # NOP
    cpu.ram[1033] = 0xEA # NOP
    cpu.ram[1034] = 0xEA # NOP
    cpu.ram[1035] = 0xEA # NOP
    cpu.ram[1036] = 0xEA # NOP
    cpu.ram[1037] = 0xEA # NOP
    cpu.ram[1038] = 0xEA # NOP
    cpu.ram[1039] = 0xEA # NOP
    cpu.ram[1040] = 0xEA # NOP
    cpu.ram[1041] = 0xEA # NOP
    cpu.ram[1042] = 0xEA # NOP
    cpu.ram[1043] = 0xEA # NOP
    cpu.ram[1044] = 0xEA # NOP
    cpu.ram[1045] = 0xEA # NOP
    
    cpu.ram[1046] = 0x4C # JMP 0x0402 (1024)
    cpu.ram[1047] = 0x02
    cpu.ram[1048] = 0x40
    
    cycle = 0
    
    while True:
        cpu.tick()
        cycle += 1
        if cycle % 1 == 0:
            os.system("clear")
            cpu.show_state()
        time.sleep(0.01)
    

