array = [2,4,5,1,6,8,3,4]

n = len(array)
swapped = True
while (swapped == True) and (n>=0):
    swapped = False
    for index in range(0, n-1): 
        if array[index]>array[index+1]:
            temp = array[index]
            array[index] = array[index+1]
            array[index+1] = temp
            swapped = True
    n = n-1

print(array)