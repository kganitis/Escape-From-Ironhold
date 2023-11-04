# actions.py module
from game.game_object import *
from .character import *
from .location_connections import *
from .locations import *
from .items import *
from .attributes import *
from .result import *


class Action:
    def __init__(self, world, command, game_objects):
        self.world = world
        self.command = command
        self.game_objects = game_objects

        # Dynamically get the action execution function matching the command verb
        self.execution_function = getattr(self, command.verb, None)

        # Initialize a list to keep all the results of the execution
        self.results = []

    @property
    def scope(self):
        return self.world.player.scope

    @property
    def player(self):
        return self.world.player

    def execute(self):
        if self.execution_function and callable(self.execution_function):
            self.execution_function()
            return self.results
        else:
            raise ValueError(f"Action not found for verb: {self.command.verb}")

    def produce_result(self, outcome_const, *args):
        result = Result(self.command, *create_outcome(outcome_const, *args))
        self.results.append(result)

    def take(self):
        invalid_objects, out_of_scope, not_obtainable, already_obtained, objects_to_take = [], [], [], [], []
        for obj in self.game_objects:
            if not isinstance(obj, GameObject):
                invalid_objects.append(str(obj))
            elif obj not in self.scope:
                out_of_scope.append(obj)
            elif not isinstance(obj, Obtainable):
                not_obtainable.append(obj)
            elif obj in self.player.inventory:
                already_obtained.append(obj)
            else:
                objects_to_take.append(obj)

        if invalid_objects:
            self.produce_result(INVALID_OBJECTS, invalid_objects)
        if out_of_scope:
            self.produce_result(OUT_OF_SCOPE, out_of_scope)
        if not_obtainable:
            self.produce_result(NOT_OBTAINABLE, not_obtainable)
        if already_obtained:
            self.produce_result(ALREADY_OBTAINED, already_obtained)
        if objects_to_take:
            for obj in objects_to_take:
                obj.take()
            self.produce_result(TAKE_SUCCESS, objects_to_take)

    def use(self):
        # Check syntax rules
        invalid_objects = [f"{obj}" for obj in self.game_objects[:2] if not isinstance(obj, (Item, LocationConnection))]
        if invalid_objects:
            return self.produce_result(INVALID_OBJECTS, invalid_objects)

        object_to_use = self.game_objects[0]
        if not isinstance(object_to_use, Usable):
            return self.produce_result(NOT_USABLE, object_to_use)

        target_object = self.game_objects[1] if len(self.game_objects) > 1 else None
        outcome = object_to_use.use(target_object) or CANT_USE_OBJECT
        self.produce_result(outcome, object_to_use, target_object)

    def lock(self):
        object_to_lock = self.game_objects[0]

        if not isinstance(object_to_lock, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECTS, object_to_lock)

        if not isinstance(object_to_lock, Lockable):
            return self.produce_result(NOT_LOCKABLE, object_to_lock)

        # Find the locking tool, if any
        locking_tool = False
        if len(self.game_objects) == 2:
            if isinstance(self.game_objects[1], LockingTool):
                locking_tool = self.game_objects[1]
        else:
            # Look in inventory
            for item in self.player.inventory:
                if isinstance(item, LockingTool):
                    locking_tool = item
        if not locking_tool:
            return self.produce_result(MISSING_LOCKING_TOOL)

        outcome = object_to_lock.lock(locking_tool) or CANT_LOCK
        self.produce_result(outcome, object_to_lock, locking_tool)

    def unlock(self):
        object_to_unlock = self.game_objects[0]

        if not isinstance(object_to_unlock, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECTS, object_to_unlock)

        if not isinstance(object_to_unlock, Lockable):
            return self.produce_result(NOT_UNLOCKABLE, object_to_unlock)

        # Find the unlocking tool, if any
        unlocking_tool = False
        if len(self.game_objects) == 2:
            if isinstance(self.game_objects[1], LockingTool):
                unlocking_tool = self.game_objects[1]
        else:
            # Look in inventory
            for item in self.player.inventory:
                if isinstance(item, LockingTool):
                    unlocking_tool = item
        if not unlocking_tool:
            return self.produce_result(MISSING_LOCKING_TOOL)

        outcome = object_to_unlock.unlock(unlocking_tool) or CANT_UNLOCK
        self.produce_result(outcome, object_to_unlock, unlocking_tool)

    def open(self):
        object_to_open = self.game_objects[0]

        if not isinstance(object_to_open, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECTS, object_to_open)

        if not isinstance(object_to_open, Openable):
            return self.produce_result(NOT_OPENABLE, object_to_open)

        opening_tool = None
        if len(self.game_objects) > 1:
            opening_tool = self.game_objects[1]

        outcome = object_to_open.open(opening_tool) or CANT_OPEN_OBJECT
        self.produce_result(outcome, object_to_open, opening_tool)

    def close(self):
        object_to_close = self.game_objects[0]

        if not isinstance(object_to_close, (Item, LocationConnection)):
            return self.produce_result(INVALID_OBJECTS, object_to_close)

        if not isinstance(object_to_close, Openable):
            return self.produce_result(NOT_CLOSABLE, object_to_close)

        outcome = object_to_close.close() or CANT_CLOSE_OBJECT
        self.produce_result(outcome, object_to_close)

    def go(self):
        location_to_go = self.game_objects[0]
        if not (isinstance(location_to_go, Location) and isinstance(location_to_go, Accessible)):
            return self.produce_result(INVALID_LOCATION, location_to_go)

        outcome = location_to_go.go() or CANT_GO_TO_LOCATION
        self.produce_result(outcome, location_to_go)
