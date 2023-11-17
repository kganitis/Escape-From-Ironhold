from abc import ABC
from .outcomes import *


# Define a common parent class for all game objects (rooms, items, characters etc.)
class GameObject(ABC):
    def __init__(self, name, initial=None, description=None, parent=None):
        self.name = name

        # Descriptions
        self.initial = initial
        self.description = description
        # Messages before and after an action takes place for this game object (action: message)
        self.before = {}
        self.after = {}

        # Object Tree
        self.parent = parent
        if parent:
            parent.add_child(self)
        self.children = []

        # Relations
        self.attached = []
        self.added_to_scope = False
        self.transparent = False
        self.concealed = False

    def __str__(self):
        return self.name

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# World Properties
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Scope Properties
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Object Tree Properties
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def siblings(self):
        if self.parent:
            return [child for child in self.parent.children if child != self]
        else:
            return []

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Descriptions Methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def examine(self):
        self.describe()
        if self == self.current_room or self.transparent:
            self.discover_children()
        self.discover_attached()
        return NO_MESSAGE

    def describe(self):
        self.message(self.description)

    def discover(self):
        if self.concealed:
            return
        if self.initial:
            self.message(self.initial)

    def discover_children(self):
        for child in self.children:
            child.discover()

    def discover_attached(self):
        for attached in self.attached:
            attached.discover()

    def message(self, message):
        if not self.world.test:
            print(message)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Object Tree Methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self
        # Every game object linked to the world object tree is also added to the objects repository
        obj.update_object_map()

    def remove(self):
        self.parent.children.remove(self)
        if self.is_attached_to(self.parent):
            self.parent.remove_attached(self)
        self.parent = None

    def move_to(self, new_parent):
        self.remove()
        new_parent.add_child(self)

    def update_object_map(self):
        self.world.object_map[self.name] = self

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Relations Methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def attach(self, obj):
        self.attached.append(obj)
        obj.attached.append(self)

    def remove_attached(self, obj):
        self.attached.remove(obj)
        obj.attached.remove(self)

    def is_attached_to(self, game_object):
        return game_object in self.attached

    def has_attached(self, game_object):
        return game_object in self.attached

    @property
    def owned(self):
        return set(self.children + self.attached)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Scope Methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Other Methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def on_move_end(self):
        return

    def on_turn_end(self):
        return
