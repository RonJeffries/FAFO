from typing import Any, Self
from collections import namedtuple

Atom = namedtuple("Atom", ["element", "scope"])


class XSet:
    @classmethod
    def classical_set(cls, a_list):
        null = cls([])
        wrapped = [Atom(item, null) for item in a_list]
        return cls(wrapped)

    @classmethod
    def tuple_set(cls, a_list):
        wrapped = [Atom(item, index+1) for index, item in enumerate(a_list)]
        return cls(wrapped)

    def __init__(self, a_list):
        self.contents = frozenset(a_list)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.contents == other.contents
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.contents)

    def __iter__(self):
        return self.contents.__iter__()

    def is_subset(self, other):
        if isinstance(other, self.__class__):
            return self.contents.issubset(other.contents)
        else:
            return NotImplemented

    def restrict(self, other) -> Self:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return XSet((candidate_atom for candidate_atom in self.contents
                          if any((check_atom.element.is_subset(candidate_atom.element)
                                  for check_atom in other.contents))))


XSet.null = XSet([])
# end of XSet ----------------------


class TestXST:
    def test_tuples(self):
        a1 = Atom(1, 2)
        a2 = Atom(2 - 1, 3 - 1)
        a3 = Atom(2, 1)
        assert a1 == a2
        assert not a1 == a3

    def test_members(self):
        a1 = Atom(31, 42)
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

    def test_frozen_sets(self):
        r1 = frozenset([Atom("jeffries", "last"), Atom("ron", "first")])
        r2 = frozenset([Atom("chet", "first"), Atom("hendrickson", "last")])
        r2rev = frozenset([Atom("hendrickson", "last"), Atom("chet", "first")])
        r3 = frozenset([Atom("hill", "last"), Atom("geepaw", "first")])
        personnel = frozenset([r1, r2])
        assert r1 in personnel
        assert r2 in personnel
        assert r2rev in personnel  # <======
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

    def test_classical_set(self):
        things = ["a", "b", "c"]
        classical = XSet.classical_set(things)
        b_atom = Atom("b", XSet.null)
        assert b_atom in classical
        wrong_atom = Atom("b", 1)
        assert wrong_atom not in classical

    def test_xset_restrict(self):
        ron = XSet([Atom("jeffries", "last"), Atom("ron", "first"), Atom("boss", "job")])
        chet = XSet([Atom("chet", "first"), Atom("hendrickson", "last"), Atom("boss", "job")])
        hill = XSet([Atom("hill", "last"), Atom("geepaw", "first"), Atom("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        boss_record = XSet([Atom("boss", "job")])
        boss_set = XSet.classical_set([boss_record])
        bosses = personnel.restrict(boss_set)
        assert isinstance(bosses, XSet)
        assert Atom(ron, XSet.null) in bosses
        assert Atom(chet, XSet.null) in bosses
        assert Atom(hill, XSet.null) not in bosses

    def test_xset_tuple_restrict(self):
        ron = XSet([Atom("jeffries", "last"), Atom("ron", "first"), Atom("boss", "job")])
        chet = XSet([Atom("chet", "first"), Atom("hendrickson", "last"), Atom("boss", "job")])
        hill = XSet([Atom("hill", "last"), Atom("geepaw", "first"), Atom("serf", "job")])
        personnel = XSet.tuple_set([ron, chet, hill])
        boss_record = XSet([Atom("boss", "job")])
        boss_set = XSet.tuple_set([boss_record])
        bosses = personnel.restrict(boss_set)
        assert Atom(ron, 1) in bosses
        assert Atom(chet, 2) in bosses
        assert Atom(hill, 3) not in bosses

    def test_xset_restrict_again(self):
        ron = XSet([Atom("jeffries", "last"), Atom("ron", "first"), Atom("boss", "job")])
        chet = XSet([Atom("chet", "first"), Atom("hendrickson", "last"), Atom("boss", "job")])
        hill = XSet([Atom("hill", "last"), Atom("geepaw", "first"), Atom("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        serf_record = XSet([Atom("serf", "job")])
        serf_set = XSet.classical_set([serf_record])
        serfs = personnel.restrict(serf_set)
        null = XSet([])
        assert Atom(ron, null) not in serfs
        assert Atom(chet, null) not in serfs
        assert Atom(hill, null) in serfs

    def test_frozen_operators(self):
        s1 = frozenset(("a", "b", "c"))
        s2 = frozenset(("x", "y"))
        s3 = s1 | s2
        assert s3 == {"a", "x", "c", "b", "y"}
        s2 |= s1
        assert s2 == s3

    def test_syntax(self):
        a = {"last": "hill"}
        m = max((1, 2, 3, 4))
        assert m == 4
