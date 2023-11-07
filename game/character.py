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
    def held(self):
        return self.inventory

    @property
    def scope(self, modifier=None):
        scope = super().scope
        scope.update(self.current_location.internal_scope)
        for con in self.current_location.connections:
            scope.update(con.scope)
        for obj in self.world.get_all_game_object_instances():
            if obj.added_to_scope and obj not in scope:
                scope.add(obj)
        return scope