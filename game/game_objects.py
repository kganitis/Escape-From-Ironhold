# game_objects.py module
from game.outcomes import *
from game.attributes import *


# Define a common parent class for all game objects (locations, items, actions etc.)
class GameObject(ABC):
    def __init__(self, game, name, description, parent=None):
        self.game = game
        self.name = name
        self.description = description
        self.parent = parent
        if parent:
            parent.add_child(self)
        self.children = []
        self.attached = []
        game.game_objects_repository[name] = self  # every game object created is added to the repository

    @property
    def player(self):
        return self.game.player

    @property
    def scope(self):
        scope = set()
        self.__update_scope(scope)
        return scope

    @property
    def internal_scope(self):
        scope = set()
        self.__update_scope(scope, 'internal')
        return scope

    @property
    def siblings(self):
        if self.parent:
            return [child for child in self.parent.children if child != self]
        else:
            return []

    def __update_scope(self, scope, modifier=None):
        if self in scope:
            return
        scope.add(self)

        if modifier and modifier.lower() != 'internal':
            scope.add(self.parent)
            for sibling in self.siblings:
                sibling.__update_scope(scope, modifier)

        for child in self.children:
            child.__update_scope(scope, modifier)

        for attached in self.attached:
            attached.__update_scope(scope, modifier)

    def __str__(self):
        return self.name

    def describe(self):
        pass

    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self

    def remove(self):
        self.parent.children.remove(self)
        self.parent = None

    def move_to(self, new_parent):
        self.remove()
        new_parent.add_child(self)

    def attach(self, obj):
        self.attached.append(obj)
        obj.attached.append(self)


# All game objects are further represented by abstract classes
class Character(GameObject, ABC):
    def __init__(self, game, name, description, parent):
        super().__init__(game, name, description, parent)


class Item(GameObject, ABC):
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


class Location(GameObject, Accessible, ABC):
    def __init__(self, game, name, description, parent):
        super().__init__(game, name, description, parent)
        self.location_connections = {}  # All the location connections to this location

    @property
    # All the items that can be found in this location
    def items(self):
        return self.children

    def add_connection(self, location_connection):
        for location in location_connection.connected_locations:
            self.location_connections[location] = location_connection

    @property
    def connections(self):
        return list(self.location_connections.values())

    def get_connection_to(self, location):
        return self.location_connections.get(location)

    def go(self):
        current_location = self.game.current_location
        new_location = self
        if new_location == current_location:
            return ALREADY_IN_LOCATION

        connection_to_current_location = new_location.get_connection_to(current_location)
        if not connection_to_current_location:
            return CANT_ACCESS_FROM_HERE

        blocked = connection_to_current_location.is_blocked()
        if blocked:
            return blocked

        self.player.move_to(new_location)
        self.game.game_world.current_location = new_location
        return ACCESSED_LOCATION


class LocationConnection(GameObject, ABC):
    def __init__(self, game, name, description, parent):
        super().__init__(game, name, description, parent)
        self.connected_locations = []

    @property
    # Items found in this location connection
    def items(self):
        return self.children

    def add_connected_locations(self, *locations):
        invalid_locations = [str(loc) for loc in locations if not isinstance(loc, Location)]
        if invalid_locations:
            raise ValueError(f"Invalid location(s): {invalid_locations}")
        self.connected_locations.extend(locations)
        for loc in locations:
            loc.add_connection(self)

    def is_blocked(self):
        return BLOCKED_LOCATION
