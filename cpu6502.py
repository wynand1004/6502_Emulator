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

            0xA9: (self.lda, Mode.IMMEDIATE, 2),
            0xA5: (self.lda, Mode.ZP, 2),
            0xB5: (self.lda, Mode.ZPX, 2),
            0xAD: (self.lda, Mode.ABS, 3),
            0xBD: (self.lda, Mode.ABX, 3),
            0xB9: (self.lda, Mode.ABY, 3),
            
            0xA2: (self.ldx, Mode.IMMEDIATE, 2),
            
            0xAC: (self.ldy, Mode.ABS, 3),
            
            0x8D: (self.sta, Mode.ABS, 3),

            0x4C: (self.jmp, Mode.ABS, 0)
        }    

        # Set up RAM
        # Note, a real 6502 would not have default RAM
        self.ram = ram
    
    # Resets all registers to default values
    def reset(self):
        self.a = 0
        self.x = 0
        self.y = 0

        self.n = False
        self.v = False
        self.r = True
        self.b = False
        self.d = False
        self.i = False
        self.z = False
        self.c = False
        
        self.pc = 1024    
        

    # Returns the related value depending on the mode
    # This is for the functions
    def get_value(self, address, mode):
        if(mode == Mode.IMPLIED):
            return None
        else:
            return self.ram[address]
    
    # This is for the decoder
    def get_memory_address(self, mode):
        if(mode == Mode.IMPLIED):
            return None
            
        elif(mode == Mode.IMMEDIATE):
            return self.pc + 1
            
        elif(mode == Mode.ZP):
            address = ram[self.pc + 1]
            if address > 255:
                address -= 256
            return address
            
        elif(mode == Mode.ZPX):
            address = self.ram[self.pc + 1] + self.x
            if address > 255:
                address -= 256
            return address
            
        elif(mode == Mode.ABS):
            return self.ram[self.pc + 1] + (self.ram[self.pc + 2] * 256)
            
        elif(mode == Mode.ABX):
            return self.ram[self.pc +1] + (self.ram[self.pc +2 ] * 256) + self.x
            
        elif(mode == Mode.ABY):
            return self.ram[self.pc+1] + (self.ram[self.pc+2] * 256) + self.y
        
    # Note: INC in implied mode (accumulator) is not part of the orginal 6502 spec
    def inc(self, address = None, mode = Mode.IMPLIED):
        # Increment accumulator by 1
        self.a += 1
        
        # Roll over 255 -> 0
        if self.a > 255:
            self.a -= 256
        
    def inx(self, address = None, mode = Mode.IMPLIED):
        # Increment X by 1
        self.x += 1
        
        # Roll over 255 -> 0
        if self.x > 255:
            self.x -= 256
    
    def iny(self, address = None, mode = Mode.IMPLIED):
        # Increment y by 1
        self.y += 1
        
        # Roll over 255 -> 0
        if self.y > 255:
            self.y -= 256
        
    def tax(self, address = None, mode = Mode.IMPLIED):
        self.x = self.a
        
    def txa(self, address = None, mode = Mode.IMPLIED):
        self.a = self.x
        
    def dex(self, address = None, mode = Mode.IMPLIED):
        self.x -= 1
        
        # Roll over 0 -> 255
        if self.x < 0:
            self.x += 256
            
    def tay(self, address = None, mode = Mode.IMPLIED):
        self.y = self.a
        
    def tya(self, address = None, mode = Mode.IMPLIED):
        self.a = self.y
        
    def dey(self, address = None, mode = Mode.IMPLIED):
        self.y -= 1
        
        # Roll over 0 -> 255
        if self.y < 0:
            self.y += 256    
        
    def clc(self, address = None, mode = Mode.IMPLIED):
        self.c = False
        
    def sec(self, address = None, mode = Mode.IMPLIED):
        self.c = True
        
    def cli(self, address = None, mode = Mode.IMPLIED):
        self.i = False
        
    def sei(self, address = None, mode = Mode.IMPLIED):
        self.i = True
        
    def cld(self, address = None, mode = Mode.IMPLIED):
        self.d = False
        
    def sed(self, address = None, mode = Mode.IMPLIED):
        self.d = True

    def clv(self, address = None, mode = Mode.IMPLIED):
        self.v = False

    def nop(self, address = None, mode = Mode.IMPLIED):
        pass
        
    def lda(self, address, mode=Mode.IMMEDIATE):
        self.a = self.get_value(address, mode)

    def ldx(self, address, mode=Mode.IMMEDIATE):
        self.x = self.get_value(address, mode)
        
    def ldy(self, address, mode=Mode.IMMEDIATE): 
        self.y = self.get_value(address, mode)

    def sta(self, address, mode=Mode.ABS):
        self.ram[address] = self.a
        
    def stx(self, address, mode=Mode.ABS):
        self.ram[address] = self.x
        
    def sty(self, address, mode=Mode.ABS):
        self.ram[address] = self.y
        
    def jmp(self, address = None, mode=Mode.ABS):
        # Note, for jmp in ABS mode, we get the memory value directly
        if not address:
            address = self.get_memory_address(mode)
        self.pc = address
        
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
        
            # input(f"opcode: {opcode}  mode: {mode}  address: {self.get_memory_address(mode)}")
            # Execute
            # Get the value from memory and execute with function
            fn(self.get_memory_address(mode), mode)
            # Update the program counter to the next opcode
            # Note, 0 is used for jmp as it resets the pc directly
            self.pc += length
        else:
            print(f"Unknown Opcode: {opcode} at memory location {self.pc}")

# Basic testing / example code
if __name__ == "__main__":
    import time
    import os
    
    cpu = CPU()
    
    cpu.ram[32] = 0xFF
    cpu.ram[33] = 0x20

    cpu.ram[1024] = 0xA2 # LDX #1
    cpu.ram[1025] = 0x01 # 1
    cpu.ram[1026] = 0xB5 # LDA ZP X-offset 0x20
    cpu.ram[1027] = 0x20 # NOP
    cpu.ram[1028] = 0xEA # NOP
    
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
    
    cpu.ram[1046] = 0x4C # JMP 0x0400 (1027)
    cpu.ram[1047] = 0x00
    cpu.ram[1048] = 0x04
    
    # Data for testing
    cpu.ram[1049] = 0xFF
    cpu.ram[1050] = 0x10
    
    
    cycle = 0
    
    while True:
        cpu.tick()
        cycle += 1
        if cycle % 1 == 0:
            os.system("clear")
            cpu.show_state()
        time.sleep(0.01)
    

