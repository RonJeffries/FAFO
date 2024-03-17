from collections import defaultdict

from set_builder import SetBuilder
from ximpl import XImplementation
from xset import XSet


class XGroup(XImplementation):
    def __init__(self, group_dictionary):
        self._dict = group_dictionary

    def __iter__(self):
        for group_keys, records in self._dict.items():
            result = XSet.from_tuples(((group_keys, 'keys'), (tuple(records), 'values')))
            yield result, XSet.null

    def __hash__(self):
        return hash(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return 'XGroup()'


class TestGroup:
    def test_group(self):
        j1 = SetBuilder()\
            .put("jeffries","last")\
            .put("ron", "first")\
            .set()
        j2 = SetBuilder()\
            .put("jeffries","last")\
            .put("tom", "first")\
            .set()
        h1 = SetBuilder()\
            .put("hendrickson","last")\
            .put("chet", "first")\
            .set()
        h2 = SetBuilder()\
            .put("hendrickson","last")\
            .put("sue", "first")\
            .set()
        peeps = XSet.n_tuple((j1, j2, h1, h2))
        group = dict()
        for e,s in peeps:
            last = e["last"]
            folx = group.get(last, list())
            folx.append((e,s))
            group[last] = folx
        report = "\n"
        for last in group:
            report += last + "\n"
            for peep, s in group[last]:
                report += "    " + peep["first"] + "\n"
        expected = """
jeffries
    ron
    tom
hendrickson
    chet
    sue
"""
        assert report == expected

    def test_two_keys(self):
        peeps = self.build_peeps()
        scopes = SetBuilder()\
            .put("department", "department")\
            .put("job", "job")\
            .set()
        group_dictionary = defaultdict(list)
        for person, scope in peeps:
            keys = person.re_scope(scopes)
            group_dictionary[keys].append((person, scope))
        it_serfs = self.find(group_dictionary, 'it', 'serf')
        assert len(it_serfs) == 2
        for peep, s in it_serfs:
            assert peep['job'] == 'serf'
        # print()
        # for key_set, records in group_dictionary.items():
        #     d = key_set['department']
        #     j = key_set['job']
        #     print(f'dept {d} job {j}')
        #     for e,s in records:
        #         print(f"    {s}: {e['department']}, {e['job']}, {e['pay']}")
        # assert False

    def find(self, group_dictionary, department, job):
        for key_set in group_dictionary:
            d = key_set['department']
            j = key_set['job']
            if d == department and j == job:
                return group_dictionary[key_set]
        return None

    def build_peeps(self):
        e1 = SetBuilder() \
            .put("it", "department") \
            .put("serf", "job") \
            .put(1000, "pay") \
            .set()
        e2 = SetBuilder() \
            .put("it", "department") \
            .put("serf", "job") \
            .put(1100, "pay") \
            .set()
        e3 = SetBuilder() \
            .put("it", "department") \
            .put("sdet", "job") \
            .put(10000, "pay") \
            .set()
        e4 = SetBuilder() \
            .put("it", "department") \
            .put("sdet", "job") \
            .put(11000, "pay") \
            .set()
        e5 = SetBuilder() \
            .put("sales", "department") \
            .put("closer", "job") \
            .put(1000, "pay") \
            .set()
        e6 = SetBuilder() \
            .put("sales", "department") \
            .put("closer", "job") \
            .put(1100, "pay") \
            .set()
        e7 = SetBuilder() \
            .put("sales", "department") \
            .put("prospector", "job") \
            .put(10000, "pay") \
            .set()
        e8 = SetBuilder() \
            .put("sales", "department") \
            .put("prospector", "job") \
            .put(11000, "pay") \
            .set()
        peeps = XSet.n_tuple((e1, e2, e3, e4, e5, e6, e7, e8))
        return peeps

    def test_build_x_group(self):
        peeps = self.build_peeps()
        scopes = SetBuilder()\
            .put("department", "department")\
            .put("job", "job")\
            .set()
        group_dictionary = defaultdict(list)
        for person, scope in peeps:
            keys = person.re_scope(scopes)
            group_dictionary[keys].append((person, scope))
        x_group = XGroup(group_dictionary)
        group_set = XSet(x_group) # contains pairs of XSets with scopes 'keys' and 'values'
        xset_it = iter(group_set)
        rec, s = next(xset_it) # pair with scopes 'keys' and 'values'
        keys = rec['keys']
        assert keys['department'] == 'it'
        assert keys['job'] == 'serf'
        # x2, s = next(xset_it)
        # assert x2['department'] == 'it'
        # assert x2['job'] == 'sdet'
        # x3, s = next(xset_it)
        # assert x3['department'] == 'sales' and x3['job'] == 'closer'

