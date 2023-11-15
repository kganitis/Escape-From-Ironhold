# items. module
from .game_object import *
from .outcomes import *


class LockingTool(GameObject, Usable, ABC):
    can_unlock = True
    can_lock = True

    def use(self, target_object=None):
        if not target_object:
            return CANT_USE_OBJECT_ALONE

        if not isinstance(target_object, Lockable):
            return CANT_USE_OBJECT_ON_TARGET

        # Transform the command to lock/unlock target object
        verb = 'unlock' if target_object.locked else 'lock'
        self.world.parse(f"{verb} {target_object} {self}")
        return COMMAND_TRANSFORMED


class LockPick(LockingTool, Obtainable):
    can_lock = False


class Key(LockingTool, Obtainable):
    _fits_into: Lockable

    @property
    def fits_into(self):
        return self._fits_into

    @fits_into.setter
    def fits_into(self, target):
        self._fits_into = target
        if target.key != self:
            target.key = self


class Mattress(GameObject):
    def examine(self):
        super().examine()
        lockpick = self.world.get('lockpick')
        lockpick.concealed = False
        lockpick.discover()
        return EXAMINE_SUCCESS


class Lock(GameObject, Lockable): pass
class Stone(GameObject, Obtainable): pass
class DogTag(GameObject, Obtainable): pass
class Wall(GameObject, Container): pass
class Barrel(GameObject, Openable): pass
