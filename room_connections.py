from game_object import *
from outcomes import *
from attributes import Openable, Lockable


class RoomConnection(GameObject, ABC):
    connected_rooms = []

    @property
    def scope(self, modifier=None):
        scope = super().scope
        scope.update(self.connected_rooms)
        return scope

    @property
    def is_blocked(self):
        return BLOCKED_CONNECTION

    def connect_rooms(self, *rooms):
        if not self.connected_rooms:
            self.connected_rooms = []
        self.connected_rooms.extend(rooms)
        for room in rooms:
            room.add_connection(self)

    def get_connected_room_from(self, coming_room):
        return next((room for room in self.connected_rooms if room != coming_room), None)


class Door(RoomConnection, Openable, Lockable):
    def __init__(self, name, long, parent, lock):
        super().__init__(name, long, None, None, parent)
        self.lock_ = lock
        self.add_child(lock)
        self.attach(lock)

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

    @property
    def initial(self):
        if self.locked:
            return "A heavy barred iron cell door separates you from the prison dungeon."
        if not self.locked and not self.is_open:
            return "A heavy barred iron cell door separates you from the prison dungeon. It's been unlocked."
        if self.is_open:
            return "The heavy barred iron cell door that separated you from the prison dungeon is open."

    @property
    def description(self):
        if self.locked:
            return "It's a heavy barred iron cell door, which separates you from the prison dungeon.\n" \
                   "You can see some things behind the iron bars, " \
                   "but you're unable to distinguish anything clearly in the darkness."
        if not self.locked and not self.is_open:
            return "It's a heavy barred iron cell door, which separates you from the prison dungeon.\n" \
                   "It has been unlocked."
        if self.is_open:
            return "The heavy barred iron cell door that separated you from the prison dungeon is now open."

    def open(self, opening_tool=None):
        if self.locked and not opening_tool:
            return BLOCKED_OBJECT_LOCKED

        if self.locked and opening_tool:
            # Generate a command to unlock the door first, before attempting to open
            result = self.world.parse(f"unlock {self} with {opening_tool}")

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


class Window(RoomConnection):
    # TODO implement a second door instead, that leads to the courtyard
    @property
    def is_blocked(self):
        return False