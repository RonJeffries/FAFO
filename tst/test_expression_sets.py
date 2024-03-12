import pytest

from expressions import XCalculation
from xset import XSet


class TestExpressionSets:
    def test_total_pay(self):
        p1 = XSet.from_tuples((('joe', 'name'),('10000', 'salary'), ('2345', 'bonus')))
        p2 = XSet.from_tuples((('sam', 'name'),('50301', 'salary'), ('4020', 'bonus')))
        personnel = XSet.n_tuple((p1, p2))
        total = 'total_pay = salary + bonus'
        double = 'double = bonus * 2'
        result = personnel.calculate([total, double])
        joe_rec = result[1]
        assert joe_rec['name'] == 'joe'
        assert joe_rec['total_pay'] == '12345'
        assert joe_rec['double'] == '4690'
        sam_rec = result[2]
        assert sam_rec['name'] == 'sam'
        assert sam_rec['total_pay'] == '54321'
        assert sam_rec['double'] == '8040'

    def test_x_calculation_iter(self):
        p1 = XSet.from_tuples((('joe', 'name'),('10000', 'salary'), ('2345', 'bonus')))
        p2 = XSet.from_tuples((('sam', 'name'),('50301', 'salary'), ('4020', 'bonus')))
        personnel = XSet.n_tuple((p1, p2))
        total = 'total_pay = salary + bonus'
        double = 'double = bonus * 2'
        x_calc = XCalculation(personnel, [total, double])
        for e, s in x_calc:
            if s == 1:
                assert e['name'] == 'joe'
                assert e['total_pay'] == '12345'
                assert e['double'] == '4690'
            elif s == 2:
                assert e['name'] == 'sam'
                assert e['total_pay'] == '54321'
                assert e['double'] == '8040'

    def test_x_calculation_patch_set(self):
        p1 = XSet.from_tuples((('joe', 'name'),('10000', 'salary'), ('2345', 'bonus')))
        p2 = XSet.from_tuples((('sam', 'name'),('50301', 'salary'), ('4020', 'bonus')))
        personnel = XSet.n_tuple((p1, p2))
        total = 'total_pay = salary + bonus'
        double = 'double = bonus * 2'
        x_calc = XCalculation(personnel, [total, double])
        calc_set = XSet(x_calc)
        joe_rec = calc_set[1]
        assert joe_rec['name'] == 'joe'
        assert joe_rec['total_pay'] == '12345'
        assert joe_rec['double'] == '4690'
        sam_rec = calc_set[2]
        assert sam_rec['name'] == 'sam'
        assert sam_rec['total_pay'] == '54321'
        assert sam_rec['double'] == '8040'
