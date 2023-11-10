# items. module
from .game_object import *
from .outcomes import *


class Item(GameObject, ABC):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)


class LockingTool(Item, Usable, ABC):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)
        self.can_unlock = True
        self.can_lock = True

    def use(self, target_object=None):
        if not target_object:
            return CANT_USE_OBJECT_ALONE

        if not isinstance(target_object, Lockable):
            return CANT_USE_OBJECT_ON_TARGET

        # Transform the command to lock/unlock target object
        verb = 'unlock' if target_object.locked else 'unlock'
        self.world.parse(f"{verb} {target_object} {self}")
        return COMMAND_TRANSFORMED


class LockPick(LockingTool, Obtainable):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)
        self.can_lock = False


class Key(LockingTool, Obtainable):
    def __init__(self, name, initial, description, parent, lockable_target=None):
        super().__init__(name, initial, description, parent)
        self.lockable_target = lockable_target
        lockable_target.key = self


class Lock(Item, Lockable):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)
        Lockable.__init__(self)


class Stone(Item, Obtainable):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)


class Barel(Item, Openable):

    def open(self, opening_tool=None):
        pass

    def close(self):
        pass
