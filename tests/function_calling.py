from tests.general_test import Test

test = """

    DECLARE param1 INITIALLY [1,2,3]
    DECLARE func INITIALLY length(param1)+1/3

    """

Test(
        test,
        test_name = "func calling",
        test_type = "code generator",
        print_tokens = False,
        print_ASTNodes = False

).run(show_error_message=True)
