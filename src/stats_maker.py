

class StatsAccumulator:
    def __init__(self, name):
        self._name = name
        self._count = 0
        self._sum = 0

    def record(self, xset):
        value = xset[self._name]
        if value:
            self.value(value)

    def statistics(self):
        from xset import XSet
        return XSet.from_tuples(self.tuples())

    def tuples(self):
        tups = []
        tups.append((self._count, self._name+'_count'))
        tups.append((self._sum, self._name+'_sum'))
        tups.append((self.mean(), self._name+'_mean'))
        return tups

    def value(self, number):
        self._count += 1
        self._sum += number

    def mean(self):
        return self._sum / self._count


class StatisticsMaker:
    def __init__(self, fields):
        self._accumulators = [StatsAccumulator(field) for field in fields]
        self._scopes = self.make_scopes(fields)
        self._key = None

    def make_scopes(self, scopes):
        from xset import XSet
        tuples = [(scope, scope) for scope in scopes]
        return XSet.from_tuples(tuples)

    def record(self, xSet):
        if not self._key:
            all_scopes = xSet.scope_set()
            desired_scopes = all_scopes - self._scopes
            self._key = xSet.re_scope(desired_scopes)
        for accumulator in self._accumulators:
            accumulator.record(xSet)

    def statistics(self):
        result = self._key
        for accumulator in self._accumulators:
            result = result | accumulator.statistics()
        return result

