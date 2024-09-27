from tests.general_test import Test

test = """

      DECLARE var INITIALLY 7+3
      DECLARE v  INITIALLY 7-3
      DECLARE variable INITIALLY 7*3
      DECLARE variable2 INITIALLY 7/3

      SET v TO 17
"""

t = Test(
    test,
    test_name="declaration",
    test_type="parser",
    print_tokens=True,
    print_ASTNodes=True
)

t.run(show_error_message=True)

print(t.parser.variables)
