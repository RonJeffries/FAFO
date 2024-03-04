class Expression:
    def __init__(self, scope, operations):
        self._scope = scope
        self._operations = operations


class TestExpressions:
    def test_create_Expression(self):
        expr = Expression('gross_pay', [])