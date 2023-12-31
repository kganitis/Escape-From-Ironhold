from outcomes import *
from attributes import Openable, Lockable


class Door(Openable, Lockable):
    def __init__(self, name, long, parent, lock):
        super().__init__(name, long, None, None, parent)
        self.connected_rooms = []
        self.lock_ = lock
        self.add_child(lock)
        self.attach(lock)

    @property
    def scope(self, modifier=None):
        scope = super().scope
        scope.update(self.connected_rooms)
        return scope

    def connect_rooms(self, *rooms):
        if not self.connected_rooms:
            self.connected_rooms = []
        self.connected_rooms.extend(rooms)
        for room in rooms:
            room.add_door(self)

    def get_connected_room_from(self, coming_room):
        return next((room for room in self.connected_rooms if room != coming_room), None)

    @property
    def key(self):
        return self.lock_.key

    @property
    def can_be_picked(self):
        return self.lock_.can_be_picked

    @property
    def locked(self):
        return self.lock_.locked

    @property
    def is_blocked(self):
        if self.locked:
            return BLOCKED_OBJECT_LOCKED
        if not self.is_open:
            return BLOCKED_OBJECT_CLOSED
        return False

    def open(self, opening_tool=None):
        if self.locked and not opening_tool:
            return BLOCKED_OBJECT_LOCKED

        if self.locked and opening_tool:
            # Generate a command to unlock the door first, before attempting to open
            result = self.world.parse(f"unlock {self.long} with {opening_tool}", advance_time=False)

            if result.outcome.outcome != UNLOCK_SUCCESS:
                return NO_MESSAGE

        self.is_open = True
        return OPEN_SUCCESS

    def lock(self, locking_tool):
        if self.is_open:
            return MUST_CLOSE_OBJECT
        return self.lock_.lock(locking_tool)

    def unlock(self, unlocking_tool):
        return self.lock_.unlock(unlocking_tool)


class CellDoor(Door):
    @property
    def textual(self):
        return "heavy barred iron door"

    @property
    def initial(self):
        if self.locked:
            return f"A {self} separates you from the prison dungeon."
        if not self.locked and not self.is_open:
            return f"A {self} separates you from the prison dungeon.\n" \
                   f"It's been unlocked."
        if self.is_open:
            return f"The {self} that separated you from the prison dungeon is open."

    @property
    def description(self):
        if self.locked:
            return f"It's a {self}, which separates you from the prison dungeon.\n" \
                   "You can see some things behind the iron bars, " \
                   "but you're unable to distinguish anything clearly in the darkness."
        if not self.locked and not self.is_open:
            return f"It's a {self}, which separates you from the prison dungeon.\n" \
                   "It has been unlocked."
        if self.is_open:
            return f"The {self} that separated you from the prison dungeon is now open."


class DungeonDoor(Door):
    @property
    def textual(self):
        return "heavy wooden door"

    @property
    def initial(self):
        if self.locked:
            return f"A {self} separates you from the prison's courtyard."
        if not self.locked and not self.is_open:
            return f"A {self} separates you from the prison's courtyard.\n" \
                   f"It's been unlocked."
        if self.is_open:
            return f"The {self} that leads to the prison's courtyard is open."

    @property
    def description(self):
        if self.locked:
            return f"It's a {self}, which separates you from freedom.\n" \
                   "It has to lead to the prison's courtyard."
        if not self.locked and not self.is_open:
            return f"It's a {self}, which separates you from the prison's courtyard.\n" \
                   "It has been unlocked."
        if self.is_open:
            return f"The {self} that leads to the prison's courtyard is now open."

    def open(self, opening_tool=None):
        outcome = super().open(opening_tool)
        if outcome == OPEN_SUCCESS:
            self.message(f"The {self} opens and reveals your way to freedom.\n"
                         f"The prison's courtyard seems safe for the time.\n"
                         f"You may proceed.")
            return NO_MESSAGE
        return outcome
