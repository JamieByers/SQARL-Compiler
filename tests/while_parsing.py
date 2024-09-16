from parser import Parser

p = Parser("""

                DECLARE condition INITIALLY true
                WHILE (condition = TRUE) AND (condition = TRUE) DO
                    SET condition TO false
                END WHILE

           """)

p.parse()

