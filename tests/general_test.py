class Test:

    def __init__(self, string, test_type, test_name, print_tokens=False):
        self.string = string
        self.test_type = test_type
        self.passed = False
        self.print_tokens = print_tokens
        self.test_name = test_name

    def run(self, write=False, show_error_message=False,):
        from lexer import Tokeniser
        from parser import Parser

        try:
            if self.test_type == "tokeniser":
                    tokeniser = Tokeniser(self.string)
                    tokeniser.tokenise()
                    if self.print_tokens:
                        print("TOKENS: ", tokeniser.tokens)

                    self.passed = True
            elif self.test_type == "parser":
                    p = Parser(self.string)
                    if self.print_tokens:
                        print(p.lexer.tokens)

                    p.parse()
                    if write == True:
                        p.write()

                    self.passed = True

        except Exception as e:
            import traceback

            self.passed = False
            print(self.test_name, "failed")
            print("Failed test with error: ", e)
            if show_error_message:
                print(traceback.format_exc())


        return self.passed
