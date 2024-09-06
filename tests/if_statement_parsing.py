from parser import Parser

p = Parser("""

                DECLARE condition INITIALLY true
                IF condition = true THEN
                    SET condition TO false
                    DECLARE test_variable INITIALLY "testing"
                    SET test_variable TO "TEST"
                END IF
           
           """)

p.parse()

