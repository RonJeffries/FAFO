import pytest

from expressions import Parser, Expression
from ximpl import XImplementation
from xset import XSet


class XCalculation(XImplementation):
    def __init__(self, base_set, expressions):
        self.base = base_set
        self.expressions = []
        for expr in expressions:
            rpn = Parser(expr).rpn()
            calc = Expression(None, rpn)
            tokens = [t.value for t in calc._tokens]
            print(calc.scope(), tokens)
            self.expressions.append(calc)

    def __iter__(self):
        for record, record_scope in self.base:
            calculated_values = self.create_calculated_values(record)
            full_record = record.union(calculated_values)
            yield full_record, record_scope

    def create_calculated_values(self, record):
        calculated = [(calc.result(record), calc.scope()) for calc in self.expressions]
        return XSet.from_tuples(calculated)

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
