import lorem
from lorem.text import TextLorem


def test_lorem():
    thing = TextLorem(srange=(3,3), prange=(2,2), trange=(4,4))
    # srange = number of words in sentence
    # prange = number of sentences in para
    # trangs = number of paras in text
    text = thing.text()
    print(text)
    assert True

