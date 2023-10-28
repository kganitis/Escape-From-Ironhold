# items.py module
from game.game_elements import Item, LockingTool
from game.outcomes import *
from game.attributes import *


class LockPick(LockingTool):
    def __init__(self, game, parent):
        name = "lockpick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(game, name, description, parent)
        self.can_lock = False


class Lock(Item, Lockable):
    def __init__(self, game, parent):
        name = "lock"
        description = "A simple lock that can be unlocked with a lock pick, if I had one..."
        super().__init__(game, name, description, parent)
        Lockable.__init__(self)

    def lock(self, locking_tool):
        if self.locked:
            return ALREADY_LOCKED
        if not locking_tool.can_lock:
            return LOCKING_TOOL_LOCK_FAIL
        self.locked = True
        return LOCK_SUCCESS

    def unlock(self, unlocking_tool):
        if not self.locked:
            return ALREADY_UNLOCKED
        if not unlocking_tool.can_unlock:
            return LOCKING_TOOL_UNLOCK_FAIL
        self.locked = False
        return UNLOCK_SUCCESS
