class MemoryStore:
    pass


class TestMemoryStore():
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_store_exists(self):
        store = MemoryStore()
