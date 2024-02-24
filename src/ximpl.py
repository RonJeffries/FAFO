from abc import ABC, abstractmethod


class XImplementation(ABC):
    # @abstractmethod can be implemented if desired
    def __contains__(self, item):
        raise NotImplemented

    @abstractmethod
    def __iter__(self):
        raise NotImplemented

    @abstractmethod
    def __hash__(self):
        raise NotImplemented

    @abstractmethod
    def __len__(self):
        raise NotImplemented

    @abstractmethod
    def __repr__(self):
        raise NotImplemented
