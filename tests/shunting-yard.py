class Token:
    def __init__(self, value) -> None:
        self.value = value

tokens = [Token("4"), Token("+"), Token("18"), Token("/"), Token("("), Token("9"), Token("-"), Token("3"), Token(")")]

def shunting_yard(tokens):
    pos = 0
    length = len(tokens)

    operator_stack = []
    output_queue = []
    operators = ["+", "-", "/", "*"]
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    def evaluate_RPN(rpn_tokens):
        stack = []

        for token in rpn_tokens:
            if token.isdigit():
                stack.append(int(token))
            else:
                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "/":
                    stack.append(left / right)
                elif token == "*":
                    stack.append(left * right)

        return stack[0]


    while pos < length and tokens[pos]:
        token = tokens[pos].value

        if token.isdigit():
            output_queue.append(token)
        
        elif token in operators:
            while operator_stack and operator_stack[-1] in operators and precedence[operator_stack[-1]] >= precedence[token]:
                top_op = operator_stack.pop()
                output_queue.append(top_op)
            operator_stack.append(token)

        elif token == "(":
            operator_stack.append(token)
        
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            operator_stack.pop()  
        
        pos += 1

    while operator_stack:
        output_queue.append(operator_stack.pop())

    print(output_queue)
    eval = evaluate_RPN(output_queue)
    print("eval: ", eval)

shunting_yard(tokens)
