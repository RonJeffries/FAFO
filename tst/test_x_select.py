from set_builder import SetBuilder
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
        def cond(e, s):
            return 'x' in e

        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        selected = source.select(cond)
        assert selected[2] == 'dxef'
        assert selected[4] == 'xyz'

    def test_x_select(self):
        def cond(e, s):
            return 'x' in e

        source = XSet.n_tuple(('abc', 'dxef', 'ghi', 'xyz'))
        x_select = XSelect(source, cond)
        assert len(x_select) == 2
        it = iter(x_select)
        assert next(it) == ('dxef', 2)
        assert next(it) == ('xyz', 4)

