from .attributes import *


# Define a common parent class for all game objects (rooms, items, characters etc.)
class GameObject(ABC):
    def __init__(self, name, initial=None, description=None, parent=None):
        self.name = name

        # Descriptions
        self.initial = initial
        self.description = description
        self.discoverable_children = True
        # Messages before and after an action takes place for this game object (action: message)
        self.before = {}
        self.after = {}

        # First degree relatives
        self.parent = parent
        if parent:
            parent.add_child(self)
        self.children = []

        # Relations to other objects
        self.attached = []
        self.added_to_scope = False
        self.concealed = False

    @property
    def world(self):
        if self.parent is None:
            return self
        else:
            return self.parent.world

    @property
    def player(self):
        return self.world.hero

    @property
    def current_room(self):
        return self.world.room

    @current_room.setter
    def current_room(self, value):
        self.world.room = value

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

    def add_to_scope(self):
        self.added_to_scope = True

    def remove_from_scope(self):
        self.added_to_scope = False

    def __str__(self):
        return self.name

    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self
        # Every game object linked to the world object tree is also added to the objects repository
        obj.update_game_objects_repository()

    def remove(self):
        self.parent.children.remove(self)
        self.parent = None

    def move_to(self, new_parent):
        self.remove()
        new_parent.add_child(self)

    def attach(self, obj):
        self.attached.append(obj)
        obj.attached.append(self)

    def examine(self):
        self.describe()
        if self.discoverable_children:
            self.discover_children()
        return EXAMINE_SUCCESS

    def describe(self):
        self.print_message(self.description)

    def discover(self):
        if self.initial:
            self.print_message(self.initial)

    def discover_children(self):
        for child in self.children:
            if not child.concealed:
                child.discover()

    def print_message(self, message):
        if not self.world.test:
            print(message)

    def update_game_objects_repository(self):
        self.world.game_objects_repository[self.name] = self
