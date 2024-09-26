n = FunctionCall(type='FunctionCall', code='length(array)', idenitifer='length', params=['array'])
swapped = True
while Condition(type='condition', code='', value='(swapped == True) and (n>=0.0)'):
    swapped = False
    for index in range(0.0, n-2): 
        if Condition(type='condition', code='', value='array[index]>array[index+1]'):
            temp = array[index]
            array[index] = array[index+1]
            array[index+1] = temp
            swapped = True
    n = n-1.0
