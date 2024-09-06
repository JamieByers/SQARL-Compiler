from parser import Parser
from lexer import Tokeniser

p = Parser("""
           
            DECLARE hello INITIALLY "hello"
            SET hello TO "world"
            SET hello TO "worldddd!!!"
           """)

p.parse()

print(p.lexer.tokens)
print(p.statements)
