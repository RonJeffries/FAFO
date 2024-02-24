from ximpl import XImplementation


class XTuple(XImplementation):
    def __init__(self, data):
        self.data = data

    def __contains__(self, t):
        if not isinstance(t, tuple):
            return False  # should raise?
        e, s = t
        return isinstance(s, int) and 0 < s <= len(self.data) and self.data[s-1] == e

    def __iter__(self):
        scope = 1
        for e in self.data:
            yield e, scope
            scope += 1

    def __hash__(self):
        return hash(self.data)

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return 'XTuple(' + repr(self.data) + ')'
