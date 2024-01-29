from tag import Tag


class MemoryStore:
    def __init__(self):
        self._store = []

    def add_document(self, tags, document):
        self._store.append((tags, document))

    def fetch(self, tags):
        result = []
        for item in self._store:
            item_tags, item_document = item
            if all((tag in item_tags for tag in tags)):
                result.append(item)
        return result



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

    def test_can_fetch(self):
        store = MemoryStore()
        tags = [Tag("author", "ron"), Tag("title", "nature")]
        document = "these are the facts"
        store.add_document(tags, document)
        pairs = store.fetch([Tag("author", "ron")])
        assert pairs
        tags, document = pairs[0]
        assert document == "these are the facts"

    def test_make_file_names(self):
        authors = ["ron", "bill", "geepaw", "chet", "sam", "amy", "janet", "susan", "beyonce", "taylor"]
        assert len(authors) == 10
        topics = ["math", "code", "python", "lisp", "fortran", "ethics", "debugging", "security", "mobbing", "pizza"]
        assert len(topics) == 10
        students = ["alice", "bob", "charlie", "dorothy", "eliza", "fred", "geena", "hector", "ida", "justin"]
        assert len(students) == 10
        time = 0
        names = []
        for author in authors:
            for topic in topics:
                for student in students:
                    time_stamp = f"t-20240129083200.{time:03d}Z"
                    line = f"{time_stamp}_author-{author}_topic-{topic}_student-{student}.curry"
                    time += 1
                    names.append(line)
        assert names[0] == "t-20240129083200.000Z_author-ron_topic-math_student-alice.curry"


