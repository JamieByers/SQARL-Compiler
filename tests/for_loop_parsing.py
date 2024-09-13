from tests.general_test import Test


tests = ["FOR i FROM 0 TO 9 DO SEND 'hello' TO DISPlAY END FOR",
         "FOR id FROM expr TO expr STEP expr DO SEND 'hello' TO DISPlAY END FOR",
         "FOR EACH id FROM expression DO SEND 'hello' TO DISPlAY END FOR EACH"]

for test in tests:
    tst = Test(

    test,
    test_name= " ".join(test.split(" ")[0:3]),
    test_type="parser",
    print_tokens=False,

    )

    tst.run(show_error_message=True)
