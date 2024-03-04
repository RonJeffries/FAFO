import re


class Expression:
    def __init__(self, scope, operations):
        self._scope = scope
        self._operations = operations[::-1]

    def result(self, record):
        def to_number(string):
            return int(string)

        stack = []
        while self._operations:
            self._operations.pop()(self, stack, record)
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

    def parse(self, forward_lexed):
        stack = []
        result = []
        lexed = forward_lexed[::-1]
        while lexed:
            item = lexed.pop()
            if item in ['*']:
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

