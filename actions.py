from items import *
from room import *
from room_connections import *


class Action:
    def __init__(self, world, command, primary_object=None, secondary_object=None):
        self.world = world
        self.command = command
        self.primary_object = primary_object
        self.secondary_object = secondary_object

        # Dynamically get the action execution function matching the command verb
        self.execution_function = getattr(self, command.verb, None)

    @property
    def player(self):
        return self.world.player

    @property
    def objects(self):
        return [obj for obj in [self.primary_object, self.secondary_object] if obj is not None]

    def execute(self):
        if self.command.verb not in ('ask', 'tell'):
            # Retrieve the last primary if a personal pronoun is used
            if self.primary_object in ('him', 'her', 'it', 'them'):
                self.primary_object = self.world.last_primary

            invalid_objects = [obj for obj in self.objects if not isinstance(obj, GameObject)]
            if invalid_objects:
                return self.create_outcome(INVALID_OBJECTS, *invalid_objects)

            out_of_scope = [obj for obj in self.objects if obj not in self.player.scope]
            if out_of_scope:
                return self.create_outcome(OUT_OF_SCOPE, *out_of_scope)

        # Execution
        if self.execution_function and callable(self.execution_function):
            outcome = self.execution_function()
            return outcome
        else:
            raise ValueError(f"Action not found for verb: {self.command.verb}")

    def create_outcome(self, outcome, *objects):
        # Convert objects to a tuple of 2, replace any missing objects with None
        objects = (objects[0] if objects else None, objects[1] if objects and len(objects) > 1 else None)

        # The primary is always the instance's primary or the first object
        primary = self.primary_object if self.primary_object in objects else objects[0]

        # The secondary is the other, if exists and not already set as primary
        if self.secondary_object in objects and self.secondary_object != primary:
            secondary = self.secondary_object
        else:
            secondary = objects[0] if primary != objects[0] else objects[1]

        # Hold the primary for future referal
        self.world.last_primary = self.primary_object

        return Outcome(outcome, self.command.input_verb, primary, secondary)

    def wait(self):
        return self.create_outcome(WAIT)

    def examine(self):
        if self.primary_object is None:
            self.primary_object = self.player.parent
        object_to_examine = self.primary_object

        another_room = isinstance(object_to_examine, Room) and object_to_examine != self.world.current_room
        if another_room:
            return self.create_outcome(CANT_EXAMINE_FROM_CURRENT_ROOM, object_to_examine)

        outcome = object_to_examine.examine()
        return self.create_outcome(outcome, object_to_examine)

    def take(self):
        object_to_take = self.primary_object
        current_owner = self.secondary_object

        not_obtainable = not isinstance(object_to_take, Obtainable)
        if not_obtainable:
            return self.create_outcome(NOT_OBTAINABLE, object_to_take)

        already_obtained = object_to_take in self.player.owned
        if already_obtained:
            return self.create_outcome(ALREADY_OBTAINED, object_to_take)

        not_owned_by_current_owner = current_owner and object_to_take not in current_owner.owned
        if not_owned_by_current_owner:
            return self.create_outcome(NOT_OWNED_BY_OBJECT, object_to_take, current_owner)

        outcome = object_to_take.take(current_owner)
        return self.create_outcome(outcome, object_to_take, current_owner)

    def drop(self):
        object_to_drop = self.primary_object

        not_in_possession = object_to_drop not in self.player.inventory and object_to_drop not in self.player.held
        if not_in_possession:
            return self.create_outcome(NOT_IN_POSSESSION, object_to_drop)

        outcome = object_to_drop.drop()
        return self.create_outcome(outcome, object_to_drop)

    def use(self):
        object_to_use = self.primary_object
        secondary_object = self.secondary_object

        not_usable = not isinstance(object_to_use, Usable)
        if not_usable:
            return self.create_outcome(NOT_USABLE, object_to_use)

        not_in_possession = object_to_use not in self.player.owned
        if not_in_possession:
            return self.create_outcome(NOT_IN_POSSESSION, object_to_use)

        outcome = object_to_use.use(secondary_object)
        return self.create_outcome(outcome, object_to_use, secondary_object)

    def __execute_lock_or_unlock(self, operation):
        lockable_object = self.primary_object
        locking_tool = self.secondary_object

        not_lockable = not isinstance(lockable_object, Lockable)
        if not_lockable:
            return self.create_outcome(NOT_LOCKABLE, lockable_object)

        already_locked_or_unlocked = lockable_object.locked if operation == 'lock' else not lockable_object.locked
        if already_locked_or_unlocked:
            return self.create_outcome(ALREADY_LOCKED if operation == 'lock' else ALREADY_UNLOCKED, lockable_object)

        locking_tool_is_specified = locking_tool is not None
        if not locking_tool_is_specified:
            # Look for a locking tool in player's inventory
            for item in self.player.inventory:
                # First, check for a fitting key
                if lockable_object.key is not None and item == lockable_object.key:
                    locking_tool = item
                    break
                # Then, check for a lockpick
                elif lockable_object.can_be_picked and isinstance(item, LockPick):
                    locking_tool = item
                    break
                # Finally, check for any key
                elif lockable_object.key and isinstance(item, Key):
                    locking_tool = item
                    break
            if not locking_tool:
                return self.create_outcome(MISSING_LOCKING_TOOL if operation == 'lock' else MISSING_UNLOCKING_TOOL)

        if locking_tool_is_specified:
            not_a_locking_tool = not isinstance(locking_tool, LockingTool)
            if not_a_locking_tool:
                return self.create_outcome(NOT_A_LOCKING_TOOL if operation == 'lock' else NOT_AN_UNLOCKING_TOOL, locking_tool)

            locking_tool_in_inventory = locking_tool in self.player.inventory
            if not locking_tool_in_inventory:
                return self.create_outcome(NOT_IN_POSSESSION, locking_tool)

            not_fitting_key = isinstance(locking_tool, Key) and lockable_object.key != locking_tool
            if not_fitting_key:
                return self.create_outcome(NOT_FITTING_KEY, lockable_object, locking_tool)

        if operation == 'lock' and not locking_tool.can_lock:
            return self.create_outcome(CANT_LOCK_WITH_OBJECT, locking_tool)
        elif operation == 'unlock' and not locking_tool.can_unlock:
            return self.create_outcome(CANT_UNLOCK_WITH_OBJECT, locking_tool)

        outcome = lockable_object.lock(locking_tool) if operation == 'lock' else lockable_object.unlock(locking_tool)
        return self.create_outcome(outcome, lockable_object, locking_tool)

    def lock(self):
        return self.__execute_lock_or_unlock('lock')

    def unlock(self):
        return self.__execute_lock_or_unlock('unlock')

    def open(self):
        object_to_open = self.primary_object
        opening_tool = self.secondary_object

        not_openable = not isinstance(object_to_open, Openable)
        if not_openable:
            return self.create_outcome(NOT_OPENABLE, object_to_open)

        already_open = object_to_open.is_open
        if already_open:
            return self.create_outcome(ALREADY_OPEN, object_to_open)

        outcome = object_to_open.open(opening_tool)
        return self.create_outcome(outcome, object_to_open, opening_tool)

    def close(self):
        object_to_close = self.primary_object

        not_closable = not isinstance(object_to_close, Openable)
        if not_closable:
            return self.create_outcome(NOT_CLOSABLE, object_to_close)

        already_closed = not object_to_close.is_open
        if already_closed:
            return self.create_outcome(ALREADY_CLOSED, object_to_close)

        outcome = object_to_close.close()
        return self.create_outcome(outcome, object_to_close)

    def go(self):
        room_to_go = self.primary_object
        current_room = self.world.current_room

        not_accessible = not isinstance(room_to_go, Accessible)
        if not_accessible:
            return self.create_outcome(NOT_ACCESSIBLE, room_to_go)

        already_in_room = room_to_go ==  current_room
        if already_in_room:
            return self.create_outcome(ALREADY_IN_ROOM, room_to_go)

        connection_to_current_room = room_to_go.get_connection_to(current_room)
        if not connection_to_current_room:
            return self.create_outcome(NOT_ACCESSIBLE_FROM_CURRENT_ROOM, room_to_go, current_room)

        blocked = connection_to_current_room.is_blocked
        if blocked:
            return self.create_outcome(blocked, connection_to_current_room)

        outcome = room_to_go.go()
        return self.create_outcome(outcome, room_to_go)

    def enter(self):
        object_to_enter = self.primary_object

        not_enterable = not isinstance(object_to_enter, Enterable)
        if not_enterable:
            return self.create_outcome(NOT_ENTERABLE, object_to_enter)

        already_entered = self.player.parent == object_to_enter
        if already_entered:
            return self.create_outcome(ALREADY_ENTERED, object_to_enter)

        outcome = object_to_enter.enter()
        return self.create_outcome(outcome, object_to_enter)

    def exit(self):
        if isinstance(self.player.parent, Enterable):
            return self._exit_from_enterable()
        return self._exit_from_room()

    def _exit_from_enterable(self):
        if self.primary_object is None:
            self.primary_object = self.player.parent
        object_to_exit = self.primary_object

        attempt_to_exit_room_while_in_enterable = self.world.current_room in self.objects
        if attempt_to_exit_room_while_in_enterable:
            return self.create_outcome(MUST_EXIT_ENTERABLE_FIRST, self.player.parent)

        outcome = object_to_exit.exit()
        return self.create_outcome(outcome, object_to_exit)

    def _exit_from_room(self):
        current_room = self.world.current_room
        room_to_exit = None
        specified_exit = None
        for obj in self.objects:
            if obj == current_room:
                room_to_exit = obj
            if isinstance(obj, Room) and obj != current_room:
                return self.create_outcome(NOT_IN_LOCATION, obj)
            if isinstance(obj, Enterable):
                return self.create_outcome(NOT_IN_OBJECT, obj)
            if isinstance(obj, RoomConnection):
                specified_exit = obj

        if not room_to_exit:
            room_to_exit = current_room
            self.primary_object = room_to_exit

        non_existing_exit = specified_exit and specified_exit not in room_to_exit.connections
        if non_existing_exit:
            return self.create_outcome(OUT_OF_SCOPE, specified_exit)

        if not specified_exit:
            specified_exit = room_to_exit.connections[0]

        new_room = specified_exit.get_connected_room_from(current_room)
        transformed_command = f"go to {new_room}"
        self.world.parse(transformed_command)
        return self.create_outcome(COMMAND_TRANSFORMED)

    def wake(self):
        object_to_wake = self.primary_object

        not_animate = not isinstance(object_to_wake, Animate)
        if not_animate:
            return self.create_outcome(NOT_ANIMATE, object_to_wake)

        not_asleep = not object_to_wake.asleep
        if not_asleep:
            return self.create_outcome(NOT_ASLEEP, object_to_wake)

        outcome = object_to_wake.wake()
        return self.create_outcome(outcome, object_to_wake)

    def attack(self):
        object_to_attack = self.primary_object
        weapon = self.secondary_object

        not_animate = not isinstance(object_to_attack, Animate)
        if not_animate:
            return self.create_outcome(NOT_ANIMATE, object_to_attack)

        not_in_possession = weapon and weapon not in self.player.owned
        if not_in_possession:
            return self.create_outcome(NOT_IN_POSSESSION, weapon)

        outcome = object_to_attack.attack(weapon)
        return self.create_outcome(outcome, object_to_attack, weapon)

    def ask(self):
        self.primary_object = self.world.get('guard')
        object_to_ask = self.primary_object

        not_animate = not isinstance(object_to_ask, Animate)
        if not_animate:
            return self.create_outcome(NOT_ANIMATE, object_to_ask)

        outcome = object_to_ask.ask()
        return self.create_outcome(outcome, object_to_ask)

    def tell(self):
        self.primary_object = self.world.get('guard')
        object_to_tell = self.primary_object

        not_animate = not isinstance(object_to_tell, Animate)
        if not_animate:
            return self.create_outcome(NOT_ANIMATE, object_to_tell)

        outcome = object_to_tell.tell()
        return self.create_outcome(outcome, object_to_tell)

    def throw(self):
        object_to_throw = self.primary_object
        target_object = self.secondary_object

        not_in_possession = object_to_throw not in self.player.owned
        if not_in_possession:
            return self.create_outcome(NOT_IN_POSSESSION, object_to_throw)

        # "throw {object}" - without a target - is essentially "drop {object}"
        if not target_object:
            transformed_command = f"drop {object_to_throw}"
            self.world.parse(transformed_command)
            return self.create_outcome(COMMAND_TRANSFORMED)

        target_non_animate = not isinstance(target_object, Animate)
        if target_non_animate:
            outcome = object_to_throw.throw(target_object)
            return self.create_outcome(outcome, object_to_throw, target_object)

        # Swap primary and secondary, since the command now concerns the target
        self.primary_object = target_object
        self.secondary_object = object_to_throw
        outcome = target_object.throw(object_to_throw)
        return self.create_outcome(outcome, target_object, object_to_throw)
