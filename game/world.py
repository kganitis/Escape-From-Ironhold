from nlp.simple_parser import parse
from .character import *
from .items import *
from .room_connections import *
from .rooms import *


class World(GameObject):
    def __init__(self, test=False):
        name = "Ironhold"
        super().__init__(name)

        self.test = test

        # A repository to hold every game object created
        # It maps the object's name to the actual instance of the game object
        self.game_objects_repository = {}

        self.room = None
        self.hero = Hero(parent=None)

    def populate(self):
        # Cell
        cell = Cell(parent=self)
        cell.add_child(self.hero)
        self.room = cell

        # Dungeon
        dungeon = Dungeon(parent=self)

        # Cell door
        cell_door_lock = Lock(
            name='lock',
            initial="You observe a simple lock.",
            description="The lock could be picked with a lockpick, if I had one...",
            parent=None
        )
        cell_door_key = Key(
            name='key',
            initial="You observe an old key.",
            description="An old key. I wonder where it fits...",
            parent=cell,
            lockable_target=cell_door_lock
        )
        cell_door = Door(
            name="door",
            initial="You observe a heavy barred iron cell door.",
            description="A heavy barred iron cell door.",
            parent=self,
            lock=cell_door_lock
        )
        cell_door.add_child(cell_door_lock)
        cell_door.connect_rooms(cell, dungeon)

        # Cell items
        lockpick = LockPick(
            name='lockpick',
            initial="You find a rusty iron lockpick hidden under the mattress.",
            description="It's a lockpick that can be used to pick locks.",
            parent=cell
        )
        lockpick.concealed = True

        mattress = Mattress(
            name='mattress',
            initial="You observe a straw mattress on the floor.",
            description="The straw mattress doesn't seem comfortable but it's better than nothing.",
            parent=cell
        )

        stone = Stone(
            name='stone',
            initial="You observe a loose stone in the cell's stone walls.",
            description="A stone of the cell's walls. Doesn't seem very useful.",
            parent=cell
        )

        barel = Barel(
            name='barel',
            initial="You observe a wooden barel.",
            description="The barel is  just large enough to fit a person.",
            parent=dungeon
        )

        # Courtyard
        courtyard = Courtyard(parent=self)
        courtyard.add_to_scope()

        cell_window = Window(
            name='window',
            initial="You observe an open window in the dungeon's wall.",
            description="The window leads to the prison's courtyard.",
            parent=self
        )
        cell_window.connect_rooms(dungeon, courtyard)

    def parse(self, command):
        return parse(self, command, self.test)

    def get_all_game_object_instances(self):
        return list(self.world.game_objects_repository.values())

    def get(self, name):
        return self.game_objects_repository.get(name, name)
