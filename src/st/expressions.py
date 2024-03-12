from expressions import Expression, Parser
from ximpl import XImplementation
from xset import XSet


class XCalculation(XImplementation):
    def __init__(self, base_set, expressions):
        self.base = base_set
        self.expressions = [Expression(None, Parser(expr).rpn()) for expr in expressions]

    def __iter__(self):
        for record, record_scope in self.base:
            calculated_values = self.create_calculated_values(record)
            full_record = record.union(calculated_values)
            yield full_record, record_scope

    def create_calculated_values(self, record):
        calculated = [(calc.result(record), calc.scope()) for calc in self.expressions]
        return XSet.from_tuples(calculated)

    def __hash__(self):
        return hash(self.base)

    def __len__(self):
        return len(self.base)

    def __repr__(self):
        return f'XCalc({[self.expressions]}'
