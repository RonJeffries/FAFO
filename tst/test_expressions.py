

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


class TestExpressions:
    def test_create_Expression(self):
        expr = Expression('gross_pay', [])

    def test_returns_constant(self):
        op = lambda self, stack, record: stack.append('42')
        record = None
        expression = Expression('Answer', [op])
        assert expression.scope() == 'Answer'
        assert expression.result(record) == '42'

    def test_rpn(self):
        op21 = lambda self, stack, record: stack.append('21')
        op2 = lambda self, stack, record: stack.append('2')
        def plus(self, stack, number):
            op1 = self.to_number(stack.pop())
            op2 = self.to_number(stack.pop())
            stack.append(str(op1 * op2))

        operations = [op21, op2, plus]
        expression = Expression('Answer', operations)
        assert expression.result(None) == '42'
