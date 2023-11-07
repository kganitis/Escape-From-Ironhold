from .items import *
from .location_connections import *
from .locations import *
from .result import *


class Action:
    def __init__(self, world, command, direct_object=None, indirect_object=None):
        self.world = world
        self.command = command
        self.direct_object = direct_object
        self.indirect_object = indirect_object
        self.objects = [obj for obj in [direct_object, indirect_object] if obj is not None]

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
        # Syntax Analysis
        invalid_objects = [obj for obj in self.objects if not isinstance(obj, GameObject)]
        out_of_scope = [obj for obj in self.objects if obj not in self.scope]
        if invalid_objects:
            self.produce_result(INVALID_OBJECTS, invalid_objects)
            return self.results
        if out_of_scope:
            self.produce_result(OUT_OF_SCOPE, out_of_scope)
            return self.results

        # Execution
        if self.execution_function and callable(self.execution_function):
            self.execution_function()
            return self.results
        else:
            raise ValueError(f"Action not found for verb: {self.command.verb}")

    def produce_result(self, outcome_const, *args):
        result = Result(self.command, *create_outcome(outcome_const, *args))
        self.results.append(result)

    def take(self):
        object_to_take = self.direct_object

        not_obtainable = not isinstance(object_to_take, Obtainable)
        if not_obtainable:
            return self.produce_result(NOT_OBTAINABLE, object_to_take)

        already_obtained = object_to_take in self.player.inventory
        if already_obtained:
            return self.produce_result(ALREADY_OBTAINED, object_to_take)

        outcome = object_to_take.take()
        self.produce_result(outcome, object_to_take)

    def drop(self):
        object_to_drop = self.direct_object

        not_in_possession = object_to_drop not in self.player.inventory and object_to_drop not in self.player.held
        if not_in_possession:
            return self.produce_result(NOT_IN_POSSESSION, object_to_drop)

        outcome = object_to_drop.drop()
        self.produce_result(outcome, object_to_drop)

    def use(self):
        object_to_use = self.direct_object
        second_object = self.indirect_object

        not_usable = not isinstance(object_to_use, Usable)
        if not_usable:
            return self.produce_result(NOT_USABLE, object_to_use)

        not_held = object_to_use not in self.player.held
        if not_held:
            return self.produce_result(NOT_HELD, object_to_use)

        outcome = object_to_use.use(second_object)
        self.produce_result(outcome, object_to_use, second_object)

    def __execute_lock_or_unlock(self, operation):
        lockable_object = self.direct_object
        locking_tool = self.indirect_object

        not_lockable = not isinstance(lockable_object, Lockable)
        if not_lockable:
            return self.produce_result(NOT_LOCKABLE, lockable_object)

        already_locked_or_unlocked = lockable_object.locked if operation == 'lock' else not lockable_object.locked
        if already_locked_or_unlocked:
            return self.produce_result(ALREADY_LOCKED if operation == 'lock' else ALREADY_UNLOCKED, lockable_object)

        not_a_locking_tool = locking_tool is not None and not isinstance(locking_tool, LockingTool)
        if not_a_locking_tool:
            return self.produce_result(NOT_A_LOCKING_TOOL if operation == 'lock' else NOT_AN_UNLOCKING_TOOL, locking_tool)

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
                return self.produce_result(MISSING_LOCKING_TOOL if operation == 'lock' else MISSING_UNLOCKING_TOOL)

        if operation == 'lock' and not locking_tool.can_lock:
            return self.produce_result(LOCKING_TOOL_LOCK_FAIL, locking_tool)
        elif operation == 'unlock' and not locking_tool.can_unlock:
            return self.produce_result(LOCKING_TOOL_UNLOCK_FAIL, locking_tool)

        outcome = lockable_object.lock(locking_tool) if operation == 'lock' else lockable_object.unlock(locking_tool)
        self.produce_result(outcome, lockable_object, locking_tool)

    def lock(self):
        self.__execute_lock_or_unlock('lock')

    def unlock(self):
        self.__execute_lock_or_unlock('unlock')

    def open(self):
        object_to_open = self.direct_object
        opening_tool = self.indirect_object

        not_openable = not isinstance(object_to_open, Openable)
        if not_openable:
            return self.produce_result(NOT_OPENABLE, object_to_open)

        already_open = object_to_open.is_open
        if already_open:
            return self.produce_result(ALREADY_OPEN, object_to_open)

        outcome = object_to_open.open(opening_tool)
        self.produce_result(outcome, object_to_open, opening_tool)

    def close(self):
        object_to_close = self.direct_object

        not_closable = not isinstance(object_to_close, Openable)
        if not_closable:
            return self.produce_result(NOT_CLOSABLE, object_to_close)

        already_closed = not object_to_close.is_open
        if already_closed:
            return self.produce_result(ALREADY_CLOSED, object_to_close)

        outcome = object_to_close.close()
        self.produce_result(outcome, object_to_close)

    def go(self):
        location_to_go = self.direct_object

        not_accessible = not isinstance(location_to_go, Accessible)
        if not_accessible:
            return self.produce_result(NOT_ACCESSIBLE, location_to_go)

        already_in_location = location_to_go == self.world.current_location
        if already_in_location:
            return self.produce_result(ALREADY_IN_LOCATION, location_to_go)

        connection_to_current_location = location_to_go.get_connection_to(self.world.current_location)
        if not connection_to_current_location:
            return self.produce_result(NOT_ACCESSIBLE_FROM_CURRENT_LOCATION, location_to_go)

        blocked = connection_to_current_location.is_blocked
        if blocked:
            return self.produce_result(blocked, connection_to_current_location)

        outcome = location_to_go.go()
        self.produce_result(outcome, location_to_go)
