import pytest


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

    def test_show_sets_are_insufficient_for_xst(self):
        r1 = {("jeffries", "last"), ("ron", "first")}
        r2 = {("chet", "first"), ("hendrickson", "last")}
        with pytest.raises(TypeError):
            _personnel = {r1, r2}

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

    def test_frozen_removes_duplicates(self):
        s = frozenset([1, 2, 1, 2])
        assert len(s) == 2

    def test_frozen_operators(self):
        s1 = frozenset(("a", "b", "c"))
        s2 = frozenset(("x", "y"))
        s3 = s1 | s2
        assert s3 == {"a", "x", "c", "b", "y"}
        s2 |= s1
        assert s2 == s3

    def test_syntax(self):
        a = {"last": "hill"}
        assert a["last"] == 'hill'
        # x = "last": "hill" unfortunately can't say this.
        m = max((1, 2, 3, 4))
        assert m == 4

    def test_slice(self):
        a = 'abcdefghi'
        d = a[3:6]
        assert d == "def"
        assert isinstance(d, str)
        s = slice(3, 6)
        d2 = a[s]
        assert d2 == 'def'

    def test_too_many_next(self):
        things = [1, 2, 3]
        it = iter(things)
        _thing1 = next(it)
        _thing1 = next(it)
        _thing1 = next(it)
        with pytest.raises(StopIteration):
            _thing1 = next(it)

    def test_generator(self):
        def lots():
            n = 0
            while True:
                yield n
                n += 1

        x = lots()
        next(x)
        next(x)
        nxt = next(x)
        assert nxt == 2

    def test_bound_method_pytest_message(self):
        class Foo:
            def __init__(self, arg):
                self.arg = arg

            def includes(self, arg):
                return arg == self.arg

        foo = Foo(3)
        assert not foo.includes(5), "did not include 5"

    def test_type_string(self):
        assert type("ethel") is not int

    def test_how_in_fails(self):
        x = 37
        with pytest.raises(TypeError):
            assert 5 in x
