from typing import Self

from set_builder import SetBuilder
from xfrozen import XFrozen
from ximpl import XImplementation
from xtuple import XTuple


class XSet:
    null = None

    @classmethod
    def classical_set(cls, a_list) -> Self:
        null = cls.null
        wrapped = [(item, null) for item in a_list]
        return cls.from_tuples(wrapped)

    @classmethod
    def n_tuple(cls, a_list) -> Self:
        return cls(XTuple(a_list))

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

    def __getitem__(self, scope):
        return self.get(scope)

    def __hash__(self):
        return hash(self.implementation)

    def __iter__(self):
        for e, s in self.implementation:
            yield e,s

    def __le__(self, other):
        return self.is_subset(other)

    def __len__(self):
        return len(self.implementation)

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
        return len(self)

    def diff(self, other):
        mine = set((e, s) for e, s in self)
        others = set((e, s) for e, s in other)
        remaining = mine - others
        return XSet.from_tuples(remaining)

    def element_set(self):
        return XSet.from_tuples((e, e) for e, s in self)

    def excludes(self, element, scope) -> bool:
        return not self.includes(element, scope)

    def get(self, scope):
        for e, s in self:
            if s == scope:
                return e
        return None

    def includes(self, element, scope) -> bool:
        if scope is None:
            scope = self.null
        return (element, scope) in self.implementation

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
        projected = (record_element.re_scope(projector)
                     for record_element, record_scope in self)
        return XSet.classical_set(projected)

    def rename(self, old_to_new_re_scope_set: Self):
        # renames this set, not its contents sets
        complete_re_scope = self.convert_rename_to_re_scope(old_to_new_re_scope_set)
        return self.re_scope(complete_re_scope)

    def convert_rename_to_re_scope(self, r):
        return self.scope_set() ^ r ^ r.element_set()

    def rename_contents(self, re_scoping_set: Self):
        try:
            return self.implementation.rename_contents(re_scoping_set)
        except AttributeError:
            new_tuples = ((e.rename(re_scoping_set), s) for e, s in self)
            return XSet.from_tuples(new_tuples)

    def re_scope(self, other) -> Self:
        try:
            return self.implementation.re_scope(other)
        except AttributeError:
            return self.generic_re_scope(other)

    def generic_re_scope(self, other):
        tuples = ((e, new) for e, s in self for old, new in other if old == s)
        return XSet.from_tuples(tuples)

    def restrict(self, restrictor) -> Self:
        def other_has_match(e, s):
            return any((e_r.is_subset(e) for e_r, s_r in restrictor))

        if not isinstance(restrictor, self.__class__):
            return NotImplemented
        return self.select(other_has_match)

    def scope_set(self):
        return XSet.from_tuples((s, s) for e, s in self)

    def select(self, cond) -> Self:
        tuples = ((e, s) for e, s in self if cond(e, s))
        return XSet.from_tuples(tuples)

    def sym_diff(self, other):
        return (self - other) | (other - self)

    def union(self, other):
        mine = set(self)
        others = set(other)
        both = mine | others
        return XSet.from_tuples(both)


XSet.null = XSet.from_tuples([])
# end of XSet ----------------------
