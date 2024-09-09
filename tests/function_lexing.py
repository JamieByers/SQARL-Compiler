from tests.general_test import Test

t = Test(

    """
        FUNCTION func(param1, param2)
            RETURN 0
        END FUNCTION
    """,

    test_type = "tokeniser",
    test_name = "function lexing",
    print_tokens = True

)

t.run(True)


