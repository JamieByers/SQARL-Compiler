from tests.general_test import Test

t = Test(

    """
        FUNCTION func(param1, param2)
            RETURN 0
        END FUNCTION
    """,

    test_type = "parser",
    test_name = "function parsing",
    print_tokens = False

)

t.run(True)


