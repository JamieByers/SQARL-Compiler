from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Token:
    type: str
    value: str

class Tokeniser:
    def __init__(self, string: str):
        self.pos = 0
        self.string = string.strip()
        self.current_char = self.string[self.pos] if self.string else None
        self.tokens = []

    def advance(self, amount=1) -> None:
        self.pos += amount
        if self.pos < len(self.string):
            self.current_char = self.string[self.pos]
        else:
            self.current_char = None

    def next_char(self) -> str:
        return self.string[self.pos+1]

    def tokenise_key(self) -> str:
        k = ""
        while self.current_char is not None and not self.current_char.isspace():
            k += self.current_char
            self.advance()

        return k

    def tokenise_key_without_advance(self) -> str:
        k = ""
        pos  = self.pos + 1
        curr_char = self.string[pos]
        while curr_char is not None and not curr_char.isspace():
            k += curr_char
            pos += 1
            curr_char = self.string[pos]

        return k

    def skip_token(self) -> str:
        skipping = ""
        while self.current_char.isspace():
            self.advance()
        while self.current_char is not None and not self.current_char.isspace():
            skipping += self.current_char
            self.advance()


    def tokenise_normal(self) -> str:
        s = ""
        while self.current_char is not None and not self.current_char.isspace() and self.current_char not in ["(", ")", "[", "]", "{", "}"]:
            s += self.current_char
            self.advance()

        s = s.strip()
        self.check_token(s)
        return s

    def tokenise_number(self) -> Token:
        n = ""
        while self.current_char is not None and self.current_char.isdigit() and not self.current_char.isspace():
           n += self.current_char
           self.advance()

        n = float(n)
        token = Token("NUMBER", n)
        self.tokens.append(token)
        return token


    def tokenise_quote(self) -> Token:
        qs = ""
        self.advance()
        while self.current_char != '"' and self.current_char != "'" and self.current_char is not None:
            qs += self.current_char
            self.advance()

        qs = '"' + qs + '"'

        self.advance()
        qs.strip()
        token = Token("STRING", qs)
        self.tokens.append(token)
        return token


    def next_token(self) -> Token:
        while self.current_char is not None and self.current_char.isspace() and self.current_char != "":
            self.advance()

        if self.current_char.isalpha() and not self.current_char.isspace() and self.current_char is not None:
            return self.tokenise_normal()
        if self.current_char is not None and self.current_char.isdigit() and not self.current_char.isspace():
            return self.tokenise_number()
        elif self.current_char == '"' or self.current_char == "'":
            return self.tokenise_quote()
        elif self.current_char in ["[", "]", "(", ")", "{", "}", ",", "+", "-", "*", "/", "<", ">", "="]:
            return self.match_token(self.current_char)

        else:
            self.advance()

    def check_token(self, token: str) -> Token:
        if token == "<"  and self.next_char() == "=":
            token = Token("LESS_THAN_OR_EQUAL", token+"=")
            token = self.tokens.append(token)
            self.advance(2)
            return token
        elif token == ">" and self.next_char() == "=":
            token = Token("MORE_THAN_OR_EQUAL", token+"=")
            token = self.tokens.append(token)
            self.advance(2)
            return token

        if token == "=":
            token = Token("COMPARITOR", " == ")
            token = self.tokens.append(token)
            self.advance()
            return token

        if token == "ELSE":
            if self.tokenise_key_without_advance() == "IF":
                self.skip_token()

                token = Token("KEYWORD_CONTINUED", "ELSE IF")
                self.tokens.append(token)
                return token


        token_types_matched = {
            "DECLARE": "VARIABLE_DECLARATION",
            "SET": "VARIABLE_ASSIGNMENT",
            "AS": "KEYWORD",
            "INTEGER": "TYPE",
            "REAL": "TYPE",
            "BOOLEAN": "TYPE",
            "CHARACTER": "TYPE",
            "ARRAY": "TYPE",
            "STRING": "TYPE",
            "OF": "TYPE_CONNECTOR",
            "INITIALLY": "VARIABLE_DECLARATION",
            "SEND": "KEYWORD",
            "TO": "ASSIGNMENT",
            "DISPLAY": "KEYWORD",
            "TRUE": "BOOLEAN",
            "FALSE": "BOOLEAN",
            ">": "GREATER_THAN",
            "<": "LESS_THAN",
            "=": "EQUAL_TO",
            "[": "LSQPAREN",
            "]": "RSQPAREN",
            "{": "LCPAREN",
            "}": "RCPAREN",
            "(": "LPAREN",
            ")": "RPAREN",
            ",": "COMMA",
            "+": "MATH_EXPR",
            "-": "MATH_EXPR",
            "*": "MATH_TERM",
            "/": "MATH_TERM",
            "WHILE": "KEYWORD",
            "DO": "BLOCK_START",
            "END": "KEYWORD",
            "IF": "KEYWORD",
            "ELSE": "KEYWORD_CONTINUED",
            "FOR": "KEYWORD",
            "EACH": "KEYWORD",
            "FROM": "KEYWORD",
            "THEN": "BLOCK_START",
            "PROCEDURE": "SUBPROGRAM",
            "FUNCTION": "SUBPROGRAM",
            "RETURN": "KEYWORD",
            "RETURNS": "KEYWORD",
            "CLASS": "OBJECT",
            "CONSTRUCTOR": "CONSTRUCTOR",
            "THIS": "THIS",
            "OVERRIDE": "SUBPROGRAM",
        }

        if token in token_types_matched.keys():
            if token in ["TRUE", "FALSE"]:
                t = Token("BOOLEAN", token.lower().capitalize())

                self.tokens.append(t)
                return t

            elif token == "END":
                self.advance()
                next = self.tokenise_key()
                if next == "IF":
                    t = Token(type= "END", value= "END IF")
                elif next == "WHILE":
                    t = Token(type= "END", value= "END WHILE")
                elif next == "PROCEDURE":
                    t = Token(type= "END", value= "END PROCEDURE")
                elif next == "FUNCTION":
                    t = Token(type= "END", value= "END FUNCTION")
                elif next == "FOR":
                    t = Token(type= "END", value= "END FOR")
                    # self.advance()
                    next = self.tokenise_key()
                    if next == "EACH":
                        t = Token(type= "END", value= "END FOR EACH")

                self.tokens.append(t)
                return t

            t = Token(type= token_types_matched[token], value= token)
            self.tokens.append(t)
            return t

        token = Token("IDENTIFIER", token)
        self.tokens.append(token)
        return token

    def match_token(self, token: str) -> None:
        if not token:
            token = self.current_char

        self.check_token(token)
        self.advance()

    def tokenise(self) -> List[Token]:
        while self.current_char is not None:
            self.next_token()

        return self.tokens

