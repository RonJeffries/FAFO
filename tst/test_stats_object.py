from stats_maker import StatsAccumulator
from xset import XSet


class TestStatsObject:
    def test_stats(self):
        stats = StatsAccumulator("pay")
        stats.value(1000)
        stats.value(2000)
        stats.value(3000)
        stats.value(4000)
        assert stats._count == 4
        assert stats._sum == 10000

    def test_stats_result_set(self):
        stats = StatsAccumulator("pay")
        stats.value(1000)
        stats.value(2000)
        stats.value(3000)
        stats.value(4000)
        result = stats.statistics()
        assert result['pay_count'] == 4
        assert result['pay_sum'] == 10000
        assert result['pay_mean'] == 2500.0

    def test_stats_given_record(self):
        stats = StatsAccumulator("pay")
        record = XSet.from_tuples(((1000, 'pay'),))
        stats.record(record)
        assert stats._count == 1
        assert stats._sum == 1000

    def test_stats_given_record_without_field(self):
        stats = StatsAccumulator("pay")
        record = XSet.from_tuples(((1000, 'pork'),))
        stats.record(record)
        assert stats._count == 0
        assert stats._sum == 0

