class StatsMaker:
    def __init__(self, name):
        self._name = name
        self._count = 0
        self._sum = 0

    def value(self, number):
        self._count += 1


class TestStatsObject:
    def test_stats(self):
        stats = StatsMaker("pay")
        stats.value(1000)
        stats.value(2000)
        stats.value(3000)
        stats.value(4000)
        assert stats._count == 4
