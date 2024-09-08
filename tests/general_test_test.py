from tests.general_test import Test

t = Test(
    """
        DECLARE var INITIALLY "hello world!"
    """,
    test_type = "tokeniser",
    test_name = "general_test",
    print_tokens = True
)

t.run(True)


