from parser import Parser

p = Parser("""

                DECLARE condition INITIALLY true
                WHILE condition = true DO
                    SET condition TO false
                    IF condition = true THEN
                        SET condition TO false
                    END IF

                    FOR index FROM 0 TO n-2 DO
                        SET condition TO false
                        SEND condition TO DISPLAY

                    END FOR

                    WHILE condition = false DO
                        SET condition TO true
                    END WHILE



                END WHILE

           """)

p.parse()

