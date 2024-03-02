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
        lexed = ['a123', '+', '37', '*', 'b17', '-', 'c', '*', '37.5']
        rpn = dij(lexed)
        assert rpn == ['a123', '37', 'b17', '*', 'c', '37.5', '*', '-', '+']

    def test_int(self):
        with pytest.raises(ValueError):
            int('1.1')


