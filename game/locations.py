# locations.py module
from game.game_objects import Location


class Cell(Location):
    def __init__(self, game, parent):
        name = "cell"
        description = "A dimly lit prison cell."
        super().__init__(game, name, description, parent)


class Dungeon(Location):
    def __init__(self, game, parent):
        name = "dungeon"
        description = "A prison dungeon."
        super().__init__(game, name, description, parent)
