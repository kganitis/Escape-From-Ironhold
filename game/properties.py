# properties.py
from abc import ABC, abstractmethod


class Usable(ABC):
    @abstractmethod
    def use(self, indirect_object=None):
        pass


class Combinable(ABC):
    @abstractmethod
    def combine(self, item):
        pass


class Obtainable(ABC):
    @abstractmethod
    def take(self):
        pass


class Accessible(ABC):
    @abstractmethod
    def go(self):
        pass


class Examinable(ABC):
    @abstractmethod
    def examine(self):
        pass


class Lockable(ABC):
    locked = True

    @abstractmethod
    def lock(self, locking_tool):
        pass

    @abstractmethod
    def unlock(self, unlocking_tool):
        pass


class Openable(ABC):
    opened = False

    @abstractmethod
    def open(self):
        pass

    def close(self):
        pass
