from lexer import Tokeniser

lexer = Tokeniser("""
                        DECLARE var INITIALLY "Hello World!"
                        DECLARE one INITIALLY 1
                        DECLARE two INITIALLY 2
                        DECLARE addition INITIALLY (1 + 2)
                  """)

lexer.tokenise()

print(lexer.tokens)
