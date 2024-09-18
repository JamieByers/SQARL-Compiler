n = length(array)
swapped = True
while (swapped == True) and (n>=0):
    swapped = False
    for index in range(0, n-2): 
        if array[index]>array[index+1]:
            temp = array[index]
            array[index] = array[index+1]
            array[index+1] = temp
            swapped = True
    n = n-1
