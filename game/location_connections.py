from .game_object import *
from .outcomes import *


class LocationConnection(GameObject, ABC):
    def __init__(self, name, description, parent):
        super().__init__(name, description, parent)
        self.connected_locations = []

    @property
    # Items found in this location connection
    def items(self):
        return self.children

    @property
    def scope(self, modifier=None):
        scope = super().scope
        scope.update(self.connected_locations)
        return scope

    def add_connected_locations(self, *locations):
        self.connected_locations.extend(locations)
        for loc in locations:
            loc.add_connection(self)

    @property
    def is_blocked(self):
        return BLOCKED_CONNECTION


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
            return BLOCKED_OBJECT_LOCKED_FAIL
        if not self.is_open:
            return BLOCKED_OBJECT_CLOSED_FAIL
        return False

    def open(self, opening_tool=None):
        open_with_tool = False
        if self.locked:
            if opening_tool:
                # Generate a command to unlock the door first, before attempting to open
                result = self.world.parse(f"unlock {self} {opening_tool}")
                open_with_tool = result[0].outcome == UNLOCK_SUCCESS[0]
            else:
                return BLOCKED_OBJECT_LOCKED_FAIL

        self.is_open = True
        return OPEN_WITH_TOOL_SUCCESS if open_with_tool else OPEN_SUCCESS

    def lock(self, locking_tool):
        if self.is_open:
            return OBJECT_OPEN_FAIL
        return self.__lock.lock(locking_tool)

    def unlock(self, unlocking_tool):
        return self.__lock.unlock(unlocking_tool)
