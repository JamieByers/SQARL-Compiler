from parser import Parser

p = Parser("""

                DECLARE condition INITIALLY true
                WHILE condition = true DO 
                    SET condition TO false
                    IF condition = true THEN
                        SET condition TO false
                    END IF
           
                    WHILE condition = false DO 
                        SET condition TO true
                    END WHILE
           
                END WHILE 
           
           """)

p.parse()

