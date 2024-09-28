from classes import *

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.pos = 0
        self.current_node = self.ast[self.pos] if self.ast else None
        self.statements = []

    def advance(self):
        self.pos += 1
        if self.pos <= len(self.ast):
            self.current_node = self.ast[self.pos]
        else:
            self.current_node = None

    def generate(self):
        while self.current_node:
            node_type = self.match_node()


    def match_node(self):
        if self.current_node.type:
            node_types = {
                "VariableDeclaration": self.add_statement,
                "VariableAssignment": self.statement


            }
        else:
            raise Exception("Current node has not type: ", self.current_node)

    def add_statement(self):
        self.statements.append(self.current_node.code)

    def DisplayNode(self):
        return f"print({self.current_node.value})"

    def VariableDeclarationNode(self):
        return f"{self.current_node.identifier} = {self.current_node.initial_value}"

    def VariableAssignmentNode(self):
        return f"{self.current_node.identifier} = {self.current_node.value}"

    def IfStatementNode(self):
        code = ""

        if_line = f"if {self.current_node.condition}:\n"
        code += if_line
        code += self.current_node.code_block

        if self.current_node.else_if_block:
           code += self.current_node.else_if_block
        if self.current_node.else_block:
            code += self.current_node.else_block

        return code

    def ForStatementNode(self):
        pass
