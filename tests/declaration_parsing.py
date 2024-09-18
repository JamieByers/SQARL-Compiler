from tests.general_test import Test

t = Test(
"""

    DECLARE words INITIALLY [1,2,3]

""",

    test_name = "declaration parsing",
    test_type = "parser",
    print_tokens = False,
    print_ASTNodes = True

)

t.run(show_error_message=True,)
