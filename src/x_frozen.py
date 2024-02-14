from src.x_impl import XImplementation


class XFrozen(XImplementation):
    def __init__(self, fs):
        self.data = fs

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        return iter(self.data)

    def __hash__(self):
        return hash(self.data)

    def __repr__(self):
        return repr(self.data)
