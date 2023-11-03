from .game_objects import *
from .character import *
from .location_connections import *
from .locations import *
from .items import *


class World(GameObject):
    def __init__(self, game):
        name = "Ironhold"
        description = "The prison of Ironhold fortress"
        super().__init__(game, name, description)

        self.current_location = None
        self.hero = Hero(game, parent=None)

    def populate(self):
        game = self.game
        cell = Cell(game, parent=self)
        cell.add_child(self.hero)
        self.current_location = cell

        lockpick = LockPick(game, parent=cell)

        dungeon = Dungeon(game, parent=self)
        Barel(game, "barel", "Just a barel", parent=dungeon)

        cell_door = Door(game, name="door", description="A heavy wooden cell door", parent=self)
        cell_door.add_connected_locations(cell, dungeon)
