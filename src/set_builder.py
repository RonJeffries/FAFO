


class SetBuilder:
    def __init__(self):
        self.contents = []

    def put(self, element, scope):
        self.contents.append((element, scope))
        return self

    def set(self):
        from xset import XSet
        return XSet.from_tuples(self.contents)
