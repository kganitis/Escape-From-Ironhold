from abc import ABC, abstractmethod
from outcomes import *
from game_object import GameObject


class Usable(GameObject, ABC):
    @abstractmethod
    def use(self, secondary_object=None):
        pass


class Obtainable(GameObject, ABC):
    def take(self, owner):
        if owner and self not in owner.owned:
            return NOT_OWNED_BY_OBJECT
        self.move_to(self.player)
        return TAKE_FROM_OWNER_SUCCESS if owner else TAKE_SUCCESS

    def drop(self):
        self.move_to(self.player.parent)
        return DROP_SUCCESS


class Accessible(GameObject, ABC):
    def go(self):
        self.player.move_to(self)
        self.current_room = self
        self.message(self.description)
        return NO_MESSAGE


class Container(GameObject, ABC):
    def contents(self):
        return self.children

    def insert(self, item):
        self.add_child(item)


class Lockable(GameObject, ABC):
    __locked: bool = True
    __key: GameObject = None
    __can_be_picked: bool = True

    @property
    def locked(self):
        return self.__locked

    @locked.setter
    def locked(self, value):
        self.__locked = value

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, value):
        self.__key = value
        if self.__key.fits_into != self:
            self.__key.fits_into = self

    @property
    def can_be_picked(self):
        return self.__can_be_picked

    @can_be_picked.setter
    def can_be_picked(self, value):
        self.__can_be_picked = value

    def lock(self, locking_tool):
        self.locked = True
        return LOCK_SUCCESS

    def unlock(self, unlocking_tool):
        self.locked = False
        return UNLOCK_SUCCESS


class Openable(GameObject, ABC):
    __open: bool = False

    @property
    def is_open(self):
        return self.__open

    @is_open.setter
    def is_open(self, value):
        self.__open = value

    def open(self, opening_tool=None):
        self.is_open = True
        return OPEN_SUCCESS

    def close(self):
        self.is_open = False
        return CLOSE_SUCCESS


class Animate(GameObject, ABC):
    attitude: int = 0
    asleep: bool = False

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def wake(self):
        pass

    @abstractmethod
    def ask(self):
        pass

    @abstractmethod
    def tell(self):
        pass

    def throw(self, thrown_object):
        thrown_object.move_to(self.parent)
        return THROW_AT_TARGET_SUCCESS
