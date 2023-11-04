# attributes.py
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
    def take(self):
        self.move_to(self.player)


class Accessible(ABC):
    @abstractmethod
    def go(self):
        pass


class Examinable(ABC):
    @abstractmethod
    def examine(self):
        pass


class Lockable(ABC):
    def __init__(self, locked=True):
        self._locked = locked

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = value

    @abstractmethod
    def lock(self, locking_tool):
        pass

    @abstractmethod
    def unlock(self, unlocking_tool):
        pass


class Openable(ABC):
    def __init__(self, _open=False):
        self._open = _open

    @property
    def is_open(self):
        return self._open

    @is_open.setter
    def is_open(self, value):
        self._open = value

    @abstractmethod
    def open(self, opening_tool=None):
        pass

    @abstractmethod
    def close(self):
        pass
