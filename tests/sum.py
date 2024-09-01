
from lexer import Tokeniser

lex = Tokeniser("""
                    DECLARE addition INITIALLY ((1 + 2) * 3 ) /4
                """)

lex.tokenise()

print(lex.tokens)
