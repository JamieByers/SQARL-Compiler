from tests.general_test import Test

test = """

    IF condition = False THEN
        SEND "hello" TO DISPLAY
    ELSE IF condition = TRUE THEN
        SEND "world" TO DISPLAY
    ELSE
        SEND "test" TO DISPLAY
    END IF

    """

Test(
    test,
    test_name = "else if",
    test_type = "tokeniser",
    print_tokens = True,
).run()
