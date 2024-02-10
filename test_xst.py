import pytest

from xset import XSet, X_tuple


class TestXST:
    def test_tuples(self):
        a1 = (1, 2)
        a2 = (2 - 1, 3 - 1)
        a3 = (2, 1)
        assert a1 == a2
        assert not a1 == a3

    # def test_members(self):
    #     a1 = Atom(31, 42)
    #     assert a1.element == 31
    #     assert a1.scope == 42

    def test_set_in(self):
        a1 = ("jeffries", "name")
        a2 = ("hendrickson", "name")
        a3 = ("hill", "name")
        s1 = {a1, a2}
        assert a1 in s1
        assert a2 in s1
        assert a3 not in s1

    def test_show_sets_insufficient_for_xst(self):
        r1 = [("jeffries", "last"), ("ron", "first")]
        r2 = [("chet", "first"), ("hendrickson", "last")]
        r2rev = [("hendrickson", "last"), ("chet", "first")]
        r3 = [("hill", "last"), ("geepaw", "first")]
        personnel = [r1, r2]
        assert r1 in personnel
        assert r2 in personnel
        assert r2rev not in personnel  # but we need it to be
        assert r3 not in personnel

    def test_frozen_sets(self):
        r1 = frozenset([("jeffries", "last"), ("ron", "first")])
        r2 = frozenset([("chet", "first"), ("hendrickson", "last")])
        r2rev = frozenset([("hendrickson", "last"), ("chet", "first")])
        r3 = frozenset([("hill", "last"), ("geepaw", "first")])
        personnel = frozenset([r1, r2])
        assert r1 in personnel
        assert r2 in personnel
        assert r2rev in personnel  # <======
        assert r3 not in personnel

    def test_xset_in(self):
        list1 = [("x", 1), ("y", 2)]
        list2 = [("y", 2), ("x", 1)]
        assert list1 != list2
        set1 = XSet(list1)
        set2 = XSet(list2)
        assert set1 == set2
        set3 = XSet([("z", 1), ("y", 2)])
        assert set1 != set3

    def test_xset_records_in(self):
        r1 = XSet([("jeffries", "last"), ("ron", "first")])
        r2 = XSet([("chet", "first"), ("hendrickson", "last")])
        r2rev = XSet([("hendrickson", "last"), ("chet", "first")])
        r3 = XSet([("hill", "last"), ("geepaw", "first")])
        personnel = XSet.classical_set([r1, r2])
        null = XSet.null
        assert (r1, null) in personnel
        assert (r2, null) in personnel
        assert (r2rev, null) in personnel  # this test killed Python {}
        assert (r3, null) not in personnel

    def test_classical_set(self):
        things = ["a", "b", "c"]
        classical = XSet.classical_set(things)
        b_atom = ("b", XSet.null)
        assert b_atom in classical
        wrong_atom = ("b", 1)
        assert wrong_atom not in classical

    def test_xset_restrict(self):
        ron = XSet([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        chet = XSet([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        hill = XSet([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        boss_record = XSet([("boss", "job")])
        boss_set = XSet.classical_set([boss_record])
        bosses = personnel.restrict(boss_set)
        assert isinstance(bosses, XSet)
        assert len(bosses.contents) > 0
        assert bosses.includes(ron, None)
        assert bosses.includes(chet, None)
        assert bosses.excludes(hill, None)

    def test_xset_tuple_restrict(self):
        ron = XSet([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        chet = XSet([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        hill = XSet([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.tuple_set([ron, chet, hill])
        boss_record = XSet([("boss", "job")])
        boss_set = XSet.tuple_set([boss_record])
        bosses = personnel.restrict(boss_set)
        assert bosses.includes(ron, 1)
        assert bosses.includes(chet, 2)
        assert bosses.excludes(hill, 3)

    def test_xset_restrict_again(self):
        ron = XSet([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        chet = XSet([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        hill = XSet([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        serf_record = XSet([("serf", "job")])
        serf_set = XSet.classical_set([serf_record])
        serfs: XSet = personnel.restrict(serf_set)
        assert serfs.excludes(ron, None)
        assert serfs.excludes(chet, None)
        assert serfs.includes(hill, None)

    def test_select(self):
        def sel(e, s):
            print("checking", e, s)
            return e > 3
        s1 = XSet.tuple_set((0, 1, 2, 3, 4, 5, 6))
        selected = s1.select(sel)
        assert (4, 5) in selected
        assert selected.includes(4, 5)

    def test_harder_select(self):
        def sel(e, s):
            return (e, s) in likes

        likes = XSet.classical_set((3, 4, 5))
        haves = XSet.classical_set((1, 2, 3, 4, 5, 6, 7))
        result: XSet = haves.select(sel)
        assert result.excludes(1, None)
        assert result.excludes(2, None)
        assert result.includes(3, None)
        assert result.includes(4, None)
        assert result.includes(5, None)
        assert result.excludes(6, None)

    def test_has_at(self):
        odd_set = XSet([(42, "answer"), (666, XSet.null)])
        assert odd_set.includes(42, "answer")
        assert odd_set.includes(666, XSet.null)
        assert odd_set.includes(666, None)
        assert not odd_set.includes(42, None)

    def test_bool(self):
        assert not XSet.null
        assert not XSet([])
        assert XSet.null == XSet([])
        assert XSet.classical_set((1, 2, 3))

    def test_frozen_operators(self):
        s1 = frozenset(("a", "b", "c"))
        s2 = frozenset(("x", "y"))
        s3 = s1 | s2
        assert s3 == {"a", "x", "c", "b", "y"}
        s2 |= s1
        assert s2 == s3

    def test_syntax(self):
        a = {"last": "hill"}
        # x = "last": "hill" unfortunately can't say this.
        m = max((1, 2, 3, 4))
        assert m == 4

    def test_project(self):
        ron = XSet([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        ron_name = XSet([("jeffries", "last"), ("ron", "first")])
        chet = XSet([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        chet_name = XSet([("chet", "first"), ("hendrickson", "last")])
        hill = XSet([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        print(personnel)
        fields = XSet.classical_set(("first", "last"))
        result = personnel.project(fields)
        print(result)
        assert result.includes(ron_name, None)
        assert result.includes(chet_name, None)

    def test_invalid_xset(self):
        with pytest.raises(AttributeError):
            bad = XSet([1, 2, 3])

    def test_hacked_n_tuple(self):
        n_tuple = ("a", "b", "c")
        test_set = XSet.tuple_set(n_tuple)
        impl = X_tuple(n_tuple)
        test_set.contents = impl  # Jam it in there
        assert test_set.includes("a", 1)
        assert test_set.includes("c", 3)
        assert test_set.excludes("a", None)
        assert test_set.excludes("a", 3)
        assert test_set.excludes("d", 4)


