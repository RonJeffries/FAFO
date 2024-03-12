from ximpl import XImplementation


class XSelect(XImplementation):
    def __init__(self, base, cond):
        self._base = base
        self._cond = cond

    def __iter__(self):
        for e, s in self._base:
            if self._cond(e, s):
                yield e, s

    def __hash__(self):
        return hash(self._base)

    def __len__(self):
        len = 0
        for _t in self:
            len += 1
        return len

    def __repr__(self):
        return f'XSelect({self._base})'
