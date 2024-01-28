from tag import Tag


class MemoryStore:
    def __init__(self):
        self._store = []

    def add_document(self, tags, document):
        self._store.append((tags, document))


class TestMemoryStore():
    def test_hookup(self):
        assert 2 + 2 == 4

    def test_store_exists(self):
        store = MemoryStore()

    def test_can_store(self):
        store = MemoryStore()
        tags = [Tag("author", "ron"), Tag("title", "nature")]
        document = "these are the facts"
        store.add_document(tags, document)
