import pytest

from xfrozen import XFrozen
from ximpl import XImplementation
from xset import XSet, XTuple


class TestXST:
    def test_classical_is_subset(self):
        c1 = XSet.classical_set((1, 2, 3, 4, 5))
        c2 = XSet.classical_set((2, 4))
        c3 = XSet.classical_set((1, 6))
        assert c2.is_subset(c1)
        assert not c3.is_subset(c1)

    def test_is_subset(self):
        r1 = XSet.from_tuples([("jeffries", "last"), ("ron", "first")])
        r2 = XSet.from_tuples([("jeffries", "last")])
        assert r2.is_subset(r1)
        assert not r1.is_subset(r2)

    def test_xset_in(self):
        list1 = [("x", 1), ("y", 2)]
        list2 = [("y", 2), ("x", 1)]
        assert list1 != list2
        set1 = XSet.from_tuples(list1)
        set2 = XSet.from_tuples(list2)
        assert set1 == set2
        set3 = XSet.from_tuples([("z", 1), ("y", 2)])
        assert set1 != set3

    def test_xset_records_in(self):
        r1 = XSet.from_tuples([("jeffries", "last"), ("ron", "first")])
        r2 = XSet.from_tuples([("chet", "first"), ("hendrickson", "last")])
        r2rev = XSet.from_tuples([("hendrickson", "last"), ("chet", "first")])
        r3 = XSet.from_tuples([("hill", "last"), ("geepaw", "first")])
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
        ron = XSet.from_tuples([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        chet = XSet.from_tuples([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        hill = XSet.from_tuples([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        boss_record = XSet.from_tuples([("boss", "job")])
        boss_set = XSet.classical_set([boss_record])
        bosses = personnel.restrict(boss_set)
        assert isinstance(bosses, XSet)
        # assert len(bosses.implementation) > 0
        assert bosses.includes(ron, None)
        assert bosses.includes(chet, None)
        assert bosses.excludes(hill, None)

    def test_xset_tuple_restrict(self):
        ron = XSet.from_tuples([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        chet = XSet.from_tuples([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        hill = XSet.from_tuples([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.n_tuple([ron, chet, hill])
        boss_record = XSet.from_tuples([("boss", "job")])
        boss_set = XSet.n_tuple([boss_record])
        bosses = personnel.restrict(boss_set)
        assert bosses.includes(ron, 1)
        assert bosses.includes(chet, 2)
        assert bosses.excludes(hill, 3)

    def test_xset_restrict_again(self):
        ron = XSet.from_tuples([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        chet = XSet.from_tuples([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        hill = XSet.from_tuples([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        serf_record = XSet.from_tuples([("serf", "job")])
        serf_set = XSet.classical_set([serf_record])
        serfs: XSet = personnel.restrict(serf_set)
        assert serfs.excludes(ron, None)
        assert serfs.excludes(chet, None)
        assert serfs.includes(hill, None)

    def test_select(self):
        def sel(e, s):
            print("checking", e, s, e > 3)
            return e > 3
        s1 = XSet.n_tuple((0, 1, 2, 3, 4, 5, 6))
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

    def test_includes(self):
        odd_set = XSet.from_tuples([(42, "answer"), (666, XSet.null)])
        assert odd_set.includes(42, "answer")
        assert odd_set.includes(666, XSet.null)
        assert odd_set.includes(666, None)
        assert not odd_set.includes(42, None)

    def test_project(self):
        ron = XSet.from_tuples([("jeffries", "last"), ("ron", "first"), ("boss", "job")])
        ron_name = XSet.from_tuples([("jeffries", "last"), ("ron", "first")])
        chet = XSet.from_tuples([("chet", "first"), ("hendrickson", "last"), ("boss", "job")])
        chet_name = XSet.from_tuples([("chet", "first"), ("hendrickson", "last")])
        hill = XSet.from_tuples([("hill", "last"), ("geepaw", "first"), ("serf", "job")])
        personnel = XSet.classical_set([ron, chet, hill])
        print(personnel)
        fields = XSet.classical_set(("first", "last"))
        result = personnel.project(fields)
        print(result)
        assert result.includes(ron_name, None)
        assert result.includes(chet_name, None)

    def test_invalid_xset(self):
        with pytest.raises(AttributeError):
            bad = XSet.from_tuples([1, 2, 3])

    def test_isinstance(self):
        xf = XFrozen(frozenset())
        assert isinstance(xf, XFrozen)
        the_set = XSet.from_tuples([('joe', 'first'), ('smith', 'last')])
        assert isinstance(the_set.implementation, XFrozen)
        assert isinstance(the_set.implementation, XImplementation)

    def test_list_is_implementation(self):
        # this is why we require an XImplementation
        # ramifications of this are not at all clear.
        rec = [('smith', 'last'), ('sinjin', 'first')]
        seq_set = XSet.from_tuples(rec)
        seq_set.implementation = rec  #  just jam it in there
        assert seq_set.includes('smith', 'last')
        assert seq_set.excludes('st. john', 'first')

    def test_list_not_allowed(self):
        rec = [('smith', 'last'), ('sinjin', 'first')]
        with pytest.raises(AssertionError):
            seq_set = XSet(rec)

    def test_hacked_n_tuple(self):
        n_tuple = ("a", "b", "c")
        test_set = XSet.n_tuple(n_tuple)
        impl = XTuple(n_tuple)
        test_set.implementation = impl  # Jam it in there
        assert test_set.includes("a", 1)
        assert test_set.includes("c", 3)
        assert test_set.excludes("a", None)
        assert test_set.excludes("a", 3)
        assert test_set.excludes("d", 4)
        assert test_set.excludes("c", 0)
        assert test_set.excludes("b", 0)
        assert test_set.excludes("a", 0)
        assert test_set.excludes("c", -1)
        assert test_set.excludes("b", -1)
        assert test_set.excludes("a", -1)
        tally = 0
        for e,s in test_set:
            assert e in ['a', 'b', 'c']
            tally += s
        assert tally == 6

    def test_re_scope(self):
        s = XSet.from_tuples((('first', 'first_name'), ('last', 'last_name')))
        z = XSet.from_tuples((('ron', 'first'), ('jeffries', 'last'), ('serf', 'job')))
        r = z.re_scope(s)
        assert r.includes('jeffries', 'last_name')
        assert r.includes('ron', 'first_name')
        count = 0
        for _e, _s in r:
            count += 1
        assert count == 2

    @pytest.mark.skip("waiting for set operation")
    def test_rename(self):
        new_names = XSet.from_tuples((('first', 'first_name'), ('last', 'last_name')))
        person = XSet.from_tuples((('ron', 'first'), ('jeffries', 'last'), ('serf', 'job')))
        renamed = person.rename(new_names)
        assert renamed.includes('jeffries', 'last_name')
        assert renamed.includes('ron', 'first_name')
        assert renamed.includes('serf', 'job')

    def test_scope_set(self):
        person = XSet.from_tuples((('ron', 'first'), ('jeffries', 'last'), ('serf', 'job')))
        scopes = person.scope_set()
        assert scopes.includes('first', 'first')
        assert scopes.includes('last', 'last')
        assert scopes.includes('job', 'job')

    def test_element_set(self):
        new_names = XSet.from_tuples((('first', 'first_name'), ('last', 'last_name')))
        old_names = new_names.element_set()
        assert old_names.includes('first', 'first')
        assert old_names.includes('last', 'last')




