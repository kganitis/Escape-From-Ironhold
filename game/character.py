from .game_object import *


class Character(GameObject, ABC):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)


class Hero(Character):
    def __init__(self, parent):
        super().__init__(
            name="Hero",
            initial=None,
            description="You are a brave hero trying to escape from the Ironhold prison",
            parent=parent
        )

    @property
    def inventory(self):
        return self.children

    @property
    def held(self):
        return self.inventory

    @property
    def scope(self, modifier=None):
        scope = super().scope
        scope.update(self.current_room.scope)
        for obj in self.world.get_all_game_object_instances():
            if obj.added_to_scope and obj not in scope:
                scope.add(obj)
        return scope
