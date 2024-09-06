from parser import Parser

p = Parser("""

                DECLARE condition INITIALLY true
                IF condition = true THEN
                    SET condition TO false
                    IF condition = false THEN
                        SET condition TO true
                        IF condition = true THEN
                            SET condition TO false
                        END IF
                    END IF
                END IF
           
           """)

p.parse()

