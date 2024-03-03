import pytest

from xset import XSet
import re


def dij(lexed: list):
    priority = { '+':1, '-':1, '*': 2}
    stack = []
    output = []
    expr = lexed[::-1]
    while expr:
        token = expr.pop()
        if token[0].isalpha():
            output.append(token)
        elif token[0].isnumeric():
            output.append(token)
        else:
            o1 = token
            p1 = priority[o1]
            while stack and stack[-1] != '(' and priority[stack[-1]] > p1:
                o2 = stack.pop()
                output.append(o2)
            stack.append(o1)
    while stack:
        output.append(stack.pop())
    return output


def to_number(string):
    try:
        return int(string)
    except ValueError:
        return float(string)


def interpret(rpn):
    stack = []
    r = rpn[::-1]
    while r:
        item = r.pop()
        if item == '+':
            stack.append(to_number(stack.pop()) + to_number(stack.pop()))
        elif item == '*':
            stack.append(to_number(stack.pop()) * to_number(stack.pop()))
        else:
            stack.append(item)
    return stack.pop()


def lex(expr):
    no_space = expr.replace(' ', '')
    rx = '([^a-zA-Z0-9.])'
    return re.split(rx, no_space)


class TestFunctions:
    def test_hookup(self):
        assert 2 == 2

    def test_calc_field(self):
        r1 = XSet.from_tuples(((1, 'a'), (2, 'b')))
        r2 = XSet.from_tuples(((10, 'a'), (20, 'b')))
        records = XSet.n_tuple((r1, r2))
        result = []
        for rec, _s in records:
            a = rec['a']
            b = rec['b']
            c = a + b
            new_rec = XSet.from_tuples(((a, 'a'), (b, 'b'), (c, 'c')))
            result.append(new_rec)
        new_set = XSet.n_tuple(result)
        c1 = new_set[1]
        assert c1['c'] == 3

    def test_lexing(self):
        expr = 'a123 + 37*b17 - c*37.5'
        no_space = expr.replace(' ', '')
        rx = '([^a-zA-Z0-9.])'
        lexed = re.split(rx, no_space)
        expected = ['a123', '+', '37', '*', 'b17', '-', 'c', '*', '37.5']
        assert lexed == expected

    def test_dijkstra_1(self):
        lexed = ['a123', '+', '37']
        rpn = dij(lexed)
        assert rpn == ['a123', '37', '+']

    def test_dijkstra_2(self):
        expr = 'a123 + 37*b17 - c*37.5'
        lexed = ['a123', '+', '37', '*', 'b17', '-', 'c', '*', '37.5']
        rpn = dij(lexed)
        assert rpn == ['a123', '37', 'b17', '*', 'c', '37.5', '*', '-', '+']

    def test_int(self):
        with pytest.raises(ValueError):
            int('1.1')
        with pytest.raises(ValueError):
            int('123abc')

    def test_interpret(self):
        rpn = ['37', '5', '+']
        result = interpret(rpn)
        assert result == 42

    def test_interpret_2(self):
        expr = '10 * 2 + 10 * 2 + 2'
        lexed = lex(expr)
        assert lexed == ['10', '*', '2', '+', '10', '*', '2', '+', '2']
        rpn = dij(lexed)
        assert rpn == ['10', '2', '*', '10', '2', '*', '2', '+', '+']
        result = interpret(rpn)
        assert result == 42


