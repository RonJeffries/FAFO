class StatsMaker:
    def __init__(self, name):
        self._name = name
        self._count = 0
        self._sum = 0


class TestStatsObject:
    def test_stats(self):
        stats = StatsMaker("pay")