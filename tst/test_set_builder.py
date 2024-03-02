from xset import XSet


class SetBuilder:
    def __init__(self):
        self.contents = []

    def put(self, element, scope):
        self.contents.append((element, scope))

    def set(self):
        return XSet.from_tuples(self.contents)


class TestSetBuilder:
    def test_exists(self):
        sb = SetBuilder()

    def test_small_set(self):
        sb = SetBuilder()
        sb.put('a', 'A')
        sb.put('b', 'B')
        xset = sb.set()
        assert xset['A'] == 'a'
        assert xset['B'] == 'b'
