
from lexer import Tokeniser

t = Tokeniser("""
        SEND "Hello World!" TO DISPLAY
        SEND 'Hello World!' TO DISPLAY
           """)

t.tokenise()

print(t.tokens)
