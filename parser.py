from lexer2 import Tokeniser

class Parser:
    def __init__(self, string):
        self.lexer = Tokeniser()
        self.pos = 0
        self.current_token = self.lexer.tokens[self.pos] if self.lexer.tokens else None



    def advance(self):
        self.pos += 1
        if self.pos >= len(self.string):
            self.current_char = None
        else:
            self.current_char = self.string[self.pos]

    def parse(self):
        statements = []
        while self.current_token:
            statements.append(self.statement)
        return statements


