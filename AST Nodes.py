VariableAssignment(type='VariableAssignment', code="n = FunctionCall(type='FunctionCall', code='length(array)', idenitifer='length', params=['array'])", name='n', value="FunctionCall(type='FunctionCall', code='length(array)', idenitifer='length', params=['array'])")
VariableAssignment(type='VariableAssignment', code='swapped = True', name='swapped', value='True')
VariableAssignment(type='VariableAssignment', code='swapped = False', name='swapped', value='False')
VariableAssignment(type='VariableAssignment', code='temp = array[index]', name='temp', value='array[index]')
VariableAssignment(type='VariableAssignment', code='array[index] = array[index+1]', name='array[index]', value='array[index+1]')
VariableAssignment(type='VariableAssignment', code='array[index+1] = temp', name='array[index+1]', value='temp')
VariableAssignment(type='VariableAssignment', code='swapped = True', name='swapped', value='True')
IfStatement(type='IfStatement', code='', condition=Condition(type='condition', code='', value='array[index]>array[index+1]'), code_block='            temp = array[index]\n            array[index] = array[index+1]\n            array[index+1] = temp\n            swapped = True\n', else_block=None, else_if_block=None)
ForStatement(type='ForStatement', code='', variable='index', start=0.0, end='n-2', step=1, code_block="        if Condition(type='condition', code='', value='array[index]>array[index+1]'):\n            temp = array[index]\n            array[index] = array[index+1]\n            array[index+1] = temp\n            swapped = True\n")
VariableAssignment(type='VariableAssignment', code='n = n-1.0', name='n', value='n-1.0')
WhileStatement(type='WhileStatement', code='', condition=Condition(type='condition', code='', value='(swapped == True) and (n>=0.0)'), code_block="    swapped = False\n    for index in range(0.0, n-2): \n        if Condition(type='condition', code='', value='array[index]>array[index+1]'):\n            temp = array[index]\n            array[index] = array[index+1]\n            array[index+1] = temp\n            swapped = True\n    n = n-1.0\n")
