# items.py module
from game.game_elements import Item, LockingTool
from game.outcomes import *
from game.properties import *


class LockPick(LockingTool):
    def __init__(self, game):
        name = "lockpick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(game, name, description)
        self.can_lock = True


class Lock(Item, Lockable):
    def __init__(self, game, locked=True):
        name = "lock"
        description = "A simple lock that can could be unlocked with a lock pick, if I had one..."
        super().__init__(game, name, description)
        self.locked = locked

    def lock(self, locking_tool):
        if not isinstance(locking_tool, LockingTool):
            return MISSING_LOCKING_TOOL
        if not self.locked:
            if locking_tool.can_lock:
                self.locked = True
                return LOCK_SUCCESS
            return LOCKING_TOOL_LOCK_FAIL
        return ALREADY_LOCKED

    def unlock(self, locking_tool):
        if not isinstance(locking_tool, LockingTool):
            return MISSING_LOCKING_TOOL
        if self.locked:
            if locking_tool.can_unlock:
                self.locked = False
                return UNLOCK_SUCCESS
            return LOCKING_TOOL_UNLOCK_FAIL
        return ALREADY_UNLOCKED
