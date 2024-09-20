from lexer import Tokeniser
from classes import *
from typing import List

class Parser:
    def __init__(self, string):
        self.lexer = Tokeniser(string)
        self.lexer.tokenise()
        self.pos = 0
        self.current_token = self.lexer.tokens[self.pos] if self.lexer.tokens else None
        self.statements = []
        self.AST_nodes = []
        self.indent_level = 0


    def advance(self, amount=1) -> None:
        self.pos += amount
        if self.pos >= len(self.lexer.tokens):
            self.current_token = None
        else:
            self.current_token = self.lexer.tokens[self.pos]

    def next_token(self):
        return self.lexer.tokens[self.pos+1]

    def expect(self, expected):
        if expected == self.lexer.tokens[self.pos+1].type:
            self.advance()
        else:
            print("ERROR UNEXPECTED TOKEN: ", self.lexer.tokens[self.pos+1], "EXPECTED ", expected)


    def display(self) -> None:
        for statement in self.statements:
            print(statement)



    def parse(self) -> List:
        while self.pos <= len(self.lexer.tokens) and self.current_token is not None:

            statement = self.statement()
            self.statements.append(statement)

        return self.statements

    def write(self) -> List:
        with open("output_file.py", "w+") as file:
            for statement in self.statements:
                file.write(statement)


    def statement(self):
        if self.current_token.type == "VARIABLE_DECLARATION":
            statement =  self.variable_declaration()
        elif self.current_token.type == "VARIABLE_ASSIGNMENT":
            statement = self.variable_assignment()
        elif self.current_token.type == "SUBPROGRAM":
            statement =  self.function_statement()
        elif self.current_token.type == "KEYWORD":
            if self.current_token.value == "IF":
                statement =  self.if_statement()
            if self.current_token.value == "FOR":
                statement =  self.for_statement()
            elif self.current_token.value == "WHILE":
                statement =  self.while_statement()
            elif self.current_token.value == "SEND":
                statement =  self.send_to_display_statement()
            elif self.current_token.value == "RETURN":
                statement =  self.return_statement()
        elif self.current_token.type == "KEYWORD_CONTINUED":
                if self.current_token.value == "ELSE IF":
                    statement = self.else_if_statement()
                elif self.current_token.value == "ELSE":
                    statement = self.else_statement()
        elif self.current_token.type == "END":
            self.advance()
        else:
            print("statement failed", self.current_token, self.pos)

        return statement

    def simple_statement(self) -> str:
        statement = ""
        while self.current_token is not None and self.current_token.type not in [ "KEYWORD", "END", "VARIABLE_ASSIGNMENT", "VARIABLE_DECLARATION", "ASSIGNMENT"]:
            statement += self.current_token.value
            self.advance()


        return statement

    def expression(self):

        print("running")
        overall_values = ["+", "-", "/", "*", "(", ")"]
        operator_values = ["+", "-", "/", "*"]
        def initialise_stacks():
            tokens = []
            operator_stack = []
            precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
            output_queue = []

            while self.current_token and self.current_token.type not in [ "KEYWORD", "END", "VARIABLE_ASSIGNMENT", "VARIABLE_DECLARATION", "ASSIGNMENT"]:
                token = self.current_token.value
                tokens.append(self.current_token)
                self.advance()

                if token not in overall_values:
                    output_queue.append(token)

                elif token in operator_values:
                    while operator_stack and operator_stack[-1] in operator_values and precedence[operator_stack[-1]] >= precedence[token]:
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)

                elif token == "(":
                    operator_stack.append(token)

                elif token == ")":
                    while operator_stack and operator_stack[-1] != "(":
                        output_queue.append(operator_stack.pop())
                    operator_stack.pop()

            while operator_stack:
                output_queue.append(operator_stack.pop())

            return output_queue

        def evaluate_stacks(output_queue):
            stack = []

            print('output_queue', output_queue)
            for t in output_queue:
                if t not in operator_values:
                    stack.append(t)

                else:
                    right = stack.pop()
                    left = stack.pop()

                    if t == "+":
                        stack.append(left + right)
                    elif t == "-":
                        stack.append(left - right)
                    elif t == "/":
                        stack.append(left / right)
                    elif t == "*":
                        if isinstance(left, str) and isinstance(right, (int, float)):
                            stack.append(left * int(right))  # Convert float to int for string multiplication
                        elif isinstance(right, str) and isinstance(left, (int, float)):
                            stack.append(right * int(left))

            return stack[0]

        output_queue = initialise_stacks()
        eval = evaluate_stacks(output_queue)

        # self.AST_nodes.append(Expression(type="Expression", value=eval))
        return eval


    def send_to_display_statement(self):
        self.advance()  # skip SEND
        to_print = ""
        while self.current_token.value != "TO":
            to_print += self.current_token.value
            self.advance()

        self.advance() # skip past DISPLAY

        code = f"print({to_print})"

        self.advance()
        return code


    def variable_declaration(self):
        def type_expectation(self, expect):
            if expect == "STRING" and self.lexer.tokens[self.pos+1].type == "PAREN":
                return True
            if expect == "INTEGER" and self.lexer.tokens[self.pos+1].isdigit():
                return True
            if expect == "REAl" and self.lexer.tokens[self.pos+1].isdigit():
                return True
            if expect == "BOOLEAN" and self.lexer.tokens[self.pos+1].value in ['TRUE', 'FALSE']:
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
        expected_type = None

        self.expect("IDENTIFIER")
        if self.current_token.type == 'IDENTIFIER':
            identifier = self.current_token.value

            self.expect('VARIABLE_DECLARATION')
            self.advance() # move up to var value
            if self.current_token.value != "AS":
                value = self.expression()
            else:
                self.expect("TYPE")
                if self.current_token.value in var_types and type_expectation(self.current_token['value']):
                    expected_type = self.current_token.value
                    self.expect("IDENTIFIER")
                    value = self.expression()
        else:
            print("EXPECTED IDENTIFIER")
            return False

        code = f"{identifier} = {value} \n"
        self.AST_nodes.append(VariableDeclaration(type="VariableDeclaration", name=identifier, initial_value = value, var_type=expected_type ))
        return code



    def variable_assignment(self):
        self.expect("IDENTIFIER")

        variable_identifier = self.simple_statement()

        self.advance() # skip past TO

        variable_value = self.simple_statement()

        statement = f"{variable_identifier} = {variable_value}\n"

        variable_value = str(variable_value)
        self.AST_nodes.append(VariableAssignment(type="VariableAssignment", name=variable_identifier, value=variable_value))
        return statement

    def condition(self):
        condition = ""
        while self.current_token.value not in ["DO", "THEN"]:
            c = self.current_token.value
            if c in ["AND", "OR"]:
                c = f" {c.lower()} "
            condition += c
            self.advance()

        self.AST_nodes.append(SimpleStatement(type="condition", value=condition))
        return condition

    def if_statement(self):
        self.advance() # move past if towards conidition
        condition = self.condition()


        code_block = self.parse_block()

        code = f"if {condition}:\n"
        code += code_block

        else_if_block = None
        else_block = None

        if self.current_token.value == "ELSE IF":
            else_if_block = self.else_if_statement()
        if self.current_token.value == "ELSE":
            else_block = self.else_statement()


        self.AST_nodes.append(IfStatement(type="IfStatement", condition=condition, code_block=code_block, else_block=else_block, else_if_block=else_if_block ))
        return code

    def else_if_statement(self):
        self.advance()
        condition = self.condition()

        code_block = self.parse_block()

        code = f"elif {condition}:\n"
        code += code_block

        return code

    def else_statement(self):
        self.advance()

        code_block = self.parse_block(skip_then=False)

        code = "else: \n"
        code += code_block

        return code

    def for_statement(self):
        self.advance()
        if self.current_token.type == "IDENTIFIER":
            for_loop_identifier = self.current_token.value
            self.expect("KEYWORD") # move to FROM
            self.advance() # move to starting index
            starting_index = self.current_token.value

            self.expect("ASSIGNMENT") # move to TO
            self.advance() # move to loop length
            loop_length = self.current_token.value

            self.advance()
            step_count = 1
            if self.current_token.value == "STEP":
                self.advance()
                step_count = self.current_token.value
                self.expect("BLOCK_START")


            for_block = self.parse_block()



            code = f"for {for_loop_identifier} in range({starting_index}, {loop_length}): \n"
            code += for_block

            self.AST_nodes.append(ForStatement(type="ForStatement", variable=for_loop_identifier, start=starting_index, end=loop_length, step=step_count, code_block=for_block))
            return code

        elif self.current_token.type == "KEYWORD":
            self.expect("IDENTIFIER")
            for_loop_identifier = self.current_token.value
            self.expect("KEYWORD")
            self.expect("IDENTIFIER")
            looping_from = self.current_token.value
            self.expect("BLOCK_START")


            for_code = self.parse_block()


            code = f"for {for_loop_identifier} in {looping_from}: \n"
            code += for_code

            self.AST_nodes.append(ForEachStatement(type="ForEachStatement", variable=for_loop_identifier, loop_from=looping_from, code_block=for_block))
            return code

        else:
            print("Error with for loop")


    def while_statement(self):
        self.advance() # skip past while
        condition = self.condition()

        code_block = self.parse_block()

        code = f"while {condition}:\n"
        code += code_block

        self.AST_nodes.append(WhileStatement(type="WhileStatement", condition=condition, code_block=code_block))
        return code


    def parse_block(self, skip_then=True):
        self.indent_level += 1
        if skip_then:
            self.advance() # skip past THEN

        block_statements = []
        while self.current_token.type not in ["END", "KEYWORD_CONTINUED"]:
            statement = self.statement()
            block_statements.append(statement)

        code = ""
        for statement in block_statements:
            if "\n" not in statement:
                code_line = self.get_indent_level() + statement + "\n"
            else:
                code_line = self.get_indent_level() + statement

            code += code_line

        if self.current_token.type == "END":
            self.advance() # end block

        self.indent_level -= 1
        return code

    def get_indent_level(self):
        return "    "*self.indent_level

    def get_params(self):
        self.expect("LPAREN")
        params = []
        while self.current_token.type != "RPAREN":
            if self.current_token.type == "IDENTIFIER":
                params.append(self.current_token.value)
            self.advance()

        return params

    def return_statement(self):
        self.advance() # skip RETURN
        returning = self.simple_statement()

        code = f"return {returning}"

        return code

    def function_statement(self):
        self.expect("IDENTIFIER")
        function_identifier = self.current_token.value
        params =  self.get_params()

        type_translation = {
            "STRING": "string",
            "CHARACTER": "string",
            "INTEGER": "int",
            "REAL": "float",
            "BOOLEAN": "bool",
            "ARRAY": "LIST",

        }

        expecting_type = False
        type_expected = None
        next_token = self.next_token()
        if next_token.value == "RETURNS":
            self.advance() # move past RETURNS
            expecting_type = True
            self.expect("TYPE")
            type_expected = self.current_token.value



        code_block = self.parse_block()

        if len(params) > 0:
            code = f"def {function_identifier}({' '.join(params)})"
        elif len(params) == 1:
            code = f"def {function_identifier}({params[0]})"
        else:
            code = f"def {function_identifier}()"

        if expecting_type:
            code += f" -> {type_translation[type_expected]}: \n"
        else:
            code += ":\n"


        code += code_block

        self.AST_nodes.append(FunctionDeclaration(type="FunctionDeclaration", name=function_identifier, params=params, code_block=code_block, return_type=type_expected))
        return code





