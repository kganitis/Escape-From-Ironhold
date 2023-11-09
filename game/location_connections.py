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

    @property
    def is_blocked(self):
        return BLOCKED_CONNECTION

    def connect_locations(self, *locations):
        self.connected_locations.extend(locations)
        for loc in locations:
            loc.add_connection(self)

    def get_connected_location_from(self, coming_location):
        return next((loc for loc in self.connected_locations if loc != coming_location), None)


class Door(LocationConnection, Openable, Lockable):
    def __init__(self, name, description, parent, lock):
        super().__init__(name, description, parent)
        Openable.__init__(self)
        Lockable.__init__(self)
        self.lock_ = lock
        self.attach(self.lock_)
        self.key = lock.key
        self.can_be_picked = lock.can_be_picked

    @property
    def locked(self):
        return self.lock_.locked

    @property
    def is_blocked(self):
        if self.locked:
            return BLOCKED_OBJECT_LOCKED
        if not self.is_open:
            return BLOCKED_OBJECT_CLOSED
        return False

    def open(self, opening_tool=None):
        open_with_tool = False
        if self.locked:
            if opening_tool:
                # Generate a command to unlock the door first, before attempting to open
                result = self.world.parse(f"unlock {self} {opening_tool}")
                open_with_tool = result.outcome.outcome == UNLOCK_SUCCESS
            else:
                return BLOCKED_OBJECT_LOCKED

        self.is_open = True
        return OPEN_WITH_TOOL_SUCCESS if open_with_tool else OPEN_SUCCESS

    def lock(self, locking_tool):
        if self.is_open:
            return MUST_CLOSE_OBJECT
        return self.lock_.lock(locking_tool)

    def unlock(self, unlocking_tool):
        return self.lock_.unlock(unlocking_tool)
