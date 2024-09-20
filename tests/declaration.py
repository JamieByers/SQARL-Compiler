from tests.general_test import Test

test = """

      DECLARE var INITIALLY "hello!"*3

"""

Test(
    test,
    test_name="declaration",
    test_type="parser",
    print_tokens=True,
    print_ASTNodes=True
).run(show_error_message=True)
