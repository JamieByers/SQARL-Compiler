from tests.general_test import Test

test = """
SET n TO 10
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
    """

t = Test(
        test,
        test_name = "real life",
        test_type = "parser",
)
t.run()
