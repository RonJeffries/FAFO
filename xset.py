from collections import namedtuple
from typing import Self

Atom = namedtuple("Atom", ["element", "scope"])


class XSet:
    null = None
    @classmethod
    def classical_set(cls, a_list) -> Self:
        null = cls([])
        wrapped = [Atom(item, null) for item in a_list]
        return cls(wrapped)

    @classmethod
    def tuple_set(cls, a_list) -> Self:
        wrapped = [Atom(item, index+1) for index, item in enumerate(a_list)]
        return cls(wrapped)

    def __init__(self, a_list):
        self.contents = frozenset(a_list)

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
        atom = Atom(element, scope if scope else self.null)
        return atom in self

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
        new_atoms = [Atom(field, field_name)
                     for field, field_name in record_element.contents
                     for desired_field_name, _ in field_selector.contents
                     if desired_field_name == field_name]
        return XSet(new_atoms)

    def restrict(self, other) -> Self:
        if not isinstance(other, self.__class__):
            return NotImplemented

        def other_has_match(our_atom):
            return any((other_item.element.is_subset(our_atom.element) for other_item in other.contents))
        return self.select(other_has_match)

    def select(self, cond) -> Self:
        return XSet((candidate_atom for candidate_atom in self.contents if cond(candidate_atom)))


XSet.null = XSet([])
# end of XSet ----------------------
