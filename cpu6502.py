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
            0x4C: (self.jmp, Mode.ABS, 3)
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
        self.pc = value - 3 # Ugly hack due to the pc being incremented outside the function
        
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
            self.pc += length

# Basic testing / example code
if __name__ == "__main__":
    import time
    import os
    
    cpu = CPU()
    cpu.ram[1024] = 0xA9 # LDA IMMEDIATE
    cpu.ram[1025] = 0x01 # 1
    cpu.ram[1026] = 0xE8 # INX
    cpu.ram[1027] = 0xC8 # INY
    cpu.ram[1028] = 0x4C # JMP 0x0400 (1024)
    cpu.ram[1029] = 0x00
    cpu.ram[1030] = 0x40
    
    while True:
        cpu.tick()
        
        os.system("clear")
        cpu.show_state()
        time.sleep(0.1)
    

