from tests.general_test import Test

test = """

      DECLARE variable INITIALLY 1+2/(3*4)
      DECLARE variable INITIALLY "hello"

"""

Test(
    test,
    test_name="declaration",
    test_type="parser",
    print_tokens=False,
    print_ASTNodes=True
).run(show_error_message=True)