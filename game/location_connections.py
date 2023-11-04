from .game_object import *
from .items import LockingTool
from .outcomes import *
from .attributes import *


class LocationConnection(GameObject, ABC):
    def __init__(self, name, description, parent):
        super().__init__(name, description, parent)
        self.connected_locations = []

    @property
    # Items found in this location connection
    def items(self):
        return self.children

    def add_connected_locations(self, *locations):
        self.connected_locations.extend(locations)
        for loc in locations:
            loc.add_connection(self)

    def is_blocked(self):
        return BLOCKED_LOCATION


class Door(LocationConnection, Openable, Lockable):
    def __init__(self, name, description, lock, parent):
        super().__init__(name, description, parent)
        Openable.__init__(self)
        Lockable.__init__(self)
        self.__lock = lock
        self.attach(self.__lock)

    @property
    def locked(self):
        return self.__lock.locked

    @property
    def is_blocked(self):
        if self.locked:
            return DOOR_LOCKED_FAIL
        if not self.is_open:
            return DOOR_CLOSED_FAIL
        return False

    def open(self, opening_tool=None):
        if self.locked:
            if opening_tool and isinstance(opening_tool, LockingTool):
                return self.unlock(opening_tool)
            else:
                return DOOR_LOCKED_FAIL

        if self.is_open:
            return ALREADY_OPEN

        self.is_open = True
        return DOOR_OPENED_SUCCESS

    def close(self):
        if not self.is_open:
            return ALREADY_CLOSED
        self.is_open = False
        return DOOR_CLOSED_SUCCESS

    def lock(self, locking_tool):
        if self.is_open:
            return DOOR_OPEN_FAIL
        return self.__lock.lock(locking_tool)

    def unlock(self, unlocking_tool):
        return self.__lock.unlock(unlocking_tool)
