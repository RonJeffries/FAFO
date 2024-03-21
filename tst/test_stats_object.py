from xset import XSet


class StatsMaker:
    def __init__(self, name):
        self._name = name
        self._count = 0
        self._sum = 0

    def value(self, number):
        self._count += 1
        self._sum += number

    def statistics(self):
        return XSet.from_tuples(self.tuples())

    def tuples(self):
        tups = []
        tups.append((self._count, self._name+'_count'))
        tups.append((self._sum, self._name+'_sum'))
        tups.append((self.mean(), self._name+'_mean'))
        return tups

    def mean(self):
        return self._sum / self._count


class TestStatsObject:
    def test_stats(self):
        stats = StatsMaker("pay")
        stats.value(1000)
        stats.value(2000)
        stats.value(3000)
        stats.value(4000)
        assert stats._count == 4
        assert stats._sum == 10000

    def test_stats_result_set(self):
        stats = StatsMaker("pay")
        stats.value(1000)
        stats.value(2000)
        stats.value(3000)
        stats.value(4000)
        result = stats.statistics()
        assert result['pay_count'] == 4
        assert result['pay_sum'] == 10000
        assert result['pay_mean'] == 2500.0
