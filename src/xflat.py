from os.path import expanduser

from ximpl import XImplementation
from xset import XSet


class XFlat(XImplementation):
    def __init__(self, fields, record):
        self.fields = fields
        self.record = record

    def __contains__(self, item):
        element, scope = item
        for symbol, start, end in self.fields:
            if symbol == scope:
                field = self.record[start:end].strip()
                if field == element:
                    return True
        return False

    def __iter__(self):
        for symbol, start, end in self.fields:
            yield self.record[start:end].strip(), symbol

    def __hash__(self):
        return -1

    def __repr__(self):
        return f"XFlat('{self.record}')"

    @classmethod
    def fields(cls, names_and_lengths):
        it = iter(names_and_lengths)
        by_two = zip(it, it)
        start = 0
        field_definitions = [(symbol, start, start := start + length) for symbol, length in by_two]
        return field_definitions


class XFlatFileIterator:
    def __init__(self, flat_file, generator):
        self.file = flat_file
        self.scope_gen = generator

    def __iter__(self):
        return self

    def __next__(self):
        _element, scope = next(self.scope_gen)
        element_tuple = (rec := self.file.element_at(scope), scope)
        if rec is None:
            raise StopIteration
        else:
            return element_tuple


class XFlatFile(XImplementation):
    def __init__(self, file_path, fields, scope_set=None):
        self.file_path = file_path
        self.fields = fields
        field_def = self.fields[-1]
        self.record_length = field_def[-1]
        self.scope_set = scope_set

    def __contains__(self, item):
        de, ds = item
        return de == self.element_at(ds)

    def __iter__(self):
        def lots():
            n = 1
            while True:
                yield n, n
                n += 1

        it = iter(self.scope_set) if self.scope_set else lots()
        for _e, scope in it:
            rec = self.element_at(scope)
            if rec is None:
                return
            yield rec, scope

    def __hash__(self):
        return hash((self.file_path, self.fields))

    def __repr__(self):
        return f'XFlatFile({self.file_path})'

    def get_record(self, index):
        seek_address = index*self.record_length
        with open(expanduser(self.file_path), "r") as f:
            f.seek(seek_address)
            rec = f.read(self.record_length)
        return rec

    def element_at(self, scope):
        if not isinstance(scope, int) or scope < 1:
            return None
        rec = self.get_record(scope - 1)
        if rec == '':
            return None
        return XSet(XFlat(self.fields, rec))
