from typing import List
from lexer import Tokeniser
from classes import *


class Parser:
    def __init__(self, string):
        self.lexer = Tokeniser(string)
        self.lexer.tokenise()
        self.pos = 0
        self.current_token = (
            self.lexer.tokens[self.pos] if self.lexer.tokens else None
        )
        self.statements = []
        self.AST_nodes = []
        self.indent_level = 0
        self.variables = {}



    def parser_error(self, error_message, error_type=None):
        if error_message:
            print("Parser Failed at Token: ", self.current_token, )
            print("Token before: ", self.lexer.tokens[self.pos-1] )
            print("Parser Failed at Position: ", self.pos)
            print()
            if error_type:
                raise Exception(error_type, error_message)
            else:
                raise Exception(error_message)


    def stand_out(self, message):
        print()
        print(message)
        print()

    def around(self, message=None):
        if message:
            print(message)
        print("Before: ", self.lexer.tokens[self.pos-1])
        print("Current: ", self.lexer.tokens[self.pos])
        print("After: ", self.lexer.tokens[self.pos+1])

    def advance(self, amount=1) -> None:
        if self.current_token:
            self.pos += amount
            if self.pos >= len(self.lexer.tokens):
                self.current_token = None
            else:
                self.current_token = self.lexer.tokens[self.pos]

    def next_token(self):
        return self.lexer.tokens[self.pos + 1]

    def expect(self, expected):
        if self.pos < len(self.lexer.tokens) and expected == self.lexer.tokens[self.pos + 1].type:
            self.advance()
        elif self.pos >= len(self.lexer.tokens):
                self.current_token = None
        else:
            print(
                "ERROR UNEXPECTED TOKEN: ",
                self.lexer.tokens[self.pos + 1],
                "EXPECTED ",
                expected,
            )

    def display(self) -> None:
        for statement in self.statements:
            print(statement)

    def parse(self) -> List:
        while self.current_token is not None and self.pos <= len(self.lexer.tokens):
            statement = self.statement()
            if statement:
                self.statements.append(statement)

        print(self.statements)
        return self.statements


    def statement(self):
        statement_types = {
            "VARIABLE_DECLARATION": self.variable_declaration,
            "VARIABLE_ASSIGNMENT": self.variable_assignment,
            "KEYWORD": self.keyword,
            "KEYWORD_CONTINUED": self.keyword_continued,
            "SUBPROGRAM": self.function_declaration,
        }


        if self.current_token and self.current_token.type in statement_types:
            return statement_types[self.current_token.type]()
        elif self.current_token and self.current_token.type == "END":
            self.advance()
        elif self.current_token and self.current_token.type == "EOF":
            self.current_token = None
            self.advance()
            return None
        else:
            self.parser_error("Token not recognised")

    def keyword(self):
        keyword_types = {
            "IF": self.if_statement,
            "FOR": self.for_statement,
            "WHILE": self.while_statement,
            "SEND": self.send_to_display_statement,
            "RETURN": self.return_statement,
        }

        if self.current_token and self.current_token.value in keyword_types:
            return keyword_types[self.current_token.value]()
        else:
            self.parser_error(error_message=f"Keyword token does not match keyword types: {self.current_token}", error_type=KeyError)

    def keyword_continued(self):
        keyword_cont_types = {
            "ELSE": self.else_statement,
            "ELSE IF": self.else_if_statement,
        }
        return keyword_cont_types[self.current_token.value]

    def simple_statement(self):
        statement = ""
        while self.current_token and self.current_token.type not in [
            "KEYWORD",
            "END",
            "VARIABLE_ASSIGNMENT",
            "VARIABLE_DECLARATION",
            "ASSIGNMENT",
            "EOF",
        ]:
            statement += str(self.current_token.value)
            self.advance()

        return statement

    def handleArithmaticExpression(self):
        overall_values = ["+", "-", "/", "*", "(", ")", "*", "^", "MOD"]
        operator_values = ["+", "-", "/", "*", "^", "MOD"]

        def initialise_stacks():
            tokens = []
            operator_stack = []
            precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "MOD": 2}
            output_queue = []

            while self.current_token and self.current_token.type not in TokenConstants.keywords:
                if self.current_token and self.current_token.type == "IDENTIFIER" and self.next_token().type == "LPAREN":
                    function_call = self.handleFunctionCall().value
                    output_queue.append(function_call)
                    tokens.append(function_call)

                else:
                    token = self.current_token.value
                    tokens.append(self.current_token)
                    self.advance()


                    if token not in overall_values:
                        output_queue.append(token)

                    elif token in operator_values:

                        while (
                            operator_stack
                            and operator_stack[-1] != "("
                            and precedence[operator_stack[-1]] >= precedence[token]
                        ):
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
                                if not isinstance(right, (str, int, float)):
                                    right = str(right)

                        if t == "+":
                            if isinstance(left, (int, float)) and isinstance(
                                right, (int, float)
                            ):
                                stack.append(left + right)
                            else:
                                stack.append(str(left) + str(right))
                        elif t == "-":
                            if isinstance(left, str) and isinstance(
                                right, (int, float)
                            ):
                                stack.append(left + "-" + str(right))
                            elif isinstance(right, str) and isinstance(
                                left, (int, float)
                            ):
                                stack.append(right + "-" + str(left))
                            elif isinstance(left, str) and isinstance(right, str):
                                self.parser_error(error_message=f"Cannot subtract two strings: {left}-{right}")
                            elif isinstance(left, (int, float)) and isinstance(
                                right, (int, float)
                            ):
                                stack.append(left - right)

                        elif t == "/":
                            if (
                                isinstance(left, (int, float)) is False
                                or isinstance(right, (int, float)) is False
                            ):
                                self.parser_error(error_message=f"Cannot divide strings or other: {left}-{right}")

                            elif isinstance(left, (int, float)) and isinstance(
                                right, (int, float)
                            ):
                                stack.append(left / right)
                        elif t == "*":
                            if isinstance(left, str) and isinstance(
                                right, (int, float)
                            ):
                                stack.append(
                                    left * int(right)
                                )  # Convert float to int for string multiplication
                            elif isinstance(right, str) and isinstance(
                                left, (int, float)
                            ):
                                stack.append(right * int(left))
                            elif isinstance(left, (int, float)) and isinstance(
                                right, (int, float)
                            ):
                                stack.append(left * right)
                        elif t == "^":
                            stack.append(left**right)
                        elif t == "MOD":
                            stack.append(left % right)

            return stack[0]

        output_queue = initialise_stacks()
        eval = evaluate_stacks(output_queue)
        exp = Expression(type="Expression", value=eval, )
        return exp

    def handleFunctionCall(self):

        def handleStandardAlgorithmValue(identifier, params):

            standard_algorithms = TokenConstants.standard_algorithms

            if identifier in standard_algorithms:
                identifier = standard_algorithms[identifier]
            else:
                return None

            if identifier == "len" and len(params) == 1:
                return len(params[0])

            return None

        def handleStandardAlgorithmIdentifier(identifier):
            if identifier in TokenConstants.standard_algorithms:
                identifier = TokenConstants.standard_algorithms[identifier]

            return identifier

        function_params: List[str] = []
        function_identifier = self.current_token.value

        self.expect("LPAREN")
        self.advance()  # skip (
        while self.current_token and self.current_token.type != "RPAREN":
            if self.current_token and self.current_token.type == "COMMA":
                self.advance()

            function_params.append(self.current_token.value)
            self.advance()

        self.advance()  # skip )

        value = handleStandardAlgorithmValue(function_identifier, function_params)
        additional_context = self.simple_statement()


        if value is None:
            return Expression(
                type="Expression",
                value = value,
            )
        else:
            value = f"{function_identifier}({', '.join(function_params) if function_params else ''})"+additional_context

        function_identifier = handleStandardAlgorithmIdentifier(function_identifier)
        ast_node = FunctionCall(
            type="FunctionCall",
            identifier=function_identifier,
            params=function_params,
            additional_context=additional_context,
            value=value
        )
        return ast_node


    def expression(self):
        def check_if_array():
            if self.current_token and self.current_token.type == "LSQPAREN":
                return True
            return False

        def check_if_function_call():
            next_token = self.next_token()
            if self.current_token and self.current_token.type == "IDENTIFIER" and next_token.type == "LPAREN":
                return True
            return False

        def check_if_index_fetch():
            if (
                self.current_token.type == "IDENTIFIER"
                and self.next_token().value == "["
            ):
                return True

        def parseArray(nested_array=[]):
            while self.current_token and self.current_token.value != "]":
                if self.current_token and self.current_token.type == "COMMA":
                    self.advance()
                elif self.current_token and self.current_token.value == "[":
                    # Recursive call to handle nested arrays
                    self.advance()
                    nested_array.append(parseArray(nested_array))
                elif self.current_token and self.current_token.type == "MATH_TERM":
                    # Handle array multiplication
                    self.advance()  # skip *
                    repeat_count = int(self.current_token.value)
                    last_element = nested_array[-1]
                    nested_array.extend([last_element] * (repeat_count - 1))
                    self.advance()  # skip the number
                else:
                    nested_array.append(str(self.current_token.value))
                    self.advance()

            self.advance()  # skip ]
            return nested_array

        def handleArrayExp():
            array_elements = []

            self.around("before parse")
            parseArray(array_elements)

            return ArrayElement(type="Array", elements=array_elements, value=str(array_elements))



        def handleIndexFetch():

            fetch = ""
            identifier = self.current_token.value
            fetch += identifier

            self.expect("LSQPAREN")
            fetch += "["
            self.advance()  # move past [

            index_values = []
            while self.current_token.value != "]":
                index_values.append(self.current_token.value)
                self.advance()

            # -- TODO -- create a small expression function that doesnt advance, or does just simply up until RSQparen, or add to current exp?
            fetch += "".join(index_values)  # TEMPORARY FIX

            fetch += "]"
            self.advance()  # move past ]

            exp = Expression(type="Expression", value=fetch, )
            return exp



        is_array = check_if_array()
        is_function_call = check_if_function_call()
        is_array_fetch = check_if_index_fetch()

        if is_array:
            el = handleArrayExp()
        elif is_function_call:
            el = self.handleFunctionCall()
        elif is_array_fetch:
            el = handleIndexFetch()
        else:
            el = self.handleArithmaticExpression()

        return el

    def send_to_display_statement(self):
        self.advance()  # skip SEND
        to_print: str = ""
        while self.current_token and self.current_token.value != "TO":
            to_print += self.current_token.value
            self.advance()

        self.advance()  # skip past DISPLAY


        self.advance()
        exp = DisplayStatement(type="DisplayStatement", value=to_print, )
        return exp

    def add_variable(self, identifier, value):
        self.variables[identifier] = value

    def handle_type(self):
        if self.current_token.value == "ARRAY":
            self.advance()
            if not self.current_token.type == "TYPE_CONNECTOR":
                return []
            else:
                arr = []
                while self.current_token.type == "TYPE_CONNECTOR":
                    self.advance() #move past of
                    if self.current_token.value == "ARRAY":
                        arr.append([None])

                    self.advance() #either move past type or move to OR

                return arr


    def variable_declaration(self):
        identifier = ""
        value = ""
        expected_type = None

        self.expect("IDENTIFIER")
        if self.current_token and self.current_token.type == "IDENTIFIER":
            identifier = self.expression()

            self.advance()  # move up to var value
            if self.current_token and self.current_token.value != "AS":
                value = self.expression()
            else:
                self.expect("TYPE")
                if self.current_token and self.current_token.type == "TYPE":
                    expected_type = self.handle_type()
                    self.advance()
                    value = self.expression()
                else:
                    self.parser_error(error_message="Expected a type definition")
        else:
            print("EXPECTED IDENTIFIER")
            return False

        exp = VariableDeclaration(
            type="VariableDeclaration",
            identifier=identifier,
            initial_value=value,
            var_type=expected_type,
        )
        self.add_variable(identifier.value, value.value)

        return exp

    def variable_assignment(self):
        self.expect("IDENTIFIER")

        variable_identifier = self.expression()
        variable_identifier_value = variable_identifier.value

        self.advance()  # skip past TO

        variable_value = self.expression()
        variable_value_value = variable_value.value

        self.add_variable(variable_identifier_value, variable_value_value)

        exp = VariableAssignment(
            type="VariableAssignment",
            identifier=variable_identifier,
            value=variable_value,
        )
        self.AST_nodes.append(exp)
        return exp

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
        self.advance()  # move past if towards conidition
        condition = self.condition()

        code_block = self.parse_block()



        else_if_block = None
        else_block = None

        if self.current_token and self.current_token.value == "ELSE IF":
            else_if_block = self.else_if_statement()
        if self.current_token and self.current_token.value == "ELSE":
            else_block = self.else_statement()

        el = IfStatement(
                type="IfStatement",
                condition=condition,
                code_block=code_block,
                else_block=else_block,
                else_if_block=else_if_block,
            )

        return el

    def else_if_statement(self):
        self.advance()
        condition = self.condition()

        code_block = self.parse_block()

        el = ElifElement(type="ElifElement", condition=condition, code_block=code_block)

        return el

    def else_statement(self):
        self.advance()

        code_block = self.parse_block(skip_then=False)


        el = ElseElement(type="ElseElement", code_block=code_block)
        return el

    def for_statement(self):
        self.advance()
        if self.current_token and self.current_token.type == "IDENTIFIER":
            for_loop_identifier = self.current_token.value
            self.expect("KEYWORD")  # move to FROM
            self.advance()  # move to starting index
            starting_index = self.current_token.value

            self.expect("ASSIGNMENT")  # move to TO
            self.advance()  # move to loop length
            loop_length = self.current_token.value

            self.advance()
            step_count: int = 1
            if self.current_token and self.current_token.value == "STEP":
                self.advance()
                step_count = self.current_token.value
                self.expect("BLOCK_START")

            for_block = self.parse_block()

            el = ForStatement(
                    type="ForStatement",
                    variable=for_loop_identifier,
                    start=starting_index,
                    end=loop_length,
                    step=step_count,
                    code_block=for_block,
                )

            return el

        elif self.current_token and self.current_token.value == "EACH":
            self.expect("IDENTIFIER")
            for_loop_identifier = self.current_token.value
            self.expect("KEYWORD")
            self.expect("IDENTIFIER")
            looping_from = self.current_token.value
            self.expect("BLOCK_START")

            for_code = self.parse_block()

            el = ForEachStatement(
                    type="ForEachStatement",
                    variable=for_loop_identifier,
                    loop_from=looping_from,
                    code_block=for_code,
                )

            return el

        else:
            print("Error with for loop")

    def while_statement(self):
        self.advance()  # skip past while
        condition = self.condition()

        code_block = self.parse_block()


        el = WhileStatement(
                type="WhileStatement", condition=condition, code_block=code_block,
            )
        return el

    def parse_block(self, skip_then=True):
        self.indent_level += 1
        if skip_then:
            self.advance()  # skip past THEN

        block_statements = []
        while self.current_token and self.current_token.type not in ["END", "KEYWORD_CONTINUED", "EOF"]:
            statement = self.statement()
            block_statements.append(statement)


        if self.current_token and self.current_token.type == "END":
            self.advance()  # end block

        self.indent_level -= 1
        return block_statements

    def get_indent_level(self):
        return "    " * self.indent_level

    def get_params(self):

        def checktype(val):
            if val in TokenConstants.types:
                return True
            return False

        def translate_type(t):
            if t in TokenConstants.type_translator:
                return TokenConstants.type_translator[t]
            else:
                self.parser_error(error_type=TypeError, error_message=f"parameter type does not exist: {t}")

        self.expect("LPAREN")
        self.advance()  # skip (
        params = []
        while self.current_token.type != "RPAREN":
            if self.current_token and self.current_token.type == "TYPE":
                param = Parameter(value="", type="")
                if checktype(self.current_token.value):
                    param.type = translate_type(self.current_token.value)
                    self.expect("IDENTIFIER")
                    param.value = self.current_token.value
                    params.append(param)
                    self.advance()
                else:
                    self.parser_error(error_message=("TYPE EXPECTED FOR PARAM. ERROR AT TOKEN " + self.current_token))
            elif self.current_token and self.current_token.type == "COMMA":
                self.advance()

        return params

    def return_statement(self):
        self.advance()  # skip RETURN
        returning = self.expression()

        el = ReturnStatement(type="ReturnStatement", value=returning)

        return el

    def function_declaration(self):
        self.expect("IDENTIFIER")
        function_identifier = self.current_token.value
        params = self.get_params()
        type_expected = None
        next_token = self.next_token()
        if next_token.value == "RETURNS":
            self.advance()  # move past RETURNS
            self.expect("TYPE")
            type_expected = self.current_token.value
            type_expected = TokenConstants.type_translator[self.current_token.value]

        code_block = self.parse_block()

        el = FunctionDeclaration(
                type="FunctionDeclaration",
                name=function_identifier,
                params=params,
                code_block=code_block,
                return_type=type_expected,
                returning_type=type_expected
            )

        return el
