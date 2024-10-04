from classes import *

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.pos = 0
        self.current_node = self.ast[self.pos] if self.ast else None
        self.statements = []
        self.indent_level = 1

    def advance(self) -> None:
        self.pos += 1
        if self.pos <= len(self.ast)-1:
            print(self.pos, len(self.ast)-1)
            self.current_node = self.ast[self.pos]
        else:
            self.current_node = None

    def generate(self):
        while self.current_node:
            statement = self.match_node(self.current_node)
            self.statements.append(statement)
            self.advance()

        return self.statements

    def display(self):
        print()
        print("Generated Code: ")
        for statement in self.statements:
            print(statement)

    def write(self):
        with open("output.py", "w+") as file:
            for statement in self.statements:
                file.write(statement)

    def get_indent_level(self):
        return "    "*self.indent_level

    def parsed_block(self, block):
        code = ""
        self.indent_level += 1

        for statement in block:
            statement: str = self.get_indent_level() + self.match_node(statement)
            if "\n" not in statement:
                statement += "\n"

            code += statement

        self.indent_level -= 1

        return code

    def match_node(self, node) -> str:
        if node is None:
            node = self.current_node


        if node.type:
            node_types = {
                "VariableDeclaration": self.VariableDeclarationNode,
                "VariableAssignment": self.VariableAssignmentNode,
                "DisplayStatement": self.DisplayNode,
                "IfStatement": self.IfStatementNode,
                "ForStatement": self.ForStatementNode,
                "ForEachStatement": self.ForEachStatementNode,
                "WhileStatement": self.WhileStatementNode,
                "FunctionDeclaration": self.FunctionDeclarationNode,
                "FunctionCall": self.FunctionCallNode,
                "ReturnStatement": self.ReturnStatementNode,
                "Expression": self.ExpressionNode,
                "Array": self.ArrayNode,
            }
            return node_types[node.type](node)
        else:
            raise Exception("Current node has not type: ", self.current_node)

    def DisplayNode(self, node) -> str:
        return f"print({node.value})"

    def variable_values(self, identifier, value):
        if not isinstance(identifier, (str, int, float, bool)):
            identifier = self.match_node(identifier)

        if not isinstance(value, (str, int, float, bool)):
            value = self.match_node(value)

        return identifier, value

    def VariableDeclarationNode(self, node) -> str:
        identifier, value = self.variable_values(node.identifier, node.initial_value)

        return f"{identifier} = {value}"

    def VariableAssignmentNode(self, node) -> str:
        identifier, value = self.variable_values(self.identifier, self.value)

        return f"{identifier} = {value}"

    def IfStatementNode(self, node) -> str:
        code: str = ""

        if_line = f"if {node.condition.value}:\n"
        code += if_line
        code += self.parsed_block(node.code_block)

        if node.else_if_block:
            else_if_line = f"elif {node.else_if_block.condition.value}:\n"
            code += else_if_line
            elif_block = self.parsed_block(node.else_if_block.code_block)
            code += elif_block
        if node.else_block:
            code += "else: \n"
            else_block = self.parsed_block(node.else_block.code_block)
            code += else_block

        return code

    def ForStatementNode(self, node) -> str:
        code: str = ""

        for_line = f"for {node.variable} in range({node.start}, {node.step}, {node.end}): \n"
        code += for_line

        code_block = self.parsed_block(node.code_block)
        code += code_block

        return code

    def ForEachStatementNode(self, node) -> str:
        code: str = ""

        for_line = f"for {node.variable} in {node.loop_from}: \n"
        code += for_line

        code_block = self.parsed_block(node.code_block)
        code += code_block

        return code

    def WhileStatementNode(self, node) -> str:
        code: str = ""

        while_line = f"while {node.condition.value}: \n"
        code += while_line

        code_block = self.parsed_block(node.code_block)
        code += code_block

        return code

    def FunctionDeclarationNode(self, node) -> str:
        code: str = ""

        parameters = [f"{param.value}: {param.type}" for param in node.params]
        funcdec: str = f"def {node.name}({', '.join(parameters)}):\n"
        code += funcdec

        code_block = self.parsed_block(node.code_block)
        code += code_block

        return code

    def FunctionCallNode(self, node):
        return f"{node.identifier}({', '.join(node.params) if node.params else ''}){str(node.additional_context) if node.additional_context else ''}"

    def ReturnStatementNode(self, node) -> str:
        return f"return {str(node.value.value)}"

    def ExpressionNode(self, node):
        return str(node.value)

    def ArrayNode(self, node):
        return str(node)
