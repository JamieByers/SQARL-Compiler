class Tokeniser:
    def __init__(self, string):
        self.pos = 0
        self.string = string.strip()
        self.current_char = self.string[self.pos] if self.string else None
        self.next_char = self.string[self.pos+1]
        self.tokens = []

    def advance(self):
        self.pos += 1
        if self.pos < len(self.string):
            self.current_char = self.string[self.pos]
        else:
            self.current_char = None

    def tokenise_normal(self):
        s = ""
        while self.current_char is not None and not self.current_char.isspace():
            if self.current_char in [",", "[", "]", "{", "}", "(", ")"]:
                self.match_token(self.current_char)
                self.advance()
            else:
                s += self.current_char
                self.advance()

        s = s.strip()
        self.match_token(s)
        return s

    def tokenise_quote(self):
        qs = ""
        self.advance()
        while self.current_char != '"' and self.current_char is not None:
            qs += self.current_char
            self.advance()

        self.advance()
        qs.strip()
        self.tokens.append({"type": "string", "value": qs})

    def tokenise_array(self):
        arr = ""
        self.advance()
        while self.current_char is not None and self.current_char != "]":
            if self.current_char.isspace():
                self.advance()
            else:
                arr += self.current_char
                self.advance()

        self.advance()
        self.tokens.append({"type": "ARRAY", "value": arr})

    def tokenise_paren(self):
        paren = ""
        self.advance()
        while self.current_char is not None and self.current_char != ")":
            if self.current_char.isspace():
                self.advance()
            else:
                paren += self.current_char
                self.advance()

        self.advance()
        self.tokens.append({"type": "PAREN", "value": paren})


    def next_token(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char != "":
            self.advance()

        print(self.current_char)
        if (self.current_char.isalpha() or self.current_char.isdigit()) and not self.current_char.isspace() and self.current_char is not None:
            self.tokenise_normal()
        elif self.current_char == '"':
            self.tokenise_quote()
        elif self.current_char == "[":
            # self.tokenise_array()
            self.match_token("[")
        elif self.current_char == "]":
            self.match_token("]")
        elif self.current_char == "(":
            # self.tokenise_paren()
            self.match_token("(")
        elif self.current_char == ")":
            self.match_token(")")
        elif self.current_char == ",":
            self.match_token(",")

        else:
            self.advance()

    def match_token(self, token):
        print("TOKEN", token)
        token_types_matched = {
            "DECLARE": "KEYWORD",
            "AS": "KEYWORD",
            "INTEGER": "TYPE",
            "REAL": "TYPE",
            "BOOLEAN": "TYPE",
            "CHARACTER": "TYPE",
            "INITIALLY": "KEYWORD",
            "true": "BOOLEAN",
            "false": "BOOLEAN",
            "[": "LSQPAREN",
            "]": "RSQPAREN",
            "{": "LCPAREN",
            "}": "RCPAREN",
            "(": "LPAREN",
            ")": "RPAREN",
            ",": "COMMA",
        }

        self.advance()

        if token in token_types_matched.keys():
            t = {"type": token_types_matched[token], "value": token}
            self.tokens.append(t)
            return t

        if token.isdigit():
            t = {"type": "NUMBER", "value": token}
            self.tokens.append(t)
            return t

        return {"type": "IDENTIFIER", "value": token}


    def tokenise(self):
        while self.current_char is not None:
            self.next_token()

        return self.tokens

