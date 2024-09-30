from tests.general_test import Test

t = """

    DECLARE con INITIALLY 12
    WHILE con <= 12 DO
        SEND con TO DISPLAY
    END WHILE

"""

test = Test(
        t,
        test_name="while parsing",
        test_type="code generator",
        print_tokens=False,
        print_ASTNodes=False,
)
test.run()

