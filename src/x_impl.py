from abc import ABC, abstractmethod


class XImplementation(ABC):
    @abstractmethod
    def __contains__(self, item):
        return False

    @abstractmethod
    def __iter__(self):
        raise NotImplemented

    @abstractmethod
    def __hash__(self):
        raise NotImplemented

    @abstractmethod
    def __repr__(self):
        raise NotImplemented
