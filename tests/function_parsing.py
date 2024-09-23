from tests.general_test import Test

t = Test(

    """
        FUNCTION func(STRING param1, INTEGER param2) RETURNS INTEGER
            RETURN 0
        END FUNCTION
        PROCEDURE proc(REAL p1 , ARRAY p2) RETURNS INTEGER
            RETURN 1
        END PROCEDURE
    """,

    test_type = "parser",
    test_name = "function parsing",
    print_tokens = False,
    print_ASTNodes=True

)

t.run(show_error_message=True)


