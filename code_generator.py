class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.pos = 0
        self.current_node = self.ast[self.pos] if self.ast else None

    def advance(self):
        pass

    def generate(self):
        pass
