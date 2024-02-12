from src.x_impl import XImplementation
from src.xset import XSet


class XFrozen(XImplementation):
    def __init__(self, fs):
        self.data = fs

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        return iter(self.data)

    def __hash__(self):
        return hash(self.data)

    def __repr__(self):
        return repr(self.data)


class TestXFrozen:
    def test_exists(self):
        fs = frozenset((1, 2, 3))
        frozen = XFrozen(fs)
        assert 1 in frozen
        assert 4 not in frozen

    def test_in_use(self):
        xs = XSet.classical_set(("a", "b", "c"))
        xs.implementation = XFrozen(xs.implementation)
        assert xs.includes("a", None)
        assert xs.excludes("a", 1)
        assert xs.excludes("d", None)
        elements = set()
        scopes = set()
        for e,s in xs:
            elements.add(e)
            scopes.add(s)
        assert elements == {"a", "c", "b"}
        assert scopes == {XSet.null}
