from game.game_objects import *
from game.items import Lock
from game.outcomes import *
from game.attributes import *


class Door(LocationConnection, Openable, Lockable):
    def __init__(self, game, name, description, parent):
        super().__init__(game, name, description, parent)
        Openable.__init__(self)
        Lockable.__init__(self)
        self.__lock = Lock(game, parent=self)
        self.attach(self.__lock)

    def locked(self):
        return self.__lock.locked

    def is_blocked(self):
        if self.__lock.locked:
            return DOOR_LOCKED_FAIL
        if not self._open:
            return DOOR_CLOSED_FAIL
        return False

    def open(self, opening_tool=None):
        if self.__lock.locked:
            if opening_tool and isinstance(opening_tool, LockingTool):
                self.game.parse(f"unlock {self} {opening_tool}")
            else:
                return DOOR_LOCKED_FAIL

        if self._open:
            return ALREADY_OPEN

        self._open = True
        return DOOR_OPENED_SUCCESS

    def close(self):
        if not self._open:
            return ALREADY_CLOSED
        self._open = False
        return DOOR_CLOSED_SUCCESS

    def lock(self, locking_tool):
        if self._open:
            return DOOR_OPEN_FAIL
        return self.__lock.lock(locking_tool)

    def unlock(self, unlocking_tool):
        return self.__lock.unlock(unlocking_tool)
