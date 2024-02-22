from typing import Self

from xfrozen import XFrozen
from ximpl import XImplementation


# Atom = namedtuple("Atom", ["element", "scope"])


class XTupleIterator:
    def __init__(self, x_tuple):
        self.data = x_tuple.data
        self.record = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.record < len(self.data):
            self.record += 1
            return self.data[self.record-1], self.record
        else:
            raise StopIteration


class XTuple:
    def __init__(self, data):
        self.data = data

    def __contains__(self, t):
        if not isinstance(t, tuple):
            return False  # should raise?
        e, s = t
        return isinstance(s, int) and 0 < s <= len(self.data) and self.data[s-1] == e

    def __iter__(self):
        scope = 1
        for e in self.data:
            yield e, scope
            scope += 1


class XSet:
    null = None

    @classmethod
    def classical_set(cls, a_list) -> Self:
        null = cls.null
        wrapped = [(item, null) for item in a_list]
        return cls.from_tuples(wrapped)

    @classmethod
    def n_tuple(cls, a_list) -> Self:
        wrapped = [(item, index+1) for index, item in enumerate(a_list)]
        return cls.from_tuples(wrapped)

    @classmethod
    def from_tuples(cls, tuples):
        def is_2_tuple(a):
            return isinstance(a, tuple) and len(a) == 2

        frozen = frozenset(tuples)  # ensure we didn't get passed a generator
        if not all(is_2_tuple(a) for a in frozen):
            raise AttributeError
        return cls(XFrozen(frozen))

    def __init__(self, an_implementation):
        assert isinstance(an_implementation, XImplementation)
        self.implementation = an_implementation

    def __and__(self, other):
        return self.intersect(other)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.is_subset(other) and other.is_subset(self)
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.implementation)

    def __iter__(self):
        for e, s in self.implementation:
            yield e,s

    def __le__(self, other):
        return self.is_subset(other)

    def __lt__(self, other):
        return self.is_subset(other) and self != other

    def __or__(self, other):
        assert isinstance(other, self.__class__)
        return self.union(other)

    def __repr__(self):
        if self == self.null:
            return "∅"
        else:
            return f"XSet({self.implementation})"

    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        return self.diff(other)

    def __xor__(self, other):
        assert isinstance(other, self.__class__)
        return self.sym_diff(other)

    def cardinality(self):
        count = 0
        for _ignored in self:
            count += 1
        return count

    def diff(self, other):
        mine = set((e, s) for e, s in self)
        others = set((e, s) for e, s in other)
        remaining = mine - others
        return XSet.from_tuples(remaining)

    def element_set(self):
        return XSet.from_tuples((e, e) for e, s in self)

    def excludes(self, element, scope) -> bool:
        return not self.includes(element, scope)

    def includes(self, element, scope) -> bool:
        if scope is None:
            scope = self.null
        try:
            return (element, scope) in self.implementation
        except NotImplemented:
            return any(e == element and s == scope for e, s in self)

    def intersect(self, other):
        return XSet.from_tuples((e, s) for e, s in self if other.includes(e, s))

    def is_subset(self, other) -> bool:
        if isinstance(other, self.__class__):
            return all(other.includes(e, s) for e,s in self)
        else:
            return NotImplemented

    def pop(self):
        it = iter(self)
        return next(it, (None, None))

    def project(self, field_selector: Self) -> Self:
        projector = XSet.from_tuples([(e, e) for e, _ignored in field_selector])
        projected = [record_element.re_scope(projector)
                     for record_element, record_scope in self]
        return XSet.classical_set(projected)

    def rename(self, re_scoping_set: Self):
        # renames this set, not its contents sets
        old_names = self.scope_set()
        replaced_names = re_scoping_set.element_set()
        update = replaced_names | re_scoping_set
        renames = old_names ^ update
        return self.re_scope(renames)

    def rename_contents(self, re_scoping_set: Self):
        try:
            return self.implementation.rename_contents(re_scoping_set)
        except AttributeError:
            new_tuples = ((e.rename(re_scoping_set), s) for e, s in self)
            return XSet.from_tuples(new_tuples)

    def re_scope(self, other) -> Self:
        new_tuples = []
        for e, s in self:
            for old, new in other:
                if old == s:
                    new_tuples.append((e,  new))
        return XSet.from_tuples(new_tuples)

    def restrict(self, restrictor) -> Self:
        def other_has_match(e, s):
            return any((e_r.is_subset(e) for e_r, s_r in restrictor))

        if not isinstance(restrictor, self.__class__):
            return NotImplemented
        return self.select(other_has_match)

    def scope_set(self):
        return XSet.from_tuples((s, s) for e, s in self)

    def select(self, cond) -> Self:
        tuples = list((e, s) for e, s in self if cond(e, s))
        return XSet.from_tuples(tuples)

    def sym_diff(self, other):
        return (self - other) | (other - self)

    def union(self, other):
        mine = set((e, s) for e, s in self)
        others = set((e, s) for e, s in other)
        both = mine | others
        return XSet.from_tuples(both)


XSet.null = XSet.from_tuples([])
# end of XSet ----------------------
