from tests.general_test import Test


test = """


SET low TO 0
SET high TO length(array)-1
SET found TO FALSE
WHILE (found = FALSE) AND (low <= high) DO
SET mid TO (low + high)/2
IF target = array[mid]
SEND target & “ found at position ” & mid TO DISPLAY
SET found TO TRUE
ELSE IF target > array[mid]
SET low TO mid+1
ELSE
SET high TO mid–1
END IF
END WHILE



"""

Test(
    test,
    test_name = "Binary Search",
    test_type = "parser",
    print_tokens = False,

).run(show_error_message=True)
