from tests.general_test import Test

test =  """
        DECLARE words INITIALLY [1,2,3]
        FOR EACH word FROM words DO

            SEND word TO DISPLAY

        END FOR EACH


    """

print(test)

t = Test(
    test,
    test_name = "for each",
    test_type = "parser",
    print_tokens = False,

)

t.run(show_error_message=True, write=True)
