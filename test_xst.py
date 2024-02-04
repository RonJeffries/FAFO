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

    def test_set_in(self):
        a1 = Atom("jeffries", "name")
        a2 = Atom("hendrickson", "name")
        a3 = Atom("hill", "name")
        s1 = {a1, a2}
        assert a1 in s1
        assert a2 in s1
        assert a3 not in s1

    def test_show_sets_insufficient_for_xst(self):
        r1 = [Atom("jeffries", "last"), Atom("ron", "first")]
        r2 = [Atom("chet", "first"), Atom("hendrickson", "last")]
        r2rev = [Atom("hendrickson", "last"), Atom("chet", "first")]
        r3 = [Atom("hill", "last"), Atom("geepaw", "first")]
        personnel = [r1, r2]
        assert r1 in personnel
        assert r2 in personnel
        assert r2rev not in personnel  # but we need it to be
        assert r3 not in personnel

