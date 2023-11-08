from nlp.parser import parse
from .character import *
from .items import *
from .location_connections import *
from .locations import *


class World(GameObject):
    def __init__(self, test=False):
        name = "Ironhold"
        description = "The prison of Ironhold fortress"
        super().__init__(name, description, parent=None)

        self.test = test

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

        cell_door_lock = Lock(parent=cell)
        cell_door_key = Key(parent=cell, lockable_target=cell_door_lock)
        cell_door = Door(name="door", description="A heavy wooden cell door", parent=self, lock=cell_door_lock)
        cell_door.add_connected_locations(cell, dungeon)

        courtyard = Courtyard(parent=self)
        courtyard.add_to_scope()

    def parse(self, command):
        return parse(self, command, self.test)

    def get_all_game_object_instances(self):
        return list(self.world.game_objects_repository.values())
