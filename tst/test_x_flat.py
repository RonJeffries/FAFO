from itertools import product
from os.path import expanduser, isfile
from xflat import XFlat
from ximpl import XImplementation
from xset import XSet


class XFlatFileIterator:
    def __init__(self, flat_file, generator):
        self.file = flat_file
        self.scope_gen = generator()

    def __iter__(self):
        return self

    def __next__(self):
        scope = next(self.scope_gen)
        element_tuple = (rec := self.file.element_at(scope), scope)
        if rec is None:
            raise StopIteration
        else:
            return element_tuple


class XFlatFile(XImplementation):
    def __init__(self, file_path, fields):
        self.file_path = file_path
        self.fields = fields
        field_def = self.fields[-1]
        self.record_length = field_def[-1]

    def __contains__(self, item):
        de, ds = item
        return de == self.element_at(ds)

    def __iter__(self):
        def lots():
            n = 1
            while True:
                yield n
                n += 1
        return XFlatFileIterator(self, lots)

    def __hash__(self):
        return hash((self.file_path, self.fields))

    def __repr__(self):
        return f'XFlatFile({self.file_path})'

    def get_record(self, index):
        seek_address = index*self.record_length
        with open(expanduser(self.file_path), "r") as f:
            f.seek(seek_address)
            rec = f.read(self.record_length)
        return rec

    def element_at(self, scope):
        if not isinstance(scope, int) or scope < 1:
            return None
        rec = self.get_record(scope - 1)
        if rec == '':
            return None
        return XSet(XFlat(self.fields, rec))


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
            result = [(record[start:finish].strip(), name) for name, start, finish in symbols]
            return XSet.from_tuples(result)
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

    def test_multiple_same_name(self):
        fields = XFlat.fields(('pay', 4, 'pay', 4))
        record = 'abcdefgh'
        flat = XFlat(fields, record)
        flat_set = XSet(flat)
        for e,s, in flat_set:
            print(e, s)
        assert flat_set.includes('abcd', 'pay')
        assert flat_set.includes('efgh', 'pay')

    def test_iteration(self):
        fields = XFlat.fields(("last", 12, "first", 10, "job", 20))
        record = 'Jeffries    Ronald    Wizard              '
        flat = XFlat(fields, record)
        elements = []
        scopes = []
        for e,s in flat:
            elements.append(e)
            scopes.append(s)
        assert elements == ['Jeffries', 'Ronald', 'Wizard']
        assert scopes == ['last', 'first', 'job']

    def test_padded_line(self):
        author = "ron"
        topic = "math"
        student = "dorothy"
        line = f'{author:12s}{topic:12s}{student:12s}'
        assert len(line) == 36
        assert line == 'ron         math        dorothy     '

    def test_make_flat_file(self):
        path = expanduser('~/Desktop/job_db')
        if isfile(path):
            return
        lasts = ["jeffries", "wake", "hill", "hendrickson", "iam"]
        firsts = ["ron", "bill", "geepaw", "chet", "sam", "amy", "janet", "susan", "beyonce", "taylor"]
        jobs = ['serf', 'boss', 'clerk', 'coder', 'architect']
        pays = [9000, 10000, 11000, 12000]
        with open(path, "w") as db:
            for l, f, j, p in product(lasts, firsts, jobs, pays):
                db.write(f'{l:12s}{f:12s}{j:12s}{p:8d}')

    def test_x_flatfile(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        assert ff.record_length == 44
        ff_set = XSet(ff)
        count = 0
        record_number_sum = 0
        for record, record_number in ff_set:
            count += 1
            record_number_sum += record_number
        assert count == 1000
        assert record_number_sum == 500500

    def test_iterate_twice(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        ff_set = XSet(ff)
        count = 0
        for _e, _s in ff_set:
            count += 1
        assert count == 1000
        count = 0
        for _e, _s in ff_set:
            count += 1
        assert count == 1000

    def test_custom_iteration(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        ff_set = XSet(ff)
        it = iter(ff_set)
        count = 0
        try:
            while (next(it)):
                count += 1
        except StopIteration:
            pass
        assert count == 1000


    def test_repr(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        assert repr(ff) == 'XFlatFile(~/Desktop/job_db)'

    def test_ff_element_at(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        e1 = ff.element_at(1)
        assert e1.includes('jeffries', 'last')
        assert e1.includes('9000', 'pay')
        assert ff.element_at(0) is None
        assert ff.element_at(1001) is None
        assert ff.element_at('three') is None

    def test_ff_contains(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        flat_set = XSet(ff)
        flat_iter = iter(flat_set)
        flat_rec, index = next(flat_iter)
        assert flat_rec.includes('jeffries', 'last')
        assert flat_set.includes(flat_rec, index)

    def test_ff_select(self):
        def sel(person, s):
            return (person.includes('iam', 'last') and
                    person.includes('taylor', 'first') and
                    person.includes('serf', 'job'))

        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        flat_set = XSet(ff)
        result = flat_set.select(sel)
        count = 0
        for person, s in result:
            count += 1
        assert count == 4

    def test_project(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        flat_set = XSet(ff)
        fields = XSet.classical_set(["last"])
        projected = flat_set.project(fields)
        count = 0
        for person, s in projected:
            count += 1
        assert count == 5





