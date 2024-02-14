class TestMisc:
    def test_hookup(self):
        assert 3 == 2 + 1

    def test_tuples(self):
        a1 = (1, 2)
        a2 = (2 - 1, 3 - 1)
        a3 = (2, 1)
        assert a1 == a2
        assert not a1 == a3

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
