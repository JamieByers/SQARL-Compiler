from tests.general_test import Test

test = """

    DECLARE func INITIALLY length(param1, )

    """

Test(
        test,
        test_name = "func calling",
        test_type = "code generator",
        print_tokens = True,
        print_ASTNodes = True

).run(show_error_message=True)
