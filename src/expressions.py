import re


class Expression:
    def __init__(self, scope, tokens):
        self._scope = scope
        self._cached_tokens = [t.value for t in tokens]
        self._tokens = tokens[::-1]
        self.handle_assignment()

    def handle_assignment(self):
        if self._tokens:
            initial_token = self._tokens[0]
            if initial_token.is_assignment():
                final_token = self._tokens[-1]
                self._scope = final_token.value
                self._tokens = self._tokens[1:-2]

    def result(self, record):
        stack = []
        while self._tokens:
            token = self._tokens.pop()
            if token.kind == 'literal':
                stack.append(token.value)
            elif token.kind == 'operator':
                try:
                    arg_1 = self.to_number(stack.pop())
                    arg_2 = self.to_number(stack.pop())
                except IndexError:
                    return f'Too many operators: {self._cached_tokens}'
                res = self.execute_operation(token, arg_1, arg_2)

                stack.append(str(res))
        if len(stack) != 1:
            return f'operator/operand mismatch: {self._cached_tokens}'
        return stack.pop()

    @staticmethod
    def execute_operation(token, arg_1, arg_2):
        match token.value:
            case '+':
                return arg_1 + arg_2
            case '-':
                return arg_1 - arg_2
            case '*':
                return arg_1 * arg_2
            case '/':
                return arg_1 / arg_2
            case _:
                return f'Unknown operator{token.value}'

    def scope(self):
        return self._scope

    @staticmethod
    def to_number(string):
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
        rx = '([^a-zA-Z0-9.])'
        split = re.split(rx, self._expr)
        return [item for item in split if item and item != ' ']


class Token:
    def __init__(self, kind, value, priority):
        self.kind = kind
        self.value = value
        self.priority = priority

    def __repr__(self):
        return f'Token({self.kind}, {self.value}, {self.priority})'

    def is_assignment(self):
        return self.value == '='

