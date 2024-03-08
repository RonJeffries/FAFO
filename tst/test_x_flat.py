from datetime import datetime
from itertools import product
from os.path import expanduser, isfile
from xflat import XFlat, XFlatFile
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

    def test_flat_set(self):
        fields = XFlat.fields(("last", 12, "first", 10, "job", 20))
        record = 'Jeffries    Ronald    Wizard              '
        flat = XFlat(fields, record)
        flat_record = XSet(flat)
        assert flat_record.includes('Jeffries', 'last')


    def test_multiple_same_name(self):
        fields = XFlat.fields(('pay', 4, 'pay', 4))
        record = 'abcdefgh'
        flat = XFlat(fields, record)
        flat_set = XSet(flat)
        assert flat_set.includes('abcd', 'pay')
        assert flat_set.includes('efgh', 'pay')

    def test_iteration(self):
        # this test assumes that the XFlat will produce fields in the order defined.
        # this is perhaps set-theoretically weird.
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

    def test_uses_scope_set(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        scopes = XSet.from_tuples(((107, 1), (932, 2)))
        ff = XFlatFile(path, fields, scopes)
        ff_set = XSet(ff)
        assert len(ff_set) == 2
        e, s = ff_set.select(lambda e, s: s == 1).pop()
        assert e.includes('amy', 'first')
        assert any(s == 1 and e.includes('amy', 'first') for e,s in ff_set)
        assert any(s == 2 and e.includes('janet', 'first') for e,s in ff_set)
        assert all(e.includes('amy', 'first') for e,s in ff_set if s == 1)
        assert all(e.includes('janet', 'first') for e,s in ff_set if s == 2)
        amy = ff_set.select(lambda e, s: s == 1 and e.includes('amy', 'first'))
        assert len(amy) == 1

    def test_uses_named_scope(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        scopes = XSet.from_tuples(((107, "amy"), (932, "janet")))
        ff = XFlatFile(path, fields, scopes)
        ff_set = XSet(ff)
        assert len(ff_set) == 2
        e, s = ff_set.select(lambda e, s: s == "amy").pop()
        assert e.includes('amy', 'first')
        assert any(s == 'amy' and e.includes('amy', 'first') for e,s in ff_set)
        assert any(s == 'janet' and e.includes('janet', 'first') for e,s in ff_set)
        assert all(e.includes('amy', 'first') for e,s in ff_set if s == 'amy')
        assert all(e.includes('janet', 'first') for e,s in ff_set if s == 'janet')
        amy = ff_set.select(lambda e, s: s == 'amy' and e.includes('amy', 'first'))
        assert len(amy) == 1


    def test_re_scope(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        r100 = ff.element_at(100)
        r900 = ff.element_at(900)
        ff_set = XSet(ff)
        assert ff_set.includes(r100, 100)
        assert ff_set.includes(r900, 900)
        scopes = XSet.from_tuples(((100, 1), (900, 2)))
        re_scoped = ff_set.re_scope(scopes)
        assert len(re_scoped) == 2
        assert re_scoped.includes(r100, 1)
        assert re_scoped.includes(r900, 2)

    def test_double_re_scope(self):
        scopes = XSet.from_tuples(((100, "fred"), (900, "ethel")))
        new_scopes = XSet.from_tuples((('fred', 'frank'), ('ethel', 'premium')))
        net_scopes = scopes.re_scope(new_scopes)
        expected = XSet.from_tuples(((100, 'frank'), (900, 'premium')))
        assert net_scopes == expected

    def test_scope_set_to_string(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        r100 = ff.element_at(100)
        r900 = ff.element_at(900)
        ff_set = XSet(ff)
        scopes = XSet.from_tuples(((100, "fred"), (900, "ethel")))
        re_scoped = ff_set.re_scope(scopes)
        assert len(re_scoped) == 2
        assert re_scoped.includes(r100, "fred")
        assert re_scoped.includes(r900, "ethel")
        new_scopes = XSet.from_tuples((('fred', 'frank'), ('ethel', 'premium')))
        re_re_scoped = re_scoped.re_scope(new_scopes)
        assert re_re_scoped.includes(r100, "frank")
        assert re_re_scoped.includes(r900, "premium")

    def test_non_integer_re_scope(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        ff_set = XSet(ff)
        scopes = XSet.from_tuples((("hello", "fred"), (13.5, "ethel"), (-1, "neg"), (10000, "big")))
        re_scoped = ff_set.re_scope(scopes)
        assert len(re_scoped) == 0
        assert re_scoped == XSet.null

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

    def test_waste_memory(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        ee = XSet(ff)
        assert ee.cardinality() == 1000
        jeffries = ee.select(lambda e, s: e.includes('jeffries', 'last'))
        assert jeffries.cardinality() == 200
        ron = ee.select(lambda e, s: e.includes('ron', 'first'))
        assert ron.cardinality() == 100
        coder = ee.select(lambda e, s: e.includes('coder', 'job'))
        assert coder.cardinality() == 200
        high = ee.select(lambda e, s: e.includes('12000', 'pay'))
        assert high.cardinality() == 250
        ron_jeffries = ron.intersect(jeffries)
        assert ron_jeffries.cardinality() == 20
        high_coder = coder & high
        assert high_coder.cardinality() == 50
        final = ron_jeffries & high_coder
        assert final.cardinality() == 1
        assert len(final) == 1
        employee, scope = final.pop()
        assert employee.includes('jeffries', 'last')
        assert employee.includes('ron', 'first')
        assert employee.includes('coder', 'job')
        assert employee.includes('12000', 'pay')

    def test_do_not_waste_memory(self):
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        ee = XSet(ff)

        def sel(e, s):
            return (e.includes('jeffries', 'last') and
                    e.includes('ron', 'first') and
                    e.includes('coder', 'job') and
                    e.includes('12000', 'pay'))

        final = ee.select(sel)
        assert final.cardinality() == 1
        employee, scope = final.pop()
        has_jeffries = employee.includes('jeffries', 'last')
        assert has_jeffries
        assert employee.includes('ron', 'first')
        assert employee.includes('coder', 'job')
        assert employee.includes('12000', 'pay')

    def test_rename(self):
        new_names = XSet.from_tuples((('first', 'first_name'), ('last', 'last_name')))
        path = '~/Desktop/job_db'
        fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
        ff = XFlatFile(path, fields)
        ee = XSet(ff)
        renamed = ee.rename_contents(new_names)
        impl = renamed.implementation
        assert isinstance(impl, XFlatFile)
        for person, scope in renamed:
            assert person.includes('jeffries', 'last_name')
            break


    # def test_100_thousand(self):
    #     path = '~/Desktop/job_db'
    #     fields = XFlat.fields(('last', 12, 'first', 12, 'job', 12, 'pay', 8))
    #     ff = XFlatFile(path, fields)
    #     ee = XSet(ff)
    #     start = datetime.now()
    #     for i in range(100):
    #         ron = ee.select(lambda e, s: e.includes('jeffries', 'last'))
    #     elapsed = datetime.now() - start
    #     print(elapsed.total_seconds())
    #     assert elapsed.total_seconds() < 1.5






