import json
from parser import Parser
from lexer import Tokeniser


# parser = Parser("42")

# ast = parser.parse()

# print(json.dumps(ast))

#sample - DECLARE var = "hello":


lex = Tokeniser("""
                DECLARE list INITIALLY [1,2,3]
                """)
lex.tokenise()

print(lex.tokens)
