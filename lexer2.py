class Token:
    def __init__(self):
        self.type = ""
        self.value = ""

class Tokeniser:
    def __init__(self, string):
        self.tokens = []
        self.string = string
        self.pos = 0
        self.current_char = self.string[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.string):
            self.current_char = None
        else:
            self.current_char = self.string[self.pos]

    def generate(self):
        while self.current_char is not None:
            if self.current_char == " ":
                self.advance()
            elif self.current_char.isalpha():
                self.stringToken()
            elif self.current_char.isdigit():
                self.numberToken()



    def numberToken(self):
        numStr = ""
        while self.current_char is not None and self.current_char.isdigit():
            numStr += self.current_char
            self.advance()

        self.tokens.append({"type": int, "value": numStr})
        return int(numStr)

    def stringToken(self):
        string = ""
        while self.current_char is not None and self.current_char.isalpha():
            string += self.current_char
            self.advance()
        self.tokens.append({"type:": str, "value": string})


    def keyToken(self):
        string = ""
        while self.current_char is not None and self.current_char.isalpha() and self.current_char != " ":
            string += self.current_char
            self.advance()

        if string == "DECLARE":
            self.tokens.append({"type:": "KEYWORD", "value": string})

        self.tokens.append({"type:": str, "value": string})
