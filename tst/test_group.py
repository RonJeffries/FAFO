from collections import defaultdict

from set_builder import SetBuilder
from xset import XSet


def find(group_dictionary, department, job):
    for key_set in group_dictionary:
        d = key_set['department']
        j = key_set['job']
        if d == department and j == job:
            return group_dictionary[key_set]
    return None


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
        it_serfs = find(group_dictionary, 'it', 'serf')
        assert len(it_serfs) == 2
        for peep, s in it_serfs:
            assert peep['job'] == 'serf'

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

