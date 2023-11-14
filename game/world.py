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

        # A dictionary to hold every game object linked to the object tree
        # It maps the object's name to the actual instance of the game object for instant access
        self.game_objects_repository = {}

        self.room = None
        self.hero = None

    def populate(self):
        # Initialize room and hero
        cell = Cell(parent=self)
        self.room = cell
        self.hero = Hero(parent=cell)

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
        # mattress.after['examine'] =

        cell_wall = Wall(
            name='wall',
            initial="You can feel some cold air entering the cell. Maybe there's a crack somewhere in the walls.",
            description="The cell walls are made of stone, some are large and heavy, others are very small and barely into place.",
            parent=cell,
        )
        cell_wall.transparent = True

        stone = Stone(
            name='stone',
            initial="You observe a loose small stone in the cell's stone walls. Maybe it can be removed...",
            description="A small stone of the cell's walls. Doesn't seem very useful.",
            parent=cell_wall
        )
        stone.after['take'] = "You manage to remove the stone from the wall but you see nothing of interest."

        barrel = Barrel(
            name='barrel',
            initial="You observe a wooden barrel.",
            description="The barrel is just large enough to fit a person.",
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
