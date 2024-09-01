from lexer import Tokeniser

class Parser:
    def __init__(self, string):
        self.lexer = Tokeniser(string)
        self.lexer.tokenise()
        self.pos = 0
        self.current_token = self.lexer.tokens[self.pos] if self.lexer.tokens else None
        self.statements = []

    def advance(self, amount=1):
        self.pos += amount
        if self.pos >= len(self.lexer.tokens):
            self.current_token = None
        else:
            self.current_token = self.lexer.tokens[self.pos]

    def parse(self):
        while self.pos <= len(self.lexer.tokens) and self.current_token is not None:
            self.statements.append(self.statement())

        return self.statements


    def statement(self):
        if self.current_token["type"] == "VARIABLE_DECLARATION":
            self.variable_declaration()
        elif self.current_token["type"] == "VARIABLE_ASSIGNMENT":
            self.variable_assignment()

    def variable_declaration(self):
        var = {}
        var_type = ""
        var_types = [
            "INTEGER",
            "CHARARACTER",
            "REAL",
            "BOOLEAN",
            "ARRAY",
        ]
        self.advance()
        if self.current_token["value"]:
            var["identifier"] = self.current_token["value"]
            self.advance(2)
            if self.current_token["value"] == "AS":
                self.advance()
                if self.current_token["value"] in var_types:
                    var_type = self.current_token["value"]
                    self.advance()
                    var["value"] = self.current_token["value"]
                else:
                    print("ERROR: EXPECTED TYPE")
            else:
                var["value"] = self.current_token["value"]
                self.advance()

        print("VARIABLE: ", var)
        return var

    def variable_assignment(self):
        self.advance()

