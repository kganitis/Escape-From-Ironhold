# actions.py module
import game.character
from game.game_elements import *
from game.outcomes import *
from game.attributes import *


class Action:
    def __init__(self, game_instance, command_verb, game_elements):
        self.game = game_instance
        # Dynamically set the action method corresponding to the command verb string
        self.execute = getattr(self, command_verb, None)
        self.game_elements = game_elements

    def is_executable(self):
        return self.execute and callable(self.execute)

    def use(self):
        # Check syntax rules
        invalid_objects = [f"{obj}" for obj in self.game_elements[:2] if not isinstance(obj, (Item, LocationConnection))]
        if invalid_objects:
            return INVALID_OBJECT

        object_to_use = self.game_elements[0]
        if not isinstance(object_to_use, Usable):
            return NOT_USABLE

        target_object = None
        if len(self.game_elements) > 1:
            target_object = self.game_elements[1]

        return object_to_use.use(target_object) or CANT_USE_OBJECT

    def lock(self):
        object_to_lock = self.game_elements[0]

        if not isinstance(object_to_lock, (Item, LocationConnection)):
            return INVALID_OBJECT

        if not isinstance(object_to_lock, Lockable):
            return NOT_LOCKABLE

        # Find the locking tool, if any
        locking_tool = False
        if len(self.game_elements) == 2:
            if isinstance(self.game_elements[1], LockingTool):
                locking_tool = self.game_elements[1]
        else:
            # Look in inventory
            for item in self.game.player.inventory.items:
                if isinstance(item, LockingTool):
                    locking_tool = item
        if not locking_tool:
            return MISSING_LOCKING_TOOL

        return object_to_lock.lock(locking_tool) or CANT_LOCK

    def unlock(self):
        object_to_unlock = self.game_elements[0]

        if not isinstance(object_to_unlock, (Item, LocationConnection)):
            return INVALID_OBJECT

        if not isinstance(object_to_unlock, Lockable):
            return NOT_UNLOCKABLE

        # Find the unlocking tool, if any
        unlocking_tool = False
        if len(self.game_elements) == 2:
            if isinstance(self.game_elements[1], LockingTool):
                unlocking_tool = self.game_elements[1]
        else:
            # Look in inventory
            for item in self.game.player.inventory.items:
                if isinstance(item, LockingTool):
                    unlocking_tool = item
        if not unlocking_tool:
            return MISSING_LOCKING_TOOL

        return object_to_unlock.unlock(unlocking_tool) or CANT_UNLOCK

    def open(self):
        object_to_open = self.game_elements[0]

        if not isinstance(object_to_open, (Item, LocationConnection)):
            return INVALID_OBJECT

        if not isinstance(object_to_open, Openable):
            return NOT_OPENABLE

        opening_tool = None
        if len(self.game_elements) > 1:
            opening_tool = self.game_elements[1]

        return object_to_open.open(opening_tool) or CANT_OPEN_OBJECT

    def close(self):
        object_to_close = self.game_elements[0]

        if not isinstance(object_to_close, (Item, LocationConnection)):
            return INVALID_OBJECT

        if not isinstance(object_to_close, Openable):
            return NOT_CLOSABLE

        return object_to_close.close() or CANT_CLOSE_OBJECT

    def combine(self):
        items_to_combine = self.game_elements[:2]

        invalid_items = [f"{item}" for item in items_to_combine if not isinstance(item, Item)]
        if invalid_items:
            return INVALID_ITEMS

        if len(items_to_combine) == 1:
            return MUST_BE_COMBINED if isinstance(items_to_combine[0], Combinable) else NOT_COMBINABLE

        item1, item2 = items_to_combine
        if not isinstance(item1, Combinable) or not isinstance(item2, Combinable):
            return NOT_COMBINABLE

        return item1.combine(item2) or item2.combine(item1) or CANT_COMBINE

    def go(self):
        location_to_go = self.game_elements[0]
        if not (isinstance(location_to_go, Location) and isinstance(location_to_go, Accessible)):
            return INVALID_LOCATION

        outcome = location_to_go.go()
        return outcome or CANT_GO_TO_LOCATION
