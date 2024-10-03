from code_generator import CodeGenerator

class Test:

    def __init__(self, string, test_type, test_name, print_tokens=False, print_ASTNodes=False):
        from lexer import Tokeniser
        from parser import Parser
        self.string = string
        self.test_type = test_type
        self.passed = False
        self.print_tokens = print_tokens
        self.print_ASTNodes = print_ASTNodes
        self.test_name = test_name
        self.tokeniser = Tokeniser(self.string)
        self.parser = Parser(self.string)
        self.code_generator = None

    def run(self, display=True, write=False, show_error_message=False, write_ast=False):
        print("test -\n", self.string)
        try:
            self.tokeniser.tokenise()
            if self.print_tokens:
                print("TOKENS: ", self.tokeniser.tokens)

            if self.test_type == "parser":

                    if self.print_tokens:
                        print(self.parser.lexer.tokens)

                    self.parser.parse()

                    if display:
                        self.parser.display()

                    if self.print_ASTNodes:
                        print(self.parser.AST_nodes)

                    if write_ast == True:
                        tokens = self.parser.AST_nodes
                        with open("AST Nodes.py", "w") as file:
                            for token in tokens:
                                file.write(str(token)+"\n")

                    self.passed = True
            elif self.test_type == "code generator":
                self.parser.parse()
                self.code_generator = CodeGenerator(ast=self.parser.statements)
                self.code_generator.generate()

                if display:
                    self.code_generator.display()

                if write:
                    self.code_generator.write()

                self.passed = True


        except Exception as e:
            import traceback

            self.passed = False
            print(self.test_name, "failed")
            print("Failed test with error: ", e)
            if show_error_message:
                print(traceback.format_exc())


        return self.passed
