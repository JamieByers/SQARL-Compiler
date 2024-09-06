from parser import Parser

p = Parser("""

                DECLARE condition INITIALLY true
                WHILE condition = true DO 
                    SET condition TO false
                END WHILE 
           
           """)

p.parse()

