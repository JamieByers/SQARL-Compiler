from tests.general_test import Test

test = """

    DECLARE func INITIALLY function(param1, param2)


    """

Test(
        test,
        test_name = "func calling",
        test_type = "parser",
        print_tokens = False,
        print_ASTNodes = True

).run(show_error_message=True)
