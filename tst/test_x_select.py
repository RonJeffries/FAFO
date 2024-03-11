from ximpl import XImplementation
from xset import XSet


class XSelect(XImplementation):
    def __init__(self, base, cond):
        self._base = base
        self._cond = cond

    def __iter__(self):
        for e, s in self._base:
            if self._cond(e, s):
                yield e, s

    def __hash__(self):
        return hash(self._base)

    def __len__(self):
        len = 0
        for _t in self:
            len += 1
        return len

    def __repr__(self):
        return f'XSelect({self._base})'


class TestXSelect:
    def test_hookup(self):
        assert 3 == 3

    def test_plain_select(self):
        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        selected = source.select(lambda e, _s: 'x' in e)
        assert selected[2] == 'dxef'
        assert selected[4] == 'xyz'

    def test_x_select(self):
        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        x_select = XSelect(source, )
        assert len(x_select) == 2
        it = iter(x_select)
        assert next(it) == ('dxef', 2)
        assert next(it) == ('xyz', 4)

    def test_through_XSet(self):
        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        sel1 = XSet.from_tuples((('dxef', 2), ))
        sel2 = XSet.from_tuples((('xyz', 4), ))
        sub1 = source.x_select(lambda e, s: (e, s) in sel1)
        sub2 = source.x_select(lambda e, s: (e, s) in sel2)
        result = sub1 | sub2
        assert ('dxef', 2) in result
        assert ('xyz', 4) in result

    def test_cascade(self):
        def even(e, _s):
            return e%2 == 0

        def fiveish(e, _s):
            return e%5 == 0

        source = XSet.classical_set(range(21))
        fives = source.x_select(fiveish)
        even_fives = fives.x_select(even)
        expected = XSet.classical_set((0, 10, 20))
        assert even_fives == expected

