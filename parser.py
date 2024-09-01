from lexer2 import Tokeniser

class Parser:
    def __init__(self, string):
        self.lexer = Tokeniser()
        self.string = string
        self.pos = 0

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.string):
            self.current_char = None
        else:
            self.current_char = self.string[self.pos]



