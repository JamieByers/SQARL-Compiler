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
        self.variables = {}


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
            if statement:
                self.statements.append(statement)

        return self.statements

    def write(self) -> None:
        with open("output_file.py", "w+") as file:
            for statement in self.statements:
                file.write(statement)


    def statement(self):
        statement = None
        if self.current_token:
            if self.current_token.type == "VARIABLE_DECLARATION":
                statement =  self.variable_declaration()
            elif self.current_token.type == "VARIABLE_ASSIGNMENT":
                statement = self.variable_assignment()
            elif self.current_token.type == "SUBPROGRAM":
                statement =  self.function_declaration()
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
            elif self.current_token.type == "EOF":
                self.current_token = None
                self.advance()
                return None
            else:
                print("statement failed", self.current_token, self.pos)

        return statement

    def simple_statement(self):
        statement = ""
        while self.current_token.type not in ["KEYWORD", "END", "VARIABLE_ASSIGNMENT", "VARIABLE_DECLARATION", "ASSIGNMENT", "EOF"]:
            statement += str(self.current_token.value)
            self.advance()

        return statement


    def expression(self):
        def check_if_array():
            if self.current_token.type == "LSQPAREN":
                return True
            return False

        def check_if_function_call():
            next_token = self.next_token()
            if self.current_token.type == "IDENTIFIER" and next_token.type == "LPAREN":
                return True
            return False

        def check_if_index_fetch():
            if self.current_token.type == "IDENTIFIER" and self.next_token().value == "[":
                return True

        def handleFunctionCall():
            # -- TODO -- add standard algorithms

            #missing ord chr random
            standard_algorithms = {
                "length": "len",
            }

            function_params: List[str] = []
            function_identifier = self.current_token.value
            if function_identifier in standard_algorithms.keys():
                function_identifier = standard_algorithms[function_identifier]

            self.expect("LPAREN")
            self.advance() # skip (
            while self.current_token.type != "RPAREN":
                if self.current_token.type == "COMMA":
                    self.advance()

                function_params.append(self.current_token.value)
                self.advance()

            self.advance() #skip )

            additional_context = self.simple_statement()

            code = f"{function_identifier}({''.join(function_params)})" + additional_context
            ast_node = FunctionCall(type="FunctionCall", idenitifer=function_identifier, params=function_params,value=code)
            ast_node.code = code
            return ast_node

        def handleArrayExp():
            self.advance() #skip past (
            array_elements = []
            while self.current_token.value != "]":
                if self.current_token.type == "COMMA":
                    self.advance()
                else:
                    array_elements.append(str(self.current_token.value))
                    self.advance()

            self.advance() #skip ]

            #f"[{', '.join([str(i) for i in array_elements])}]"
            el = ArrayElement(type="Array", elements=array_elements)
            return el

        def handleIndexFetch():

            fetch = ""
            identifier = self.current_token.value
            fetch += identifier

            self.expect("LSQPAREN")
            fetch += "["
            self.advance() #move past [

            index_values = []
            while self.current_token.value != "]":
                index_values.append(self.current_token.value)
                self.advance()

            # -- TODO -- create a small expression function that doesnt advance, or does just simply up until RSQparen, or add to current exp?
            fetch += "".join(index_values) #TEMPORARY FIX

            fetch += "]"
            self.advance() #move past ]

            exp = Expression(type="Expression", value=fetch)
            return exp



        def handleArithmaticExpression():
            overall_values = ["+", "-", "/", "*", "(", ")", "*", "^", "MOD"]
            operator_values = ["+", "-", "/", "*", "^", "MOD"]
            def initialise_stacks():
                tokens = []
                operator_stack = []
                precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "MOD": 2}
                output_queue = []

                while self.current_token and self.current_token.type not in ["KEYWORD", "END", "VARIABLE_ASSIGNMENT", "VARIABLE_DECLARATION", "ASSIGNMENT", "EOF"]:
                    token = self.current_token.value
                    tokens.append(self.current_token)
                    self.advance()

                    if token not in overall_values:
                        output_queue.append(token)

                    elif token in operator_values:

                        while operator_stack and operator_stack[-1] != "(" and precedence[operator_stack[-1]] >= precedence[token]:
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

                for t in output_queue:
                    if t not in operator_values:
                        stack.append(t)

                    else:
                        if len(stack) > 1:
                            right = stack.pop()
                            left = stack.pop()

                            if left in self.variables.keys():
                                left = self.variables[left]
                                if isinstance(left, (Expression)):
                                    left = left.value
                                    if not isinstance(left, (str, int, float)):
                                        left = str(left)
                            if right in self.variables.keys():
                                right = self.variables[right]
                                if isinstance(right, (Expression)):
                                    right = right.value
                                    if not isinstance(right,(str, int,float)):
                                        right = str(right)

                            print("leftright",left, right)

                            if t == "+":
                                if isinstance(left, (int,float)) and isinstance(right, (int, float)):
                                    stack.append(left + right)
                                else:
                                    stack.append(str(left) + str(right))
                            elif t == "-":
                                if isinstance(left, str) and isinstance(right, (int, float)):
                                    stack.append(left+"-"+str(right))
                                elif isinstance(right, str) and isinstance(left, (int, float)):
                                    stack.append(right+"-"+str(left))
                                elif isinstance(left, str) and isinstance(right, str):
                                    raise Exception(f"Cannot subtract two strings: {left}-{right}")
                                elif isinstance(left, (int,float)) and isinstance(right, (int,float)):
                                    stack.append(left - right)

                            elif t == "/":
                                if (left.isdigit == False or right.isdigit() == False):
                                    raise Exception(f"Cannot divide strings or other: {left}-{right}")
                                elif left.isdigit() and right.isdigit():
                                    stack.append(left / right)
                            elif t == "*":
                                if isinstance(left, str) and isinstance(right, (int, float)):
                                    stack.append(left * int(right))  # Convert float to int for string multiplication
                                elif isinstance(right, str) and isinstance(left, (int, float)):
                                    stack.append(right * int(left))
                                elif isinstance(left, (int,float)) and isinstance(right, (int,float)):
                                    stack.append(left * right)
                            elif t == "^":
                                stack.append(left ** right)
                            elif t == "MOD":
                                stack.append(left % right)

                return stack[0]

            output_queue = initialise_stacks()
            eval = evaluate_stacks(output_queue)
            exp = Expression(type="Expression", value=eval)
            # self.AST_nodes.append(Expression(type="Expression", value=eval))
            return exp



        is_array = check_if_array()
        is_function_call = check_if_function_call()
        is_array_fetch = check_if_index_fetch()

        if is_array:
            code = handleArrayExp()
        elif is_function_call:
            code = handleFunctionCall()
        elif is_array_fetch:
            code = handleIndexFetch()
        else:
            code = handleArithmaticExpression()

        return code

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

    def add_variable(self, identifier, value):
        self.variables[identifier] = value

    def variable_declaration(self):
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
                exact_value = value.value
            else:
                self.expect("TYPE")
                if self.current_token.type == "TYPE":
                    expected_type = self.current_token.value
                    self.advance()
                    value = self.expression()
                    exact_value = value.value
                else:
                    raise Exception("Expected a type definition")
        else:
            print("EXPECTED IDENTIFIER")
            return False

        code = f"{identifier} = {exact_value} \n"
        exp = VariableDeclaration(type="VariableDeclaration", idenitifer=identifier, initial_value = value, var_type=expected_type )
        exp.code = code
        self.AST_nodes.append(exp)
        self.add_variable(identifier, exact_value)

        return code



    def variable_assignment(self):
        self.expect("IDENTIFIER")

        variable_identifier = self.expression()

        self.advance() # skip past TO

        variable_value = self.expression()

        statement = f"{variable_identifier} = {variable_value}\n"
        self.add_variable(variable_identifier, variable_value)

        variable_value = str(variable_value)
        exp = VariableAssignment(type="VariableAssignment", idenitifer=variable_identifier, value=variable_value, )
        exp.code = statement.strip("\n")
        self.AST_nodes.append(exp)
        return statement

    def condition(self):
        condition = ""
        while self.current_token.value not in ["DO", "THEN"]:
            c = str(self.current_token.value)
            if c in ["AND", "OR"]:
                c = f" {c.lower()} "
            condition += c
            self.advance()

        return Condition(type="condition", value=condition)

    def if_statement(self):
        self.advance() # move past if towards conidition
        condition = self.condition()


        code_block = self.parse_block()

        code = f"if {condition}:\n"
        code += code_block

        else_if_block = ""
        else_block = ""

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

            self.AST_nodes.append(ForEachStatement(type="ForEachStatement", variable=for_loop_identifier, loop_from=looping_from, code_block=for_code))
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
        while self.current_token.type not in ["END", "KEYWORD_CONTINUED", "EOF"]:
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

        def checktype(val):
            types = [
                "CHAR",
                "STRING",
                "INTEGER",
                "REAL",
                "ARRAY",
                "OBJECT",
                "CLASS",
                "FUNCTION",
            ]

            if val in types:
                return True
            return False

        self.expect("LPAREN")
        self.advance() #skip (
        params = []
        while self.current_token.type != "RPAREN":
            if self.current_token.type == "TYPE":
                param = Parameter()
                if checktype(self.current_token.value):
                    param.type = self.current_token.value
                    self.expect("IDENTIFIER")
                    param.value = self.current_token.value
                    params.append(param)
                    self.advance()
                else:
                    raise Exception("TYPE EXPECTED FOR PARAM. ERROR AT TOKEN "+self.current_token)
            elif self.current_token.type == "COMMA":
                self.advance()

        return params

    def return_statement(self):
        self.advance() # skip RETURN
        returning = self.expression()

        code = f"return {returning}"

        return code

    def function_declaration(self):
        self.expect("IDENTIFIER")
        function_identifier = self.current_token.value
        params = self.get_params()

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
        param_identifiers = [param.value for param in params]

        if len(param_identifiers) > 0:
            code = f"def {function_identifier}({' '.join(param_identifiers)})"
        elif len(param_identifiers) == 1:
            code = f"def {function_identifier}({param_identifiers[0]})"
        else:
            code = f"def {function_identifier}()"

        if expecting_type and type_expected:
            code += f" -> {type_translation[type_expected]}: \n"
        else:
            code += ":\n"


        code += code_block

        self.AST_nodes.append(FunctionDeclaration(type="FunctionDeclaration", name=function_identifier, params=params, code_block=code_block, return_type=type_expected))
        return code






