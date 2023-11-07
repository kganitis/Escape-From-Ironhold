from abc import ABC, abstractmethod
from .outcomes import *


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
        return TAKE_SUCCESS

    def drop(self):
        self.move_to(self.player.parent)
        return DROP_SUCCESS


class Accessible(ABC):
    def go(self):
        self.player.move_to(self)
        self.current_location = self
        return ACCESSED_LOCATION_SUCCESS


class Examinable(ABC):
    @abstractmethod
    def examine(self):
        pass


class Lockable(ABC):
    def __init__(self, locked=True, key=None, can_be_picked=True):
        self._locked = locked
        self.key = key
        if key:
            key.lockable_target = self
        self.can_be_picked = can_be_picked

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

    def close(self):
        self.is_open = False
        return CLOSE_SUCCESS
