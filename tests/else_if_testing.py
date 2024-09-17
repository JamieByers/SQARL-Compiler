from tests.general_test import Test

test = """

    IF condition = FALSE THEN
        SEND "hello" TO DISPLAY
    ELSE IF con = TRUE THEN
        SEND "Hello" TO DISPLAY
    ELSE IF cond = FALSE THEN
        SEND "world" TO DISPLAY
    ELSE
        SEND "test" TO DISPLAY
    END IF

    """

t = Test(
    test,
    test_name = "else if",
    test_type = "parser",
    print_tokens = False,
)
t.run(write=True, show_error_message=True)

# for token in t.parser.lexer.tokens:
#     print(token, " ---> ")


