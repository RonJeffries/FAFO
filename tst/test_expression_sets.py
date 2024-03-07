import pytest

from expressions import Parser, Expression
from ximpl import XImplementation
from xset import XSet


class XCalculation(XImplementation):
    def __init__(self, base_set, expressions):
        self.base = base_set
        self.expressions = expressions

    def __iter__(self):
        for record, s in self.base:
            calculated = []
            for expr in self.expressions:
                rpn = Parser(expr).rpn()
                calc = Expression(None, rpn)
                value = calc.result(record)
                calculated.append((value, calc.scope()))
            all_results = XSet.from_tuples(calculated)
            full_record = record.union(all_results)
            yield full_record, s

    def __hash__(self):
        return hash(self.base)

    def __len__(self):
        return len(self.base)

    def __repr__(self):
        return f'XCalc({[self.expressions]}'


class TestExpressionSets:
    @pytest.mark.skip("later")
    def test_total_pay(self):
        p1 = XSet.from_tuples((('joe', 'name'),('10000', 'salary'), ('2345', 'bonus')))
        p2 = XSet.from_tuples((('sam', 'name'),('50301', 'salary'), ('4020', 'bonus')))
        personnel = XSet.n_tuple((p1, p2))
        total = 'totalpay = salary + bonus'
        result = personnel.calculate([total])
        r1 = result[1]
        tp1 = r1['totalpay']
        assert tp1 == '12345'
        r2 = result[2]
        tp2 = r2['totalpay']
        assert tp2 == '54321'

    def test_x_calculation(self):
        expression = 'totalpay = salary + bonus'
        data = XSet.n_tuple(["a", "b"])
        x_calc = XCalculation(data, [expression])
        assert x_calc.base == data
        assert expression in x_calc.expressions

    def test_x_calculation_iter(self):
        p1 = XSet.from_tuples((('joe', 'name'),('10000', 'salary'), ('2345', 'bonus')))
        p2 = XSet.from_tuples((('sam', 'name'),('50301', 'salary'), ('4020', 'bonus')))
        personnel = XSet.n_tuple((p1, p2))
        total = 'totalpay = salary + bonus'
        double = 'double = bonus * 2'
        x_calc = XCalculation(personnel, [total, double])
        for e, s in x_calc:
            if s == 1:
                assert e['name'] == 'joe'
                assert e['totalpay'] == '12345'
                assert e['double'] == '4690'
            elif s == 2:
                assert e['name'] == 'sam'
                assert e['totalpay'] == '54321'
                assert e['double'] == '8040'
