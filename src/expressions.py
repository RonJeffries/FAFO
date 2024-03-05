import re


class Expression:
    def __init__(self, scope, operations):
        self._scope = scope
        if operations and operations[-1].value == '=':
            self._scope = operations[0].value
            operations = operations[1:-2]
        self._operations = operations[::-1]

    def result(self, record):
        def to_number(string):
            return int(string)

        stack = []
        while self._operations:
            op = self._operations.pop()
            if op.kind == 'literal':
                stack.append(op.value)
            elif op.kind == 'operator':
                op1 = self.to_number(stack.pop())
                op2 = self.to_number(stack.pop())
                match op.value:
                    case '+':
                        res = op1 + op2
                    case '-':
                        res = op1 - op2
                    case '*':
                        res = op1 * op2
                    case '/':
                        res = op1 / op2
                    case _:
                        res = f'Unknown operator{op.value}'

                stack.append(str(res))
        return stack.pop()

    def scope(self):
        return self._scope

    def to_number(self, string):
        try:
            return int(string)
        except ValueError:
            return float(string)


class Parser:
    def __init__(self, expression_string):
        self._expr = expression_string

    def make_tokens(self, lexed_list):
        return [self.make_token(item) for item in lexed_list]

    def make_token(self, string_item):
        if string_item in ['*', '/']:
            return Token('operator', string_item, 2)
        elif string_item in ['+', '-']:
            return Token('operator', string_item, 1)
        elif string_item == '=':
            return Token('operator', string_item, 0)
        elif string_item[0].isalpha():
            return Token('scope', string_item, None)
        else:
            return Token('literal', string_item, None)

    def parse(self, forward_lexed):
        stack = []
        result = []
        lexed = forward_lexed[::-1]
        tokens = self.make_tokens(lexed)
        while tokens:
            item = tokens.pop()
            if item.kind == 'operator':
                while stack and stack[-1].priority > item.priority:
                    result.append(stack.pop())
                stack.append(item)
            else:
                result.append(item)
        while stack:
            result.append(stack.pop())
        return result

    def rpn(self):
        lexed = self.lex()
        result = self.parse(lexed)
        return result

    def lex(self):
        no_space = self._expr.replace(' ', '')
        rx = '([^a-zA-Z0-9.])'
        return re.split(rx, no_space)


class Token:
    def __init__(self, kind, value, priority):
        self.kind = kind
        self.value = value
        self.priority = priority

    def __repr__(self):
        return f'Token({self.kind}, {self.value}, {self.priority})'

