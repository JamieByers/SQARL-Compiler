from parser import Parser

p = Parser("""

        SEND "Hello World!" TO DISPLAY
        SEND 'Hello World!' TO DISPLAY
           """)

p.parse()

