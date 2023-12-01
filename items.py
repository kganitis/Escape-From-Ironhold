# items. module
from random import random

from game_object import *
from outcomes import *
from attributes import Usable, Obtainable, Container, Lockable, Enterable


class LockingTool(Usable, ABC):
    can_unlock: bool = True
    can_lock: bool = True

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
    # TODO chance to break
    can_lock: bool = False
    under_mattress: bool = True

    @property
    def initial(self):
        if self.under_mattress:
            return "There is a rusty iron lockpick hidden under the mattress."
        return super().initial

    def take(self, owner):
        self.under_mattress = False
        return super().take(owner)


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


class Keys(Obtainable):
    @property
    def initial(self):
        guard = self.get('guard')
        if self.parent == guard:
            in_reach = ""
            if self.current_room == self.get('cell') and guard.guard_location == guard.NEAR_CELL:
                in_reach = "Maybe they're within your reach."
            return f"A pair of old keys hangs from the guard's belt. {in_reach}"
        return super().initial

    def take(self, owner):
        guard = self.get('guard')
        if guard not in (self.parent, owner):
            return super().take(owner)

        chance_to_steal = 0.1 + 0.8 * guard.asleep
        successful_steal = random() < chance_to_steal

        if successful_steal:
            # Separate the pair into two distinct keys, one for each door
            cell_key = self.get('key')
            cell_key.concealed = False
            cell_key.move_to(self.player)

            dungeon_key = self.get('key2')
            dungeon_key.concealed = False
            dungeon_key.move_to(self.player)

            self.remove()
            return f"You reach and with a quick move you grab the {self} out the guard's belt, without him noticing.\n" \
                   f"Looking at them closely, you can distinguish them clearly:\n" \
                   f"{cell_key.initial[:-1]} and {dungeon_key.initial.lower()} ", SUCCESS

        wakes_up = " wakes up and" if guard.asleep else ""
        guard.asleep = False
        self.player.dead = True
        return f"The {guard}{wakes_up} catches you while reaching your hand to grab the {self}.\n" \
               f"He draws his sword and in a cruel twist, he severs your hand, " \
               f"leaving you to bleed slowly to death.", SUCCESS


class Mattress(GameObject):
    def examine(self):
        super().examine()
        lockpick = self.get('lockpick')
        if lockpick.concealed:
            lockpick.concealed = False
            lockpick.discover()
        return NO_MESSAGE


class Stone(Obtainable):
    @property
    def initial(self):
        if self.parent == self.get('wall'):
            return "One of the small stones is loose. Maybe it can be removed..."
        return super().initial

    @property
    def description(self):
        if self.parent == self.get('wall'):
            return "A loose small stone of the cell's walls. Maybe it can be removed..."
        return "A small stone of the cell's walls. It doesn't seem very useful..."

    def take(self, owner):
        if self.get('wall') in (owner, self.parent):
            super().take(owner)
            return "You manage to remove the stone from the wall but you see nothing of interest.", SUCCESS
        return super().take(owner)


class Lock(Lockable):
    @property
    def description(self):
        if self.locked:
            return f"The {self.long} could be picked with a lockpick, if I had one..."
        return f"The {self.long} has been unlocked."


class CellLock(Lock):
    def unlock(self, unlocking_tool):
        guard = self.get('guard')
        chance_to_get_caught = 0.8 * (not guard.asleep)
        successful_unlock = random() > chance_to_get_caught

        if guard.guard_location != guard.NEAR_CELL or successful_unlock:
            return super().unlock(unlocking_tool)

        wakes_up = " wakes up and" if guard.asleep else ""
        guard.asleep = False
        self.player.dead = True
        return f"The {guard}{wakes_up} catches you while attempting to unlock the door.\n" \
               f"He storms into your cell, swiftly drawing his sword.\n" \
               f"and in a cruel twist, he severs your hand,\n" \
               f"leaving you to bleed slowly to death.", SUCCESS


class DungeonLock(Lock):
    def unlock(self, unlocking_tool):
        guard = self.get('guard')
        chance_to_get_caught = 0.8 * (not guard.asleep)
        successful_unlock = random() > chance_to_get_caught

        if guard.guard_location == guard.NOT_IN_DUNGEON or successful_unlock:
            return super().unlock(unlocking_tool)

        wakes_up = " wakes up and" if guard.asleep else ""
        guard.asleep = False
        self.player.dead = True
        return f"The {guard}{wakes_up} catches you while attempting to unlock the door.\n" \
               f"He rushes to your location, swiftly drawing his sword.\n" \
               f"and in a cruel twist, he severs your hand,\n" \
               f"leaving you to bleed slowly to death.", SUCCESS


class DogTag(Obtainable):
    @property
    def initial(self):
        if self.parent == self.get('cell'):
            return "Some kind of a metallic dog tag lies on the ground."
        return super().initial


class Wall(Container):
    pass


class Barrel(Enterable, Container):
    def examine(self):
        if self.player in self.contents:
            self.message("You can't see a thing in here. Maybe you could wait to hear something...")
            return NO_MESSAGE
        return super().examine()
