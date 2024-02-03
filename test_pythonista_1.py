from collections import namedtuple


def test_tag_set_exists():
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

def test_bad_subset():
    s1 = TagSet()
    assert not s1.is_subset(37)



Atom = namedtuple("Atom", ["value", "name"])


class TagSet:
    def __init__(self):
        self._cont = set()

    def add_at(self, value, name):
        self._cont.add(Atom(value, name))

    def get_file_name(self):
        ts = next(filter(lambda pair: pair.name == "t", self._cont))
        remainder = self._cont.copy()
        remainder.discard(ts)
        tags = [pair for pair in remainder]
        tags.sort(key=lambda p: (p.name, p.value))
        tags.insert(0, ts)
        strings = [f"{t.name}-{t.value}" for t in tags]
        return "_".join(strings) + "_.curry"

    def has_at(self, v, n):
        return (v, n) in self._cont

    # return any([value == v and name == n for value, name in self._cont])

    def is_subset(self, s):
        return self._cont.issubset(s._cont) if isinstance(s, self.__class__) else False
        # consider double dispatch? Still would have to check type. Used to use try:except:
