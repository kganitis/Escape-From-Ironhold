from abc import ABC, abstractmethod

from .outcomes import *


class Usable(ABC):
    @abstractmethod
    def use(self, secondary_object=None):
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
        self.current_room = self
        self.print_message(self.description)
        return ACCESS_ROOM_SUCCESS


class Container(ABC):
    def contents(self):
        return self.children

    def insert(self, item):
        self.add_child(item)


class Lockable(ABC):
    _locked = True
    _key = None
    can_be_picked = True

    def __init__(self, locked=True, key=None, can_be_picked=True):
        self.locked = locked
        self.key = key
        self.can_be_picked = can_be_picked

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        self._locked = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        if self.key.fits_into != self:
            self._key.fits_into = self

    def lock(self, locking_tool):
        self.locked = True
        return LOCK_SUCCESS

    def unlock(self, unlocking_tool):
        self.locked = False
        return UNLOCK_SUCCESS


class Openable(ABC):
    _open = False

    def __init__(self, open):
        self._open = open

    @property
    def is_open(self):
        return self._open

    @is_open.setter
    def is_open(self, value):
        self._open = value

    def open(self, opening_tool=None):
        self.is_open = True
        return OPEN_SUCCESS

    def close(self):
        self.is_open = False
        return CLOSE_SUCCESS
