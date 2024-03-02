from xset import XSet


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


