from parser import Parser

p = Parser("""

                IF condition = true THEN
                    SEND "Hello World!" TO DISPlAY
                END IF

           """)

p.parse()
p.write()
