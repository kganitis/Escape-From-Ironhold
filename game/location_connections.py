from game.game_elements import *
from game.items import Lock
from game.outcomes import *
from game.properties import *


class Door(LocationConnection, Openable, Lockable):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)
        self._lock = Lock(game)
        self.items.append(self._lock)

    def is_blocked(self):
        outcome = False
        if self._lock.locked:
            outcome = DOOR_LOCKED_FAIL
        elif not self.opened:
            outcome = DOOR_CLOSED_FAIL
        return outcome

    def open(self):
        if self._lock.locked:
            return DOOR_LOCKED_FAIL

        if self.opened:
            return ALREADY_OPEN

        self.opened = True
        return DOOR_OPENED_SUCCESS

    def close(self):
        if not self.opened:
            return ALREADY_CLOSED
        self.opened = False
        return DOOR_CLOSED_SUCCESS

    def toggle_locked(self, locked, locking_tool):
        if not isinstance(locking_tool, LockingTool):
            return MISSING_LOCKING_TOOL
        outcome = self._lock.lock(locking_tool) if locked else self._lock.unlock(locking_tool)
        self.locked = self._lock.locked
        return outcome

    def lock(self, locking_tool):
        if self.opened:
            return DOOR_OPEN_FAIL
        return self.toggle_locked(True, locking_tool)

    def unlock(self, locking_tool):
        return self.toggle_locked(False, locking_tool)
