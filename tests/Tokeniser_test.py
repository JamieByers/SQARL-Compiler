from lexer import Tokeniser

t = Tokeniser("""

                WHILE hello = "world" DO
                    SEND hello TO DISPLAY
                END WHILE

              """)

t.tokenise()

print(t.tokens)


