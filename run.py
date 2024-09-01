import json
from parser import Parser
from lexer import Tokeniser

p = Parser("""
                DECLARE variable INITIALLY "hello"
                DECLARE hello INITIALLY "world"
                DECLARE number INITIALLY 2
           """)

print("TOKENS: ", p.lexer.tokens)

p.parse()
