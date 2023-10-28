# game_elements.py module
from game.outcomes import *
from game.attributes import *


# Define a common parent class for all game elements (locations, items, actions etc.)
class GameElement(ABC):
    def __init__(self, game, name, description, parent=None):
        self.game = game
        self.name = name
        self.description = description
        self.parent = parent
        game.game_elements_repository[name] = self  # every game element created is added to the repository

    def __str__(self):
        return self.name

    def describe(self):
        pass


# All game elements are further represented by abstract classes
class Character(GameElement, ABC):
    def __init__(self, game, name, description, parent):
        super().__init__(game, name, description, parent)


class Item(GameElement, ABC):
    def __init__(self, game, name, description, parent):
        super().__init__(game, name, description, parent)


class LockingTool(Item, Usable, ABC):
    def __init__(self, game, name, description, parent):
        super().__init__(game, name, description, parent)
        self.can_unlock = True
        self.can_lock = True

    def use(self, target_object=None):
        if not target_object:
            return CANT_USE_OBJECT_ALONE

        if not isinstance(target_object, Lockable):
            return NOT_LOCKABLE

        return target_object.unlock(self) if target_object.locked else target_object.lock(self)


class Location(GameElement, Accessible, ABC):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)
        self.items = []  # All the items that can be found in this location
        self.location_connections = []  # All the location connections for this location

    def connected_locations(self):
        return [location for connection in self.location_connections for location in connection if location != self]

    def get_connection_to(self, location):
        connection = None
        for location_connection in self.location_connections:
            for connected_location in location_connection.connected_locations:
                if connected_location == location:
                    connection = location_connection
        return connection

    def go(self):
        current_location = self.game.current_location
        new_location = self
        connection_to_current_location = new_location.get_connection_to(current_location)

        if new_location == current_location:
            return ALREADY_IN_LOCATION

        if not connection_to_current_location:
            return CANT_ACCESS_FROM_HERE

        blocked = connection_to_current_location.is_blocked()
        if blocked:
            return blocked

        self.game.current_location = new_location
        return ACCESSED_LOCATION


class LocationConnection(GameElement, ABC):
    def __init__(self, game, name, description):
        super().__init__(game, name, description)
        self.connected_locations = []
        self.items = []  # Items found in this location connection

    def is_blocked(self):
        return BLOCKED_LOCATION
