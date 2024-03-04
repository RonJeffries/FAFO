from expressions import Expression, Parser, Token


class TestExpressions:
    def test_create_Expression(self):
        expr = Expression('gross_pay', [])

    def test_returns_constant(self):
        op = Token('literal', '42', None)
        record = None
        expression = Expression('Answer', [op])
        assert expression.scope() == 'Answer'
        assert expression.result(record) == '42'

    def test_rpn(self):
        op21 = Token('literal', '21', None)
        op2 = Token('literal', '2', None)
        times = Token('operator', '*', 2)
        operations = [op21, op2, times]
        expression = Expression('Answer', operations)
        assert expression.result(None) == '42'

    def test_make_rpn(self):
        text = '21 * 2'
        rpn = Parser(text).rpn()
        assert rpn[0].kind == 'literal'
        assert rpn[1].kind == 'literal'
        assert rpn[2].kind == 'operator'

    def test_make_harder_rpn(self):
        text = 'pay * 1.1 + bonus'
        rpn = Parser(text).rpn()
        values = [t.value for t in rpn]
        assert values == ['pay', '1.1', '*', 'bonus', '+' ]

    def test_lexing(self):
        text = '21 * 2'
        lex = Parser(text).lex()
        assert lex == ['21', '*', '2']

    def test_token_sequence(self):
        parser = Parser('')
        token = parser.make_token('*')
        assert token.kind == 'operator'
        assert token.value == '*'
        assert token.priority == 2

    def test_round_trip(self):
        text = '10 * 2 * 2 + 2'
        rpn = Parser(text).rpn()
        result = Expression('Ignored', rpn).result(None)
        assert result == '42'
