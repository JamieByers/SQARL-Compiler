from tests.general_test import Test


class Real_test:
    def __init__(self, name, test_data):
        self.name = name
        self.test_data = test_data


tests = [
    Real_test("binary search", """

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

    """),

    Real_test("Bubble sort", """
SET n TO length(array)
SET swapped TO TRUE
WHILE (swapped = TRUE) AND (n >= 0) DO
SET swapped TO FALSE
FOR index FROM 0 TO n-2 DO
IF array[index] > array[index+1] THEN
SET temp TO array[index]
SET array[index] TO array[index+1]
SET array[index+1] TO temp
SET swapped TO TRUE
END IF
END FOR
SET n TO n -1
END WHILE
    """),

    Real_test("insertion sort", """

FOR i FROM 1 TO length(array)-1 DO
SET temp TO array[i]
SET index TO i
WHILE (index > 0) AND (temp < array[index-1]) DO
SET array[index] TO array[index-1]
SET index TO index–1
END WHILE
SET array[index] TO temp
END FOR

    """)


]

for test in tests:
    Test(
        test.test_data,
        test_name = test.name,
        test_type = "parser",
    ).run(show_error_message=True)
