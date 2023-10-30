# actions.py module
from game.game_elements import *
from game.attributes import *
from game.result import Result


class Action:
    def __init__(self, game_instance, command, game_elements):
        self.game = game_instance
        self.command = command
        self.game_elements = game_elements
        # Dynamically set the action method corresponding to the command verb string
        self.execute = getattr(self, command.verb, None)
        # Initialize a list to keep all the results of the execution
        self.results = []

    def is_executable(self):
        return self.execute and callable(self.execute)

    def produce_result(self, outcome_const, *args):
        result = Result(self.command, *create_outcome(outcome_const, *args))
        self.results.append(result)

    def take(self):
        invalid_items, not_obtainable, already_obtained, items_to_take = [], [], [], []
        for item in self.game_elements:
            if not isinstance(item, Item):
                invalid_items.append(f"{item}")
            elif not isinstance(item, Obtainable):
                not_obtainable.append(item)
            elif item in self.game.player.inventory.items:
                already_obtained.append(item)
            else:
                items_to_take.append(item)

        if invalid_items:
            self.produce_result(INVALID_ITEMS, invalid_items)
        if not_obtainable:
            self.produce_result(NOT_OBTAINABLE, not_obtainable)
        if already_obtained:
            self.produce_result(ALREADY_OBTAINED, already_obtained)

        # Take the rest of the items
        if items_to_take:
            for item in items_to_take:
                item.take(self.game.player.inventory.items)
            self.produce_result(TAKE_SUCCESS, items_to_take)

    def use(self):
        # Check syntax rules
        invalid_objects = [f"{obj}" for obj in self.game_elements[:2] if not isinstance(obj, (Item, LocationConnection))]
        if invalid_objects:
            return self.produce_result(INVALID_OBJECT, invalid_objects)

        object_to_use = self.game_elements[0]
        if not isinstance(object_to_use, Usable):
            return self.produce_result(NOT_USABLE, object_to_use)

        target_object = self.game_elements[1] if len(self.game_elements) > 1 else None
        outcome = object_to_use.use(target_object) or CANT_USE_OBJECT
        self.produce_result(outcome, object_to_use, target_object)

    def lock(self):
        object_to_lock = self.game_elements[0]

        if not isinstance(object_to_lock, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECT, object_to_lock)

        if not isinstance(object_to_lock, Lockable):
            return self.produce_result(NOT_LOCKABLE, object_to_lock)

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
            return self.produce_result(MISSING_LOCKING_TOOL)

        outcome = object_to_lock.lock(locking_tool) or CANT_LOCK
        self.produce_result(outcome, object_to_lock, locking_tool)

    def unlock(self):
        object_to_unlock = self.game_elements[0]

        if not isinstance(object_to_unlock, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECT, object_to_unlock)

        if not isinstance(object_to_unlock, Lockable):
            return self.produce_result(NOT_UNLOCKABLE, object_to_unlock)

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
            return self.produce_result(MISSING_LOCKING_TOOL)

        outcome = object_to_unlock.unlock(unlocking_tool) or CANT_UNLOCK
        self.produce_result(outcome, object_to_unlock, unlocking_tool)

    def open(self):
        object_to_open = self.game_elements[0]

        if not isinstance(object_to_open, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECT, object_to_open)

        if not isinstance(object_to_open, Openable):
            return self.produce_result(NOT_OPENABLE, object_to_open)

        opening_tool = None
        if len(self.game_elements) > 1:
            opening_tool = self.game_elements[1]

        outcome = object_to_open.open(opening_tool) or CANT_OPEN_OBJECT
        self.produce_result(outcome, object_to_open, opening_tool)

    def close(self):
        object_to_close = self.game_elements[0]

        if not isinstance(object_to_close, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECT, object_to_close)

        if not isinstance(object_to_close, Openable):
            return self.produce_result(NOT_CLOSABLE, object_to_close)

        outcome = object_to_close.close() or CANT_CLOSE_OBJECT
        self.produce_result(outcome, object_to_close)

    def go(self):
        location_to_go = self.game_elements[0]
        if not (isinstance(location_to_go, Location) and isinstance(location_to_go, Accessible)):
            return self.produce_result(INVALID_LOCATION, location_to_go)

        outcome = location_to_go.go() or CANT_GO_TO_LOCATION
        self.produce_result(outcome, location_to_go)
