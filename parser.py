from lexer import Tokeniser

class Parser:
    def __init__(self, string):
        self.lexer = Tokeniser(string)
        self.lexer.tokenise()
        self.pos = 0
        self.current_token = self.lexer.tokens[self.pos] if self.lexer.tokens else None
        self.statements = []
        self.variables = {}
        self.indent_level = 0

    def advance(self, amount=1):
        self.pos += amount
        if self.pos >= len(self.lexer.tokens):
            self.current_token = None
        else:
            self.current_token = self.lexer.tokens[self.pos]


    def expect(self, expected):
        if expected == self.lexer.tokens[self.pos+1]["type"]:
            self.advance()
        else:
            print("ERROR UNEXPECTED TOKEN: ", self.lexer.tokens[self.pos+1], "EXPECTED ", expected)
            raise f"Expected: {expected}"

    def parse(self):
        while self.pos <= len(self.lexer.tokens) and self.current_token is not None:

            statement = self.statement()
            self.statements.append(statement)

        print(self.statements)
        return self.statements


    def statement(self):
        if self.current_token["type"] == "VARIABLE_DECLARATION":
            return self.variable_declaration()
        elif self.current_token["type"] == "VARIABLE_ASSIGNMENT":
            return self.variable_assignment()
        elif self.current_token["type"] == "KEYWORD":
            if self.current_token["value"] == "IF":
                return self.if_statement()
            elif self.current_token["value"] == "WHILE":
                return self.while_statement()
            elif self.current_token["value"] == "SEND":
                return self.send_to_display_statement()
        else:
            return

    def simple_statement(self):
        statement = ""
        while self.current_token is not None and self.current_token["type"] != "KEYWORD":
            statement += self.current_token["value"]
            self.advance()

        print(statement)
        return statement

    def send_to_display_statement(self):
        self.advance()  # skip SEND
        to_print = ""
        while self.current_token["value"] != "TO":
            to_print += self.current_token["value"]
            self.advance()

        self.advance() # skip past DISPLAY

        code = f"print({to_print})"

        self.advance()
        return code


    def variable_declaration(self):
        def type_expectation(self, expect):
            if expect == "STRING" and self.lexer.tokens[self.pos+1]["type"] == "PAREN":
                return True
            if expect == "INTEGER" and self.lexer.tokens[self.pos+1].isdigit():
                return True
            if expect == "REAl" and self.lexer.tokens[self.pos+1].isdigit():
                return True
            if expect == "BOOLEAN" and self.lexer.tokens[self.pos+1]['value'] in ['TRUE', 'FALSE']:
                return True

            return False

        var_types = [
            "INTEGER",
            "CHARARACTER",
            "REAL",
            "BOOLEAN",
            "ARRAY",
        ]
        var = ""
        identifier = ""
        value = ""

        self.expect("IDENTIFIER")
        if self.current_token['type'] == 'IDENTIFIER':
            var += self.current_token['value']
            self.variables[self.current_token['value']] = None
            identifier = self.current_token['value']

            self.expect('VARIABLE_DECLARATION')
            self.advance() # move up to var value
            if self.current_token['value'] != "AS":
                if self.current_token['type'] == "STRING":
                    var += (" = " + self.current_token['value'])
                    value = self.current_token['value']
                    self.advance()
                else:
                    var += (" = " + self.simple_statement())
                    value =self.simple_statement()
                    return var

            else:
                self.expect("TYPE")
                if self.current_token['value'] in var_types and type_expectation(self.current_token['value']):
                    self.expect("IDENTIFIER")
                    var += self.current_token['value']
                    value = self.current_token['value']
        else:
            print("EXPECTED IDENTIFIER")
            return False

        self.variables[identifier] = value
        code = f"{identifier} = {value}"
        return code



    def variable_assignment(self):
        self.expect("IDENTIFIER")
        if self.current_token["value"] in self.variables.keys():
            variable_identifier = self.current_token["value"]

            self.expect("ASSIGNMENT")
            self.advance()

            variable_value = self.current_token["value"]

            self.variables[variable_identifier] =  variable_value
            statement = variable_identifier + " = " + '"' + variable_value + '"'

            self.advance()
        return statement

    def condition(self):
        condition = ""
        while self.current_token["value"] not in ["DO", "THEN"]:
            condition += self.current_token["value"]
            self.advance()


        return condition

    def if_statement(self):
        self.advance() # move past if towards conidition
        condition = self.condition()

        self.indent_level += 1
        code_block = self.parse_block()
        self.indent_level -= 1


        code = f"if {condition}:\n"
        code += code_block

        print(code)

        self.advance() # end if statement
        return code

    def while_statement(self):
        self.advance() # skip past while
        condition = self.condition()

        self.indent_level += 1
        code_block = self.parse_block()
        self.indent_level -= 1

        code = f"while {condition}:\n"
        code += code_block

        print("code- ")
        print(code)

        self.advance() # end while statement
        return code


    def parse_block(self):
        self.advance() # skip THEN
        block_statements = []
        while self.current_token["type"] != "END":
            block_statements.append(self.statement())

        code = ""
        for statement in block_statements:
            code_line = self.get_indent_level() + statement + "\n"
            code += code_line


        return code

    def get_indent_level(self):
        return "    "*self.indent_level

