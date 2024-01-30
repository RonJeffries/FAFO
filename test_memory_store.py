import os
from datetime import datetime

from lorem.text import TextLorem

from tag import Tag
from test_pythonista_1 import TagSet
from os.path import expanduser, exists


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
        names = self.make_filenames()
        assert names[0] == "t-20240129083200.000Z_author-ron_student-alice_topic-math.curry"

    def make_filenames(self):
        authors = ["ron", "bill", "geepaw", "chet", "sam", "amy", "janet", "susan", "beyonce", "taylor"]
        topics = ["math", "code", "python", "lisp", "fortran", "ethics", "debugging", "security", "mobbing", "pizza"]
        students = ["alice", "bob", "charlie", "dorothy", "eliza", "fred", "geena", "hector", "ida", "justin"]
        time = 0
        names = []
        for author in authors:
            for topic in topics:
                for student in students:
                    time_stamp = f"20240129083200.{time:03d}Z"
                    ts = TagSet()
                    ts.add_at(time_stamp, "t")
                    ts.add_at(author, "author")
                    ts.add_at(topic, "topic")
                    ts.add_at(student, "student")
                    line = ts.get_file_name()
                    time += 1
                    names.append(line)
        return names

    def test_make_database(self):
        # assert False
        start = datetime.now()
        database = expanduser("~/programming/database")
        if exists(database):
            print("not writing")
        else:
            print("writing")
            names = self.make_filenames()
            os.mkdir(database)
            for name in names:
                lorem = TextLorem(srange=(7,10), prange=(4, 8), trange=(5, 9))
                # srange = number of words in sentence
                # prange = number of sentences in para
                # trangs = number of paras in text
                doc = name + "\n" + lorem.text()
                full_name = f"{database}/{name}"
                with open(full_name, "w") as db_file:
                    db_file.writelines(doc)
        elapsed = datetime.now() - start
        print(elapsed)
        # assert False





