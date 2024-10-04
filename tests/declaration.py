from tests.general_test import Test

test = """
      DECLARE var INITIALLY AS ARRAY OF ARRAY [[]*2]
"""

t = Test(
    test,
    test_name="declaration",
    test_type="code generator",
    print_tokens=False,
    print_ASTNodes=True
)

t.run(show_error_message=True)

print(t.parser.variables)
