# items. module
from .attributes import *
from .game_object import *
from .outcomes import *


class Item(GameObject, ABC):
    def __init__(self, name, description, parent):
        super().__init__(name, description, parent)


class LockingTool(Item, Usable, ABC):
    def __init__(self, name, description, parent):
        super().__init__(name, description, parent)
        self.can_unlock = True
        self.can_lock = True

    def use(self, target_object=None):
        if not target_object:
            return CANT_USE_OBJECT_ALONE

        if not isinstance(target_object, Lockable):
            return NOT_LOCKABLE

        return target_object.unlock(self) if target_object.locked else target_object.lock(self)


class LockPick(LockingTool, Obtainable):
    def __init__(self, parent):
        name = "lockpick"
        description = "A simple lock pick that could be useful for picking locks."
        super().__init__(name, description, parent)
        self.can_lock = False


class Lock(Item, Lockable):
    def __init__(self, parent):
        name = "lock"
        description = "A simple lock that can be unlocked with a lock pick, if I had one..."
        super().__init__(name, description, parent)
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


class Stone(Item, Obtainable):
    pass


class Barel(Item, Openable):

    def open(self, opening_tool=None):
        pass

    def close(self):
        pass
