import json
from parser import Parser
from lexer import Tokeniser


# parser = Parser("42")

# ast = parser.parse()

# print(json.dumps(ast))

#sample - DECLARE var = "hello":


lex = Tokeniser("""
                    DECLARE amount INITIALLY 3
                    IF amount <= 4 DO

                """)
lex.tokenise()

print(lex.tokens)
