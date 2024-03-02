from set_builder import SetBuilder


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

    def test_streamlined(self):
        xset = SetBuilder()\
            .put('a', 'A')\
            .put('b','B')\
            .set()
        assert xset['A'] == 'a'
        assert xset['B'] == 'b'

    def test_set_of_records(self):
        rb = SetBuilder()
        r1 = SetBuilder()\
            .put('a', 'A')\
            .put('b', 'B')\
            .set()
        rb.put(r1, 1)
        r2 = SetBuilder()\
            .put('aa', 'A')\
            .put('bb', 'B')\
            .set()
        rb.put(r2, 2)
        records = rb.set()
        assert records[2]['B'] == 'bb'

