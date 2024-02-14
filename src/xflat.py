class XFlat:
    @classmethod
    def fields(cls, names_and_lengths):
        it = iter(names_and_lengths)
        by_two = zip(it, it)
        start = 0
        field_definitions = [(symbol, start, start := start + length) for symbol, length in by_two]
        return field_definitions
