from parser import Parser

p = Parser("""

                DECLARE condition INITIALLY true
                IF condition = true THEN
                    SET condition TO false
                    SEND "Hello World!" TO DISPlAY
                END IF

           """)

p.parse()
p.write()
