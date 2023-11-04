# character.py module
from .game_object import *


class Character(GameObject, ABC):
    def __init__(self, name, description, parent):
        super().__init__(name, description, parent)


class Hero(Character):
    def __init__(self, parent):
        name = "Hero"
        description = "A brave hero trying to escape from the Ironhold prison."
        super().__init__(name, description, parent)

    @property
    def inventory(self):
        return self.children

    @property
    def scope(self, modifier=None):
        scope = super().scope
        scope.update(self.current_location.internal_scope)
        for con in self.current_location.connections:
            scope.update(con.scope)
        return scope
