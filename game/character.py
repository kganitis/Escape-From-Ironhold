# character.py module
from game.game_objects import Character


class Hero(Character):
    def __init__(self, game, parent):
        name = "Hero"
        description = "A brave hero trying to escape from the Ironhold prison."
        super().__init__(game, name, description, parent)

    @property
    def inventory(self):
        return self.children

    @property
    def scope(self, modifier=None):
        scope = super().scope
        scope.update(self.game.current_location.internal_scope)
        for con in self.game.current_location.connections:
            scope.update(con.scope)
        return scope
