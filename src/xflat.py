from os.path import expanduser
from os import stat

from ximpl import XImplementation
from xset import XSet


class XFlat(XImplementation):
    def __init__(self, fields, record):
        self.fields = fields
        self.record = record

    def __iter__(self):
        for symbol, start, end in self.fields:
            yield self.record[start:end].strip(), symbol

    def __hash__(self):
        return -1

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        return f"XFlat('{self.record}')"

    @classmethod
    def fields(cls, names_and_lengths):
        it = iter(names_and_lengths)
        by_two = zip(it, it)
        start = 0
        field_definitions = [(symbol, start, start := start + length) for symbol, length in by_two]
        return field_definitions


class XFlatFile(XImplementation):
    def __init__(self, file_path, fields, scope_set=None, buffer=None):
        self.file_path = file_path
        self.full_file_path = expanduser(file_path)
        self.fields = fields
        field_def = self.fields[-1]
        self.record_length = field_def[-1]
        self.scope_set = scope_set
        if buffer is None:
            with open(self.full_file_path, "r") as f:
                self.buffer = f.read()
        else:
            self.buffer = buffer

    def __contains__(self, item):
        if self.scope_set is not None:
            return any(es == item for es in self)
        de, ds = item
        return de == self.element_at(ds)

    def __iter__(self):
        def lots():
            n = 1
            while True:
                yield n, n
                n += 1

        it = iter(self.scope_set) if self.scope_set else lots()
        for old_scope, new_scope in it:
            rec = self.element_at(old_scope)
            if rec is None:
                return
            yield rec, new_scope

    def __hash__(self):
        return hash((self.full_file_path, self.fields))

    def __len__(self):
        if self.scope_set is not None:
            return len(self.scope_set)
        return self.file_length_in_records()

    def file_length_in_records(self):
        return int(len(self.buffer) / self.record_length)

    def __repr__(self):
        return f'XFlatFile({self.file_path})'

    def get_record(self, index):
        seek_address = index*self.record_length
        if seek_address > len(self.buffer):
            return ''
        else:
            return self.buffer[seek_address:seek_address + self.record_length]

    def element_at(self, scope):
        if not isinstance(scope, int) or scope < 1:
            return None
        rec = self.get_record(scope - 1)
        if rec == '':
            return None
        return XSet(XFlat(self.fields, rec))

    def rename_contents(self, re_scoping_set):
        new_names = []
        for name, start, len in self.fields:
            changed_name = name
            for old, new in re_scoping_set:
                if name == old:
                    changed_name = new
            new_names.append((changed_name, start, len))
        return self.__class__(self.full_file_path, new_names, self.scope_set)

    def re_scope(self, re_scoping_set):
        if self.scope_set is not None:
            re_scoping_set = self.scope_set.re_scope(re_scoping_set)
        re_scoping_set = self.validate_scope_set(re_scoping_set)
        if len(re_scoping_set) == 0:
            return None
        new_impl = self.__class__(self.full_file_path, self.fields, re_scoping_set, self.buffer)
        return XSet(new_impl)

    def validate_scope_set(self, re_scoping_set):
        maximum = self.file_length_in_records()
        return re_scoping_set.select(lambda e, s: type(e) is int and 0 < e <= maximum)

