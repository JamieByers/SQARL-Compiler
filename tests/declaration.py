from tests.general_test import Test

test = """
      DECLARE num INITIALLY AS INTEGER 4
"""

t = Test(
    test,
    test_name="declaration",
    test_type="code generator",
    print_tokens=True,
    print_ASTNodes=True
)

t.run(show_error_message=True)

print(t.parser.variables)
