import json
from lexer import Tokeniser
from parser import Parser

p = Parser("""
              DECLARE variable INITIALLY "hello"
           """)


print(p.parse())
print(p.variables)
