from lexer import Tokeniser

t = Tokeniser("""

                DECLARE condition INITIALLY true
                IF condition = true THEN
                    SET condition TO false
                    SEND condition TO DISPLAY
                END IF

           """)

t.tokenise()

print(t.tokens)
