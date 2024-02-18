from collections import namedtuple
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
        return XTupleIterator(self)


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

        concrete = list(tuples)  # ensure we didn't get passed a generator
        if not all(is_2_tuple(a) for a in concrete):
            raise AttributeError
        return cls(XFrozen(frozenset(concrete)))

    def __init__(self, an_implementation):
        assert isinstance(an_implementation, XImplementation)
        self.implementation = an_implementation

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.is_subset(other) and other.is_subset(self)
        else:
            return NotImplemented

    def __repr__(self):
        if self == self.null:
            return "∅"
        else:
            return f"XSet({self.implementation})"

    def __hash__(self):
        return hash(self.implementation)

    def __iter__(self):
        return self.implementation.__iter__()

    def excludes(self, element, scope) -> bool:
        return not self.includes(element, scope)

    def includes(self, element, scope) -> bool:
        if scope is None:
            scope = self.null
        try:
            return (element, scope) in self.implementation
        except NotImplemented:
            return any(e == element and s == scope for e, s in self)

    def is_subset(self, other) -> bool:
        if isinstance(other, self.__class__):
            return all(other.includes(e, s) for e,s in self)
        else:
            return NotImplemented

    def project(self, field_selector: Self) -> Self:
        projected = [self.project_one_record(record_element, field_selector)
                     for record_element, record_scope in self]
        return XSet.classical_set(projected)

    def project_one_record(self, record_element, field_selector):
        new_atoms = [(field, field_name)
                     for field, field_name in record_element
                     for desired_field_name, _ in field_selector
                     if desired_field_name == field_name]
        return XSet.from_tuples(new_atoms)

    def restrict(self, restrictor) -> Self:
        def other_has_match(e, s):
            return any((e_r.is_subset(e) for e_r, s_r in restrictor))

        if not isinstance(restrictor, self.__class__):
            return NotImplemented
        return self.select(other_has_match)

    def select(self, cond) -> Self:
        tuples = list((e, s) for e, s in self if cond(e, s))
        return XSet.from_tuples(tuples)


XSet.null = XSet.from_tuples([])
# end of XSet ----------------------
