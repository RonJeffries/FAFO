from collections import namedtuple
Atom = namedtuple("Atom", ["element", "scope"])

class TestXST:
    def test_tuples(self):
        a1 = Atom(1, 2)
        a2 = Atom(2-1, 3-1)
        a3 = Atom(2, 1)
        assert a1 == a2
        assert not a1 == a3

    def test_members(self):
        a1 = Atom (31, 42)
        assert a1.element == 31
        assert a1.scope == 42
