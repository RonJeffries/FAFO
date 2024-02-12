import pytest

from src.tag import Tag


class TestTag:
    def test_tag(self):
        assert True

    def test_creation(self):
        tag = Tag("author", "ron")
        assert tag.name == "author"
        assert tag.value == "ron"

    def test_modification(self):
        tag = Tag("author", "ron")
        with pytest.raises(AttributeError):
            tag.value = "not gonna happen"

    def test_does_not_equal_non_tag(self):
        tag = Tag("author", "ron")
        assert tag != ("author", "ron")

