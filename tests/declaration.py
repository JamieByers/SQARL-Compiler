from tests.general_test import Test

test = """

      DECLARE var INITIALLY AS STRING "hello!"*3

"""

Test(
    test,
    test_name="declaration",
    test_type="parser",
    print_tokens=False,
    print_ASTNodes=True
).run(show_error_message=True)
