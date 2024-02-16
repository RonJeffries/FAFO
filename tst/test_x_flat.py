from itertools import product
from os.path import expanduser, isfile

from x_impl import XImplementation
from xflat import XFlat
from xset import XSet


class XFlatFileIterator:
    def __init__(self, flat_file):
        self.file = flat_file
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        rec = self.file.get_record(self.index)
        if rec == '':
            raise StopIteration
        else:
            self.index += 1
            flat_set = XSet(XFlat(self.file.fields, rec))
            return flat_set, self.index


class XFlatFile(XImplementation):
    def __init__(self, file_path, fields):
        self.file_path = file_path
        self.fields = fields
        field_def = self.fields[-1]
        self.record_length = field_def[-1]

    def __contains__(self, item):
        de, ds = item
        for e,s in self:
            if de == e and ds == s:
                return True
        return False

    def __iter__(self):
        return XFlatFileIterator(self)

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

    def test_repr(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        assert repr(ff) == 'XFlatFile(~/Desktop/job_db)'

    def test_ff_contains(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        flat_set = XSet(ff)
        flat_iter = iter(flat_set)
        flat_rec, index = next(flat_iter)
        assert flat_rec.includes('jeffries', 'last')
        # result = flat_set.includes(flat_set, index)
        # assert result






