from xflat import XFlat
from xset import XSet


class TestXFlat:
    def test_slicing(self):
        record = 'Jeffries    Ronald      Boss      '
        first = record[12:24]
        assert first == 'Ronald      '

    def test_make_symbol_table(self):
        def make_symbols(names_and_lengths):
            it = iter(names_and_lengths)
            by_two = zip(it, it)
            start = 0
            field_definitions = []
            for symbol, length in by_two:
                field_definitions.append((symbol, start, start+length))
                start += length
            return field_definitions
        info = ("last", 12, "first", 10, "job", 8)
        symbols = make_symbols(info)
        s1, s2, s3 = symbols
        assert s1 == ("last", 0, 12)
        assert s2 == ("first", 12, 22)
        assert s3 == ("job", 22, 30)

    def test_unpack(self):
        def field_set(record, symbols):
            result = ((record[start:finish].strip(), name) for name, start, finish in symbols)
            return XSet(result)
        record = 'Jeffries    Ronald      Boss        '
        symbols = (("last", 0, 12), ("first", 12, 24), ("job", 24, 36))
        fields = field_set(record, symbols)
        assert fields.includes("Jeffries", "last")
        assert fields.includes("Ronald", "first")
        assert fields.includes("Boss", "job")

    def test_flat_set_makes_fields(self):
        f1, f2, f3 = XFlat.fields(("last", 12, "first", 10, "job", 20))
        assert f1 == ("last", 0, 12)
        assert f2 == ("first", 12, 22)
        assert f3 == ("job", 22, 42)

    def test_drive_out_init(self):
        fields = XFlat.fields(("last", 12, "first", 10, "job", 20))
        record = 'Jeffries    Ronald    Wizard              '
        flat = XFlat(fields, record)

    def test_contains(self):
        fields = XFlat.fields(("last", 12, "first", 10, "job", 20))
        record = 'Jeffries    Ronald    Wizard              '
        flat = XFlat(fields, record)
        assert ('Jeffries', 'last') in flat
        assert ('Ron', 'first') not in flat
        assert ('Wizard', 'job') in flat




