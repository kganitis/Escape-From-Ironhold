from .attributes import *


# Define a common parent class for all game objects (locations, items, actions etc.)
class GameObject(ABC):
    def __init__(self, name, description, parent):
        self.name = name
        self.description = description
        self.parent = parent
        if parent:
            parent.add_child(self)
        self.children = []
        self.attached = []

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
    def current_location(self):
        return self.world.location

    @current_location.setter
    def current_location(self, value):
        self.world.location = value

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
        obj.update_game_objects_repository()  # every game object created is added to the repository

    def remove(self):
        self.parent.children.remove(self)
        self.parent = None

    def move_to(self, new_parent):
        self.remove()
        new_parent.add_child(self)

    def attach(self, obj):
        self.attached.append(obj)
        obj.attached.append(self)

    def update_game_objects_repository(self):
        self.world.game_objects_repository[self.name] = self
