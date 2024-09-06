from parser import Parser

p = Parser("""

                DECLARE sum INITIALLY (2+1)/3
                DECLARE test INITIALLY "hello"
           """)

p.parse()

