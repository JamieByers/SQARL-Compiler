# from tests.general_test import Test

# t = Test(
#     string = """

#     SET low TO 0
# SET high TO length(array)-1
# SET found TO FALSE
# WHILE (found = FALSE) AND (low <= high) DO
# SET mid TO (low + high)/2
# IF target = array[mid]
# SEND target & “ found at position ” & mid TO DISPLAY
# SET found TO TRUE
# ELSE IF target > array[mid]
# SET low TO mid+1
# ELSE
# SET high TO mid–1
# END IF
# END WHILE
# """,
#     test_type="parser",
#     test_name="real_life_test",
# )

# t.run(show_error_message=True, write=True)

from parser import Parser 

p = Parser(
    """
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
    SET high TO mid-1
    END IF
    END WHILE

"""
)

p.parse()