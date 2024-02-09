from collections import namedtuple
from typing import Self

# Atom = namedtuple("Atom", ["element", "scope"])


class XSet:
    null = None

    @classmethod
    def classical_set(cls, a_list) -> Self:
        null = cls([])
        wrapped = [(item, null) for item in a_list]
        return cls(wrapped)

    @classmethod
    def tuple_set(cls, a_list) -> Self:
        wrapped = [(item, index+1) for index, item in enumerate(a_list)]
        return cls(wrapped)

    def __init__(self, a_list):
        def is_2_tuple(a):
            return isinstance(a, tuple) and len(a) == 2

        self.contents = frozenset(a_list)
        if not all(is_2_tuple(a) for a in self.contents):
            raise AttributeError

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.contents == other.contents
        else:
            return NotImplemented

    def __repr__(self):
        if self == self.null:
            return "∅"
        else:
            return f"XSet({self.contents})"

    def __hash__(self):
        return hash(self.contents)

    def __iter__(self):
        return self.contents.__iter__()

    def __bool__(self):
        return bool(self.contents)

    def excludes(self, element, scope) -> bool:
        return not self.includes(element, scope)

    def includes(self, element, scope) -> bool:
        if not scope:
            scope = self.null
        return (element, scope) in self

    def is_subset(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.contents.issubset(other.contents)
        else:
            return NotImplemented

    def project(self, field_selector: Self) -> Self:
        projected = [self.project_one_record(record_element, field_selector)
                     for record_element, record_scope in self.contents]
        return XSet.classical_set(projected)

    def project_one_record(self, record_element, field_selector):
        new_atoms = [(field, field_name)
                     for field, field_name in record_element.contents
                     for desired_field_name, _ in field_selector.contents
                     if desired_field_name == field_name]
        return XSet(new_atoms)

    def restrict(self, restrictor) -> Self:
        def other_has_match(e, s):
            return any((e_r.is_subset(e) for e_r, s_r in restrictor))

        if not isinstance(restrictor, self.__class__):
            return NotImplemented
        return self.select(other_has_match)

    def select(self, cond) -> Self:
        return XSet(((e, s) for e, s in self.contents if cond(e, s)))


XSet.null = XSet([])
# end of XSet ----------------------
