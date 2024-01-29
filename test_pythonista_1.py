import pytest
from collections import namedtuple


def test_tagset_exists():
    ts = TagSet()


def test_add():
    ts = TagSet()
    ts.add_at("ron", "author")
    assert ts.has_at("ron", "author")


def test_subset():
    s1 = TagSet()
    s1.add_at("ron", "author")
    s2 = TagSet()
    s2.add_at("bill", "author")
    s2.add_at("ron", "author")

    assert s1.is_subset(s2)
    assert not s2.is_subset(s1)


Atom = namedtuple("Atom", ["value", "name"])


class TagSet:
    def __init__(self):
        self._cont = set()

    def add_at(self, value, name):
        self._cont.add(Atom(value, name))

    def has_at(self, v, n):
        return (v, n) in self._cont

    # return any([value == v and name == n for value, name in self._cont])

    def is_subset(self, s):
        # return all([s.has_at(v, n) for v, n in self._cont])
        return self._cont.issubset(s._cont)
