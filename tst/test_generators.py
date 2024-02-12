import pytest


def doubler(seq):
    for v in seq:
        yield 2 * v


def twice(seq):
    for v in seq:
        yield v
        yield v


class TestGenerators:
    def test_doubler(self):
        result = []
        for d in doubler([1,2,3]):
            result.append(d)
        assert result == [2,4,6]

    def test_twice(self):
        result = []
        for d in twice((1,3,5)):
            result.append(d)
        assert result == [1, 1, 3, 3, 5, 5]

    def test_nested(self):
        result = []
        for d in twice(doubler((1, 2, 3))):
            result.append(d)
        assert result == [2, 2, 4, 4, 6, 6]

    def test_nested_comprehension(self):
        result = [d for d in twice(doubler((1, 2, 3)))]
        assert result == [2, 2, 4, 4, 6, 6]

    def test_what_is_generator(self):
        gen = twice((3, 2, 1))
        assert gen.__class__.__name__ == "generator"

    def test_use_saved_generator(self):
        gen = doubler((3, 2, 1))
        assert next(gen) == 6
        assert next(gen) == 4
        assert next(gen) == 2
        with pytest.raises(StopIteration):
            next(gen)

    def test_greater_than(self):
        def gt(seq, value):
            for v in seq:
                if v > value:
                    yield v
        big_ones = [big for big in gt((8, 9, 10, 11, 12), 9)]
        assert big_ones == [10, 11, 12]

    def test_nested_saved(self):
        doubles = doubler((10, 20, 30))
        dups = twice(doubles)
        dup_doubles = [d for d in dups]
        assert dup_doubles == [20, 20, 40, 40, 60, 60]


