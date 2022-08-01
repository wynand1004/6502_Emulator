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
            234: "nop"
        }    
        
        # Set up RAM
        # Note, a real 6502 would not have default RAM
        self.ram = ram

    # Returns the related value depending on the mode
    def get_value(self, value, mode):
        if(mode == Mode.IMMEDIATE):
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
        
            
    def decode_opcode(opcode):
        pass

    # Note: INC in implied mode (accumulator) is not part of the orginal 6502 spec
    def inc(self, mode=Mode.IMPLIED, value = 0):
        # Increment accumulator by 1
        self.a += 1
        
        # Roll over 255 -> 0
        if self.a == 256:
            self.a = 0
            
        self.pc += 1
        
    def inx(self):
        # Increment X by 1
        self.x += 1
        
        # Roll over 255 -> 0
        if self.x == 256:
            self.x = 0
            
        self.pc += 1
    
    def iny(self):
        # Increment y by 1
        self.y += 1
        
        # Roll over 255 -> 0
        if self.y == 256:
            self.y = 0
            
        self.pc += 1
        
    def tax(self):
        self.x = self.a
        
        self.pc += 1
        
    def txa(self):
        self.a = self.x
        
        self.pc += 1
        
    def dex(self):
        self.x -= 1
        
        # Roll over 0 -> 255
        if self.x < 0:
            self.x = 255
            
        self.pc += 1
            
    def tay(self):
        self.y = self.a
        
        self.pc += 1
        
    def tya(self):
        self.a = self.y
        
        self.pc += 1
        
    def dey(self):
        self.y -= 1
        
        # Roll over 0 -> 255
        if self.y < 0:
            self.y = 255    
            
        self.pc += 1
        
    def clc(self):
        self.c = False
        
        self.pc += 1
        
    def sec(self):
        self.c = True
        
        self.pc += 1
        
    def cli(self):
        self.i = False
        
        self.pc += 1
        
    def sei(self):
        self.i = True
        
        self.pc += 1
        
    def cld(self):
        self.d = False
        
        self.pc += 1
        
    def sed(self):
        self.d = True
        
        self.pc += 1

    def clv(self):
        self.v = False
        
        self.pc += 1

    def nop(self):
        self.pc += 1
        
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
        
    def show_state(self):
        print(f"A: {self.a}")
        print(f"X: {self.x}")
        print(f"Y: {self.y}")
        print(f"PC: {self.pc}")
        print(self.ram[16384])


# Basic testing / example code
if __name__ == "__main__":
    cpu = CPU()
    cpu.show_state()
    cpu.inc()
    cpu.inx()
    cpu.iny()
    cpu.show_state()
    cpu.inc()
    cpu.tax()
    cpu.iny()
    cpu.iny()
    cpu.tya()
    cpu.show_state()
