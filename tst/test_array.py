from array import array
from copy import deepcopy


class TestArray:
    def test_hookup(self):
        assert 2 == 2

    def test_first_array(self):
        ary = array("B", b'abcd1234')
        assert ary[0] == 97
        print(dir(ary))
        assert True

    def test_swap(self):
        ary = array("B", b'abcd1234')
        xry = deepcopy(ary)
        ery = array("B", b'badc2143')
        for i in range(0, 8, 2):
            xry[i], xry[i+1] = xry[i+1], xry[i]
        assert xry == ery

    def test_slice(self):
        ary = array("B", b'abcd1234')
        xry = array("B", b'1234abcd')
        bry = ary[4:8] + ary[0:4]
        assert bry == xry

    def test_get_string(self):
        ary = array("B", b'abcd1234')
        ss = "".join([chr(b) for b in ary])
        assert ss == 'abcd1234'

    def test_init(self):
        def to_string(bytes):
            return "".join((chr(b) for b in bytes))

        names = b'ron chetmarydaverobbcarl'
        ary = array('B', names)
        name_list = [to_string(ary[i:i+4]) for i in range(0, len(ary), 4)]
        assert 'chet' in name_list
        assert 'mary' in name_list
        assert 'dave' in name_list
        assert 'robb' in name_list
        assert 'carl' in name_list
