from functools import partial

import pytest

from xset import XSet
import re


def dijkstra(lexed: list):
    priority = {'+': 1, '-': 1, '*': 2}
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


def make_executable(rpn):
    ops = {'+': '__add__', '*': '__mul__'}

    def stack_value(value, stack):
        stack.append(to_number(value))

    def binary_op(op, stack):
        stack.append(getattr(stack.pop(), op)(stack.pop()))

    exec = []
    for r in rpn:
        if r in ops:
            do_op = partial(binary_op, ops[r])
            exec.append(do_op)
        else:
            sv = partial(stack_value, r)
            exec.append(sv)
    return exec


def interpret(rpn):
    stack = []
    r = rpn[::-1]
    executable_r = make_executable(r)
    while executable_r:
        executable_r.pop()(stack)
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
        rpn = dijkstra(lexed)
        assert rpn == ['a123', '37', '+']

    def test_dijkstra_2(self):
        expr = 'a123 + 37*b17 - c*37.5'
        lexed = ['a123', '+', '37', '*', 'b17', '-', 'c', '*', '37.5']
        rpn = dijkstra(lexed)
        assert rpn == ['a123', '37', 'b17', '*', 'c', '37.5', '*', '-', '+']

    def test_int(self):
        with pytest.raises(ValueError):
            int('1.1')
        with pytest.raises(ValueError):
            int('123abc')
        assert int(42) == 42
        assert float(42.42) == 42.42

    def test_lambda(self):
        v = 2
        l1 = lambda: 2 * v
        v = 3
        assert l1() == 6  # surprised me

    def test_interpret(self):
        rpn = ['37', '5', '+']
        result = interpret(rpn)
        assert result == 42

    def test_interpret_2(self):
        expr = '10 * 2 + 10 * 2 + 2'
        lexed = lex(expr)
        assert lexed == ['10', '*', '2', '+', '10', '*', '2', '+', '2']
        rpn = dijkstra(lexed)
        assert rpn == ['10', '2', '*', '10', '2', '*', '2', '+', '+']
        result = interpret(rpn)
        assert result == 42

    def test_lambda_2(self):
        def full(val, stack):
            stack.append(val)

        stack_6 = partial(full, 6)
        stack = []
        stack_6(stack)
        assert stack[0] == 6


