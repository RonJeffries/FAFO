from collections import defaultdict
from set_builder import SetBuilder
from xset import XSet


class TestGroup:
    """
    Various experiments leading up to the group_by method.
    """

    def test_group(self):
        j1 = SetBuilder() \
            .put("jeffries", "last") \
            .put("ron", "first") \
            .set()
        j2 = SetBuilder() \
            .put("jeffries", "last") \
            .put("tom", "first") \
            .set()
        h1 = SetBuilder() \
            .put("hendrickson", "last") \
            .put("chet", "first") \
            .set()
        h2 = SetBuilder() \
            .put("hendrickson", "last") \
            .put("sue", "first") \
            .set()
        peeps = XSet.n_tuple((j1, j2, h1, h2))
        group = dict()
        for e, s in peeps:
            last = e["last"]
            folx = group.get(last, list())
            folx.append((e, s))
            group[last] = folx
        report = "\n"
        for last in group:
            report += last + "\n"
            for peep, s in group[last]:
                report += "    " + peep["first"] + "\n"
        expected = ("\n"
                    "jeffries\n"
                    "    ron\n"
                    "    tom\n"
                    "hendrickson\n"
                    "    chet\n"
                    "    sue\n")
        assert report == expected

    def test_two_keys(self):
        peeps = self.build_peeps()
        scopes = SetBuilder() \
            .put("department", "department") \
            .put("job", "job") \
            .set()
        group_dictionary = defaultdict(list)
        for person, scope in peeps:
            keys = person.re_scope(scopes)
            group_dictionary[keys].append((person, scope))
        it_serfs = self.find(group_dictionary, 'it', 'serf')
        assert len(it_serfs) == 2
        for peep, s in it_serfs:
            assert peep['job'] == 'serf'

    @staticmethod
    def find(group_dictionary, department, job):
        for key_set in group_dictionary:
            d = key_set['department']
            j = key_set['job']
            if d == department and j == job:
                return group_dictionary[key_set]
        return None

    @staticmethod
    def build_peeps():
        e1 = SetBuilder() \
            .put("it", "department") \
            .put("joe", "name") \
            .put("serf", "job") \
            .put(1000, "pay") \
            .put(100, "bonus") \
            .set()
        e2 = SetBuilder() \
            .put("it", "department") \
            .put("bob", "name") \
            .put("serf", "job") \
            .put(1100, "pay") \
            .put(110, "bonus") \
            .set()
        e3 = SetBuilder() \
            .put("it", "department") \
            .put("ole", "name") \
            .put("sdet", "job") \
            .put(10000, "pay") \
            .put(1000, "bonus") \
            .set()
        e4 = SetBuilder() \
            .put("it", "department") \
            .put("sam", "name") \
            .put("sdet", "job") \
            .put(11000, "pay") \
            .put(1100, "bonus") \
            .set()
        e5 = SetBuilder() \
            .put("sales", "department") \
            .put("ben", "name") \
            .put("closer", "job") \
            .put(1000, "pay") \
            .put(200, "bonus") \
            .set()
        e6 = SetBuilder() \
            .put("sales", "department") \
            .put("cee", "name") \
            .put("closer", "job") \
            .put(1100, "pay") \
            .put(220, "bonus") \
            .set()
        e7 = SetBuilder() \
            .put("sales", "department") \
            .put("don", "name") \
            .put("prospector", "job") \
            .put(10000, "pay") \
            .put(2000, "bonus") \
            .set()
        e8 = SetBuilder() \
            .put("sales", "department") \
            .put("fay", "name") \
            .put("prospector", "job") \
            .put(11000, "pay") \
            .put(2200, "bonus") \
            .set()
        peeps = XSet.n_tuple((e1, e2, e3, e4, e5, e6, e7, e8))
        return peeps

    def test_group_keys_via_project(self):
        peeps = self.build_peeps()
        fields = XSet.classical_set(("department", "job"))
        keys = peeps.project(fields)
        print()
        lines = []
        for key_set, scope in keys:
            record = []
            for key, value in key_set:
                record.append(f'{value}^{key}')
            lines.append(','.join(sorted(record)))
        report = '\n'.join(sorted(lines))
        expected = ("department^it,job^sdet\n"
                    "department^it,job^serf\n"
                    "department^sales,job^closer\n"
                    "department^sales,job^prospector")
        assert report == expected

    def test_restrict_returns_group_records(self):
        personnel = self.build_peeps()
        fields = XSet.classical_set(("department", "job"))
        groups = personnel.project(fields)
        for group_keys, _g_scope in groups:
            search_set = XSet.classical_set([group_keys])
            selected_people = personnel.restrict(search_set)
            assert len(selected_people) == 2
            department = group_keys['department']
            job = group_keys['job']
            for person, _p_scope in selected_people:
                assert person['department'] == department
                assert person['job'] == job

    def test_build_report(self):
        def details(record, r_scope):
            return f"        {r_scope}: {record['name']} {record['job']}: {record['pay']}"

        print()
        personnel = self.build_peeps()
        get_departments = XSet.classical_set(("department",))
        departments = personnel.project(get_departments)
        department_names = []
        for dept_rec, _dept in departments:
            department_names.append(dept_rec['department'])
        department_names = sorted(department_names)
        report_lines = []
        for dept in department_names:
            report_lines.append("Dept: " + dept)
            dept_rec = XSet.from_tuples([(dept, 'department')])
            dept_set = XSet.classical_set([dept_rec])
            dept_recs = personnel.restrict(dept_set)
            job_names = set()
            for rec, scope in dept_recs:
                job = rec['job']
                job_names.add(job)
            job_names = sorted(job_names)
            for job in job_names:
                report_lines.append("    Job: " + job)
                job_rec = XSet.from_tuples([(job, 'job')])
                job_set = XSet.classical_set([job_rec])
                job_recs = dept_recs.restrict(job_set)
                local_lines = sorted([details(rec, scope) for rec, scope in job_recs])
                report_lines.extend(local_lines)
        report = '\n'.join(report_lines)
        expected = ('Dept: it\n'
                    '    Job: sdet\n'
                    '        3: ole sdet: 10000\n'
                    '        4: sam sdet: 11000\n'
                    '    Job: serf\n'
                    '        1: joe serf: 1000\n'
                    '        2: bob serf: 1100\n'
                    'Dept: sales\n'
                    '    Job: closer\n'
                    '        5: ben closer: 1000\n'
                    '        6: cee closer: 1100\n'
                    '    Job: prospector\n'
                    '        7: don prospector: 10000\n'
                    '        8: fay prospector: 11000')
        assert report == expected

    def test_group_by(self):
        report_lines = []
        personnel = self.build_peeps()
        for dept in personnel.group_by('department'):
            report_lines.append(dept.name)
            for job in dept.values.group_by('job'):
                report_lines.append("    " + job.name)
                for pay in sorted([worker['pay'] for worker, scope in job.values]):
                    report_lines.append("        " + str(pay))
        report = '\n'.join(report_lines)
        expected = ("it\n"
                    "    sdet\n"
                    "        10000\n"
                    "        11000\n"
                    "    serf\n"
                    "        1000\n"
                    "        1100\n"
                    "sales\n"
                    "    closer\n"
                    "        1000\n"
                    "        1100\n"
                    "    prospector\n"
                    "        10000\n"
                    "        11000")
        assert report == expected

    def test_average_by(self):
        report_lines = []
        personnel = self.build_peeps()
        for dept in personnel.group_by('department'):
            report_lines.append(dept.name)
            for job in dept.values.group_by('job'):
                report_lines.append("    " + job.name)
                count = 0
                sum = 0
                for pay in sorted([worker['pay'] for worker, scope in job.values]):
                    count += 1
                    sum += pay
                    report_lines.append("        " + str(pay))
                report_lines.append(f"        avg: {sum / count}")
        report = '\n'.join(report_lines)
        expected = ('it\n'
                    '    sdet\n'
                    '        10000\n'
                    '        11000\n'
                    '        avg: 10500.0\n'
                    '    serf\n'
                    '        1000\n'
                    '        1100\n'
                    '        avg: 1050.0\n'
                    'sales\n'
                    '    closer\n'
                    '        1000\n'
                    '        1100\n'
                    '        avg: 1050.0\n'
                    '    prospector\n'
                    '        10000\n'
                    '        11000\n'
                    '        avg: 10500.0')
        assert report == expected

    def test_statistics(self):
        report_lines = []
        personnel = self.build_peeps()
        for dept in personnel.group_by('department'):
            report_lines.append(dept.name)
            for job in dept.values.group_by('job'):
                report_lines.append("    " + job.name)
                for pay in sorted([worker['pay'] for worker, scope in job.values]):
                    report_lines.append("        " + str(pay))
                stats = job.values.statistics(['pay', 'bonus'])  # just returns the record
                report_lines.append(f"        pay_mean: {stats['pay_mean']}  bonus_mean: {stats['bonus_mean']}")
        report = '\n'.join(report_lines)
        expected = ('it\n'
                    '    sdet\n'
                    '        10000\n'
                    '        11000\n'
                    '        pay_mean: 10500.0  bonus_mean: 1050.0\n'
                    '    serf\n'
                    '        1000\n'
                    '        1100\n'
                    '        pay_mean: 1050.0  bonus_mean: 105.0\n'
                    'sales\n'
                    '    closer\n'
                    '        1000\n'
                    '        1100\n'
                    '        pay_mean: 1050.0  bonus_mean: 210.0\n'
                    '    prospector\n'
                    '        10000\n'
                    '        11000\n'
                    '        pay_mean: 10500.0  bonus_mean: 2100.0')
        assert report == expected

    def test_whole_set(self):
        peeps = self.build_peeps()
        projector = XSet.classical_set(['pay', 'bonus'])
        pay_and_bonus = peeps.project(projector)
        stats = pay_and_bonus.statistics(['pay', 'bonus'])
        assert stats['pay_count'] == 8
        assert stats['pay_sum'] == 46200
        assert stats['pay_mean'] == 46200/8
        assert stats['bonus_count'] == 8
        assert stats['bonus_sum'] == 6930
        assert stats['bonus_mean'] == 6930/8