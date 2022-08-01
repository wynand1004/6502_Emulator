# Character Display
# Will need start of character memory, width, height
# Currently will print - later graphical

class TextDisplay():
    def __init__(self, ram, start, width, height):
        self.ram = ram
        self.start = start
        self.width = width
        self.height = height
        
    def tick(self):
        for row in range(0, self.height):
            for col in range(0, self.width):
                c = self.ram[self.start + col + (self.width * row)]
                # Only print basic ASCII Characters
                # Otherwise print a space
                if c >= 32 and c <= 126:
                    print(chr(c), end='')
                else:
                    print(" ", end='')
            print()
        print()

class GraphicDisplay():
    def __init__(self, ram, start, width, height):
        self.ram = ram
        self.start = start
        self.width = width
        self.height = height
        
    def tick(self):
        for row in range(0, self.height):
            for col in range(0, self.width):
                c = self.ram[self.start + col + (self.width * row)]
                # For now, print O or nothing
                if c > 0:
                    print("O", end='')
                else:
                    print(" ", end='')
            print()
        print()
