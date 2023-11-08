from .items import *
from .location_connections import *
from .locations import *
from .result import *


class Action:
    def __init__(self, world, command, primary_object=None, secondary_object=None):
        self.world = world
        self.player = world.player
        self.command = command
        self.primary_object = primary_object
        self.secondary_object = secondary_object
        self.objects = [obj for obj in [primary_object, secondary_object] if obj is not None]

        # Dynamically get the action execution function matching the command verb
        self.execution_function = getattr(self, command.verb, None)

    def execute(self):
        # Syntax Analysis
        invalid_objects = [obj for obj in self.objects if not isinstance(obj, GameObject)]
        out_of_scope = [obj for obj in self.objects if obj not in self.player.scope]
        if invalid_objects:
            return self._outcome(INVALID_OBJECTS, *invalid_objects)
        if out_of_scope:
            return self._outcome(OUT_OF_SCOPE, *out_of_scope)

        # Execution
        if self.execution_function and callable(self.execution_function):
            return self.execution_function()
        else:
            raise ValueError(f"Action not found for verb: {self.command.verb}")

    # TODO simplify this shit
    def _outcome(self, outcome, *objects):
        # Make sure objects count is exactly 2 and replace any missing objects with None
        objects = (objects[0] if objects else None, objects[1] if objects and len(objects) > 1 else None)

        # First decide the objects based on the instance fields
        primary = self.primary_object if self.primary_object in objects else None
        secondary = self.secondary_object if self.secondary_object in objects else None

        # If the objects given are not in the instance's primary and secondary fields,
        # get the missing objects from the objects tuple.
        if not (primary and secondary):
            primary, secondary = objects
        elif primary and not secondary:
            secondary = objects[0] if objects[0] != primary else objects[1]
        elif secondary and not primary:
            primary = objects[0] if objects[0] != secondary else objects[1]

        return Outcome(outcome, primary, secondary)

    def take(self):
        object_to_take = self.primary_object

        not_obtainable = not isinstance(object_to_take, Obtainable)
        if not_obtainable:
            return self._outcome(NOT_OBTAINABLE, object_to_take)

        already_obtained = object_to_take in self.player.inventory
        if already_obtained:
            return self._outcome(ALREADY_OBTAINED, object_to_take)

        outcome = object_to_take.take()
        return self._outcome(outcome, object_to_take)

    def drop(self):
        object_to_drop = self.primary_object

        not_in_possession = object_to_drop not in self.player.inventory and object_to_drop not in self.player.held
        if not_in_possession:
            return self._outcome(NOT_IN_POSSESSION, object_to_drop)

        outcome = object_to_drop.drop()
        return self._outcome(outcome, object_to_drop)

    def use(self):
        object_to_use = self.primary_object
        secondary_object = self.secondary_object

        not_usable = not isinstance(object_to_use, Usable)
        if not_usable:
            return self._outcome(NOT_USABLE, object_to_use)

        not_held = object_to_use not in self.player.held
        if not_held:
            return self._outcome(NOT_HELD, object_to_use)

        outcome = object_to_use.use(secondary_object)
        return self._outcome(outcome, object_to_use, secondary_object)

    def __execute_lock_or_unlock(self, operation):
        lockable_object = self.primary_object
        locking_tool = self.secondary_object

        not_lockable = not isinstance(lockable_object, Lockable)
        if not_lockable:
            return self._outcome(NOT_LOCKABLE, lockable_object)

        already_locked_or_unlocked = lockable_object.locked if operation == 'lock' else not lockable_object.locked
        if already_locked_or_unlocked:
            return self._outcome(ALREADY_LOCKED if operation == 'lock' else ALREADY_UNLOCKED, lockable_object)

        not_a_locking_tool = locking_tool is not None and not isinstance(locking_tool, LockingTool)
        if not_a_locking_tool:
            return self._outcome(NOT_A_LOCKING_TOOL if operation == 'lock' else NOT_AN_UNLOCKING_TOOL, locking_tool)

        # If the tool is missing, try to find one in the inventory
        if locking_tool is None:
            for item in self.player.inventory:
                # First, check for a key
                if lockable_object.key is not None and item == lockable_object.key:
                    locking_tool = item
                    break
                # Then, check for a lockpick
                elif lockable_object.can_be_picked and isinstance(item, LockPick):
                    locking_tool = item
                    break
            else:
                return self._outcome(MISSING_LOCKING_TOOL if operation == 'lock' else MISSING_UNLOCKING_TOOL)

        if operation == 'lock' and not locking_tool.can_lock:
            return self._outcome(LOCKING_TOOL_LOCK_FAIL, locking_tool)
        elif operation == 'unlock' and not locking_tool.can_unlock:
            return self._outcome(LOCKING_TOOL_UNLOCK_FAIL, locking_tool)

        outcome = lockable_object.lock(locking_tool) if operation == 'lock' else lockable_object.unlock(locking_tool)
        return self._outcome(outcome, lockable_object, locking_tool)

    def lock(self):
        return self.__execute_lock_or_unlock('lock')

    def unlock(self):
        return self.__execute_lock_or_unlock('unlock')

    def open(self):
        object_to_open = self.primary_object
        opening_tool = self.secondary_object

        not_openable = not isinstance(object_to_open, Openable)
        if not_openable:
            return self._outcome(NOT_OPENABLE, object_to_open)

        already_open = object_to_open.is_open
        if already_open:
            return self._outcome(ALREADY_OPEN, object_to_open)

        outcome = object_to_open.open(opening_tool)
        return self._outcome(outcome, object_to_open, opening_tool)

    def close(self):
        object_to_close = self.primary_object

        not_closable = not isinstance(object_to_close, Openable)
        if not_closable:
            return self._outcome(NOT_CLOSABLE, object_to_close)

        already_closed = not object_to_close.is_open
        if already_closed:
            return self._outcome(ALREADY_CLOSED, object_to_close)

        outcome = object_to_close.close()
        return self._outcome(outcome, object_to_close)

    def go(self):
        location_to_go = self.primary_object

        not_accessible = not isinstance(location_to_go, Accessible)
        if not_accessible:
            return self._outcome(NOT_ACCESSIBLE, location_to_go)

        already_in_location = location_to_go == self.world.current_location
        if already_in_location:
            return self._outcome(ALREADY_IN_LOCATION, location_to_go)

        connection_to_current_location = location_to_go.get_connection_to(self.world.current_location)
        if not connection_to_current_location:
            return self._outcome(NOT_ACCESSIBLE_FROM_CURRENT_LOCATION, location_to_go)

        blocked = connection_to_current_location.is_blocked
        if blocked:
            return self._outcome(blocked, connection_to_current_location)

        outcome = location_to_go.go()
        return self._outcome(outcome, location_to_go)
