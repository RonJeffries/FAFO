class Expression:
    def __init__(self, scope, operations):
        self._scope = scope
        self._operations = operations[::-1]

    def result(self, record):
        def to_number(string):
            return int(string)

        stack = []
        while self._operations:
            self._operations.pop()(self, stack, record)
        return stack.pop()

    def scope(self):
        return self._scope

    def to_number(self, string):
        try:
            return int(string)
        except ValueError:
            return float(string)
