from .game_object import *


class Player(GameObject):
    @property
    def inventory(self):
        return self.children

    @property
    def held(self):
        return self.inventory

    @property
    def scope(self):
        """
        :return: direct relatives, room scope and any other object added to scope
        """
        scope = super().scope
        scope.update(self.current_room.scope)
        for obj in self.world.get_all_game_object_instances():
            if obj.added_to_scope and obj not in scope:
                scope.add(obj)
        return scope
