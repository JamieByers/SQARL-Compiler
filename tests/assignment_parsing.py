from tests.general_test import Test

tests = ["SET condition TO true", "SET hello TO 'world'", "SET n TO 10"]

for test in tests:
    print("running", test)
    t = Test(
        test,
        test_name = " ".join(test.split(" ")[0:2]),
        test_type = "parser",

    )

    t.ru(show_error_message=True)
