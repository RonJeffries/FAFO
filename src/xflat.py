from x_impl import XImplementation


class XFlat(XImplementation):
    def __init__(self, fields, record):
        self.fields = fields
        self.record = record

    def __contains__(self, item):
        pass

    def __iter__(self):
        pass

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    @classmethod
    def fields(cls, names_and_lengths):
        it = iter(names_and_lengths)
        by_two = zip(it, it)
        start = 0
        field_definitions = [(symbol, start, start := start + length) for symbol, length in by_two]
        return field_definitions
