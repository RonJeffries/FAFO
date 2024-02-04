from collections import namedtuple
Atom = namedtuple("Atom", ["element", "scope"])


class XSet:
    def __init__(self, a_list):
        self.contents = a_list

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.is_subset(other) and other.is_subset(self)
        else:
            return False

    def __iter__(self):
        return self.contents.__iter__()

    def is_subset(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(atom in other for atom in self)


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

    def test_xset_in(self):
        list1 = [Atom("x", 1), Atom("y", 2)]
        list2 = [Atom("y", 2), Atom("x", 1)]
        assert list1 != list2
        set1 = XSet(list1)
        set2 = XSet(list2)
        assert set1 == set2
        set3 = XSet([Atom("z", 1), Atom("y", 2)])
        assert set1 != set3

    def test_xset_records_in(self):
        r1 = XSet([Atom("jeffries", "last"), Atom("ron", "first")])
        r2 = XSet([Atom("chet", "first"), Atom("hendrickson", "last")])
        r2rev = XSet([Atom("hendrickson", "last"), Atom("chet", "first")])
        r3 = XSet([Atom("hill", "last"), Atom("geepaw", "first")])
        personnel = XSet([r1, r2])
        assert r1 in personnel
        assert r2 in personnel
        assert r2rev in personnel  # this test killed Python {}
        assert r3 not in personnel

