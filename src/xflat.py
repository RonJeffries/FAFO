from x_impl import XImplementation


class XFlat(XImplementation):
    def __init__(self, fields, record):
        self.fields = fields
        self.record = record

    def __contains__(self, item):
        element, scope = item
        for symbol, start, end in self.fields:
            if symbol == scope:
                field = self.record[start:end].strip()
                return field == element
        return False

    def __iter__(self):
        return ((self.record[start:end].strip(), symbol) for symbol, start, end in self.fields)

    def __hash__(self):
        return -1

    def __repr__(self):
        return f"XFlat('{self.record}')"

    @classmethod
    def fields(cls, names_and_lengths):
        it = iter(names_and_lengths)
        by_two = zip(it, it)
        start = 0
        field_definitions = [(symbol, start, start := start + length) for symbol, length in by_two]
        return field_definitions
