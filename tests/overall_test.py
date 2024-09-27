from tests.general_test import Test

test = """
    DECLARE var INITIALLY 1
    DECLARE answer INITIALLY 1+var
    """

t = Test(
        test,
        test_name="overall test",
        test_type="parser",
        print_tokens=False,
        print_ASTNodes=False,
)

t.run(show_error_message=True)
print(t.parser.variables)
