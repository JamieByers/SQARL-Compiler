from tests.general_test import Test


tests = ["FOR id FROM expr TO expr DO command END FOR", 
         "FOR id FROM expr TO expr STEP expr DO command END FOR", 
         "FOR EACH id FROM expression DO command END FOR EACH"]

for test in tests:
    tst = Test(
    
    test,
    test_name= " ".join(test.split(" ")[0:3]),
    test_type="tokeniser",
    print_tokens=True,
    
    )

    tst.run(show_error_message=True)
    
