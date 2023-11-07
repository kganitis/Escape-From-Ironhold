from nlp.parser import parse
from .character import *
from .items import *
from .location_connections import *
from .locations import *


class World(GameObject):
    def __init__(self):
        name = "Ironhold"
        description = "The prison of Ironhold fortress"
        super().__init__(name, description, parent=None)

        # A repository to hold every game object created
        # It maps the object's name to the actual instance of the game object
        self.game_objects_repository = {}

        self.location = None
        self.hero = Hero(parent=None)

    def populate(self):
        cell = Cell(parent=self)
        cell.add_child(self.hero)
        self.location = cell

        lockpick = LockPick(parent=cell)
        stone = Stone("stone", "A stone of the cell's walls", parent=cell)

        dungeon = Dungeon(parent=self)
        Barel("barel", "A barel just large enough to fit a person", parent=dungeon)

        lock = Lock(parent=None)
        cell_door = Door(name="door", description="A heavy wooden cell door", lock=lock, parent=self)
        cell_door.add_child(lock)
        cell_door.add_connected_locations(cell, dungeon)

    def parse(self, command):
        return parse(self, command)
