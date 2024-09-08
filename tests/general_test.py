class Test:
    def __init__(self, string, test_type, test_name, print_tokens=False):
        self.string = string
        self.test_type = test_type
        self.passed = False
        self.print_tokens = print_tokens
        self.test_name = test_name

    def run(self, show_error_message=False):
        from lexer import Tokeniser
        from parser import Parser

        try:
            if self.test_type == "tokeniser":
                    t = Tokeniser(self.string)
                    t.tokenise()
                    if self.print_tokens:
                        print(t.tokens)

                    self.passed = True
            elif self.type == "parser":
                    p = Parser(self.string)
                    p.parse()
                    if self.print_tokens:
                        print(p.lexer.tokens)

                    self.passed = True

        except Exception as e:
            self.passed = False
            print(self.test_name, "failed")
            if show_error_message:
                print("Failed test with error: ", e)

        return self.passed
