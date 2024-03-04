from expressions import Expression, Parser


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
        def times(self, stack, number):
            op1 = self.to_number(stack.pop())
            op2 = self.to_number(stack.pop())
            stack.append(str(op1 * op2))

        operations = [op21, op2, times]
        expression = Expression('Answer', operations)
        assert expression.result(None) == '42'

    def test_make_rpn(self):
        text = '21 * 2'
        rpn = Parser(text).rpn()
        assert rpn == [('literal', '21', None), ('literal', '2', None), ('operator', '*', 2)]

    def test_lexing(self):
        text = '21 * 2'
        lex = Parser(text).lex()
        assert lex == ['21', '*', '2']

    def test_token_sequence(self):
        parser = Parser('')
        token = parser.make_token('*')
        assert token == ('operator', '*', 2)

