

class Tag:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.name == other.name and self.value == other.value
        else:
            return NotImplemented

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value
