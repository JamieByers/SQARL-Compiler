from lexer import Tokeniser

t = Tokeniser("""

        PROCEDURE func(param)
            DECLARE hello INITIALLY "hello"
        END PROCEDURE

        FUNCTION func(param)
            DECLARE example INITIALLY "test"
            RETURN example
        END FUNCTION

              """)


t.tokenise()

print(t.tokens)


