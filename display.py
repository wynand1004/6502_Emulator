# Character Display
# Will need ram reference, start of character memory, width, height
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
                print(chr(c), end='')
            print()
        print()
