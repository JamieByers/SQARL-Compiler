from tests.general_test import Test

test = """
                IF condition = true THEN
                    DECLARE hello INITIALLY "hello"
                    SET hello TO "hello world!"
                    SEND hello TO DISPlAY
                ELSE IF conition = false THEN
                    SEND "what?" TO DISPLAY
                ELSE
                    SEND "NO WAY" TO DISPLAY
                END IF
"""

t = Test(
        test,
        test_name="if statement parsing",
        test_type="code generator",
        print_tokens=False,
        print_ASTNodes=False,
)

t.run(display=True, show_error_message=True, write=True)

