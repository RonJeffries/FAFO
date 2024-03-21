from stats_maker import StatsMaker
from xset import XSet


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

    def test_stats_given_record(self):
        stats = StatsMaker("pay")
        record = XSet.from_tuples(((1000, 'pay'),))
        stats.record(record)
        assert stats._count == 1
        assert stats._sum == 1000

