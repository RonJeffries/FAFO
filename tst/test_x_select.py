from x_select import XSelect
from xset import XSet


class TestXSelect:
    def test_plain_select(self):
        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        selected = source.select(lambda e, _s: 'x' in e)
        assert selected[2] == 'dxef'
        assert selected[4] == 'xyz'

    def test_x_select(self):
        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        x_select = XSelect(source, lambda e, _s: 'x' in e)
        assert len(x_select) == 2
        it = iter(x_select)
        assert next(it) == ('dxef', 2)
        assert next(it) == ('xyz', 4)

    def test_through_XSet(self):
        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        sel1 = XSet.from_tuples((('dxef', 2), ))
        sel2 = XSet.from_tuples((('xyz', 4), ))
        sub1 = source.select(lambda e, s: (e, s) in sel1)
        sub2 = source.select(lambda e, s: (e, s) in sel2)
        result = sub1 | sub2
        assert ('dxef', 2) in result
        assert ('xyz', 4) in result

    def test_cascade(self):
        def even(e, _s):
            return e%2 == 0

        def fiveish(e, _s):
            return e%5 == 0

        source = XSet.classical_set(range(21))
        fives = source.select(fiveish)
        even_fives = fives.select(even)
        expected = XSet.classical_set((0, 10, 20))
        assert even_fives == expected

