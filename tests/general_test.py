class Test:

    def __init__(self, string, test_type, test_name, print_tokens=False):
        from lexer import Tokeniser
        from parser import Parser
        self.string = string
        self.test_type = test_type
        self.passed = False
        self.print_tokens = print_tokens
        self.test_name = test_name
        self.tokeniser = Tokeniser(self.string)
        self.parser = Parser(self.string)

    def run(self, write=False, show_error_message=False,):
        try:
            if self.test_type == "tokeniser":
                    self.tokeniser.tokenise()
                    if self.print_tokens:
                        print("TOKENS: ", self.tokeniser.tokens)

                    self.passed = True
            elif self.test_type == "parser":
                    if self.print_tokens:
                        print(self.parser.lexer.tokens)

                    self.parser.parse()
                    self.parser.display()
                    if write == True:
                        self.parser.write()

                    self.passed = True

        except Exception as e:
            import traceback

            self.passed = False
            print(self.test_name, "failed")
            print("Failed test with error: ", e)
            if show_error_message:
                print(traceback.format_exc())


        return self.passed
