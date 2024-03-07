from expressions import Expression, Parser, Token
from xset import XSet


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
        assert values == ['pay', '1.1', '*', 'bonus', '+']

    def test_assignment(self):
        text = 'four = 3 + 1'
        rpn = Parser(text).rpn()
        values = [t.value for t in rpn]
        assert values == ['four', '3', '1', '+', '=']

    def test_expression_gets_scope(self):
        text = 'four = 3 + 1'
        rpn = Parser(text).rpn()
        tokens = [t.value for t in rpn]
        assert tokens == ['four', '3', '1', '+', '=']
        expr = Expression('wrong', rpn)
        assert expr.scope() == 'four'
        adjusted_tokens = [t.value for t in expr._tokens]
        assert adjusted_tokens == ['+', '1', '3']

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

    def test_float(self):
        text = '20.5 * 2 + 1'
        rpn = Parser(text).rpn()
        result = Expression('Ignored', rpn).result(None)
        assert result == '42.0'

    def test_too_many_operators(self):
        text = '2 + - *'
        rpn = Parser(text).rpn()
        result = Expression('Ignored', rpn).result(None)
        assert result == "Too many operators: ['2', '*', '-', '+']"

    def test_malformed(self):
        text = '6 7 + 5'
        rpn = Parser(text).rpn()
        result = Expression('Ignored', rpn).result(None)
        assert result == "operator/operand mismatch: ['6', '7', '5', '+']"

    def test_lex(self):
        text = '2 + - *'
        lexed = Parser(text).lex()
        assert lexed == ['2', '+', '-', '*']

    def test_lex_2(self):
        text = 'abc   def  +    5'
        lexed = Parser(text).lex()
        assert lexed == ['abc', 'def', '+', '5']

    def test_record(self):
        text = 'pay = salary + bonus'
        rpn = Parser(text).rpn()
        print()
        print("rpn", rpn)
        record = XSet.from_tuples((('10000', 'salary'), ('2345', 'bonus')))
        assert record.get('salary') == '10000'
        expr = Expression('ignored', rpn)
        assert expr.scope() == 'pay'
        result = expr.result(record)
        assert result == '12345'

    def test_twice(self):
        text = 'pay = salary + bonus'
        rpn = Parser(text).rpn()
        print()
        print("rpn", rpn)
        record = XSet.from_tuples((('10000', 'salary'), ('2345', 'bonus')))
        assert record.get('salary') == '10000'
        expr = Expression('ignored', rpn)
        assert expr.scope() == 'pay'
        result = expr.result(record)
        assert result == '12345'
        result = expr.result(record)
        assert result == '12345'

    def test_scope_not_in_record(self):
        text = 'pay = salary + bogus'
        rpn = Parser(text).rpn()
        print()
        print("rpn", rpn)
        record = XSet.from_tuples((('10000', 'salary'), ('2345', 'bonus')))
        assert record.get('salary') == '10000'
        expr = Expression('ignored', rpn)
        assert expr.scope() == 'pay'
        result = expr.result(record)
        assert result == 'Record has no scope: bogus'
