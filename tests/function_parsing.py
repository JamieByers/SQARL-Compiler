from tests.general_test import Test

t = Test(

    """
        FUNCTION func(param1, param2) RETURNS INTEGER
            RETURN 0
        END FUNCTION
        PROCEDURE proc(p1, p2) RETURNS INTEGER
            RETURN 1
        END PROCEDURE
    """,

    test_type = "parser",
    test_name = "function parsing",
    print_tokens = False

)

t.run(True)


