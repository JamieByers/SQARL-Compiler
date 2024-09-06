from lexer import Tokeniser 

t = Tokeniser("""

                DECLARE condition = true
                IF condition = true THEN
                    SET condition TO false
                END IF
           
           """)

t.tokenise()

print(t.tokens)