from abc import ABC
from outcomes import *


# Define a common parent class for all game objects (rooms, items, characters etc.)
class GameObject(ABC):
    def __init__(self, name, long, initial=None, description=None, parent=None):
        self.name = name
        self.long = long

        # Descriptions
        self._initial = initial
        self._description = description

        # Object Tree
        self.parent = parent
        if parent:
            parent.add_child(self)
        self.children = []

        # Relations
        self.attached = []
        self.discovered = False
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
# Description Properties
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def initial(self):
        if self._initial:
            return self._initial
        return f"{self.article(self.long)} {self.long}."

    @initial.setter
    def initial(self, value):
        self._initial = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Object Tree Properties
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def siblings(self):
        if self.parent:
            return [child for child in self.parent.children if child != self]
        return []

    @property
    def owned(self):
        return set(self.children + self.attached)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Description Methods
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
        self.message(f"- {self.initial}")
        self.discovered = True

    def discover_children(self):
        for child in self.children:
            child.discover()

    def discover_attached(self):
        for attached in self.attached:
            attached.discover()

    def message(self, message):
        if not self.world.test:
            if message.strip()[-1] not in ".!":
                message = message + '.'
            print(message)

    def article(self, word):
        first_word = word.split()[0] if ' ' in word else word
        if first_word and first_word[0].lower() in 'aeiou':
            return 'An'
        return 'A'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Object Tree Methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self
        # Every game object linked to the world object tree is also added to the object map
        obj.update_object_map()

    def remove(self):
        if self.parent:
            self.parent.children.remove(self)
        if self.is_attached_to(self.parent):
            self.parent.remove_attached(self)
        self.parent = None

    def move_to(self, new_parent):
        self.remove()
        new_parent.add_child(self)

    def update_object_map(self):
        self.world.object_map[self.name] = self

    def get(self, name):
        return self.world.get(name)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Relations Methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def attach(self, obj):
        self.attached.append(obj)

    def remove_attached(self, obj):
        self.attached.remove(obj)

    def is_attached_to(self, game_object):
        return self in game_object.attached

    def has_attached(self, game_object):
        return game_object in self.attached

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

    @property
    def is_last_move_of_turn(self):
        return self.world.current_move == self.world.MOVES_PER_TURN
