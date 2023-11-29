from simple_parser import parse
from guard import *
from items import *
from player import *
from room import *
from room_connections import *


class World(GameObject):
    def __init__(self, test=False):
        name = "Ironhold"
        long = "Ironhold fortress"
        super().__init__(name, long)

        self.test = test

        # A dictionary to hold every game object linked to the object tree
        # It maps the object's name to the actual instance of the game object for instant access
        self.object_map = {}

        # Variables to hold current room and player
        self.room = None
        self.hero = None

        # Moves and turns
        self.MOVES_PER_TURN = 5
        self.current_move = 1

    def populate(self):
        # Initialize room and player
        cell = Room(
            name="cell",
            long="Ironhold prison cell",
            initial="As you slowly regain consciousness, you find yourself in a small, dimly lit prison cell with cold stone walls.\n"
                    "Your head throbs with pain, and the memories of your surroundings begin to piece together.\n"
                    "You are John Silver, a soldier wrongly accused and now locked away in the prison of Ironhold fortress.",
            description="You are in a small, dimly lit prison cell with cold stone walls.\n"
                    "A narrow slit near the ceiling lets in feeble moonlight, revealing a straw-covered floor.\n"
                    "Iron bars separate you from the dungeon outside, and the air carries a metallic scent,\n"
                    "a reminder of the fortress's stern grip.",
            parent=self
        )
        self.room = cell
        self.hero = Player(
            name="John Silver",
            long="John Silver",
            description="You are John Silver, a soldier wrongly accused and now locked away in the prison of Ironhold fortress.",
            parent=cell
        )
        self.hero.concealed = True

        # Dungeon
        dungeon = Room(
            name="dungeon",
            long="prison dungeon",
            initial="Stepping out of your cramped cell, you enter the heart of the prison dungeon.\n"
                    "The corridor, hewn from ancient stone, stretches in both directions.\n"
                    "Distant torches flicker, casting dancing shadows on the cold, damp walls.\n"
                    "The air is thick with the musty scent of forgotten secrets.",
            description="You stand in the prison dungeon, surrounded by the echoes of countless stories etched into the very stone.\n"
                        "The corridor, dimly lit by flickering torches, reveals a maze of cells, each a silent witness to the passage of time.\n"
                        "The distant sound of dripping water adds a haunting melody to the quiet symphony of captivity.",
            parent=self
        )

        # Cell door
        cell_door_lock = Lock(
            name='lock',
            long="simple iron lock",
            initial="It has a simple iron lock.",
            parent=None
        )
        cell_door = Door(
            name="door",
            long="heavy barred iron cell door",
            parent=self,
            lock=cell_door_lock
        )
        cell_door.connect_rooms(cell, dungeon)

        # Cell items
        lockpick = LockPick(
            name='lockpick',
            long="rusty iron lockpick",
            description="It's a lockpick that can be used to pick locks.",
            parent=cell
        )
        lockpick.concealed = True

        cell_wall = Wall(
            name='wall',
            long="cell walls",
            initial="You can feel some cold air entering the cell. Maybe there's a crack somewhere in the walls.",
            description="The cell walls are made of stone, some are large and heavy, others are very small and barely into place.",
            parent=cell,
        )
        cell_wall.transparent = True

        mattress = Mattress(
            name='mattress',
            long="straw mattress",
            initial="A straw mattress on the floor for the prisoners to sleep.",
            description="The straw mattress doesn't seem comfortable but it's better than nothing.",
            parent=cell
        )

        stone = Stone(
            name='stone',
            long="small stone",
            parent=cell_wall
        )

        dog_tag = DogTag(
            name='tag',
            long="metallic dog tag",
            description="The text is worn off. Seems it was left behind by a veteran...",
            parent=cell
        )

        barrel = Barrel(
            name='barrel',
            long="large wooden barrel",
            description="The barrel is just large enough to fit a person.",
            parent=dungeon
        )

        # Guard
        guard = Guard(
            name='guard',
            long="guard",
            parent=cell
        )
        guard.asleep = True
        guard.add_to_scope()

        cell_door_key = Key(
            name='key',
            long="old iron key",
            description="An old iron key. I wonder where it fits...",
            parent=guard,
        )
        cell_door_key.fits_into = cell_door_lock
        guard.attach(cell_door_key)

        # Courtyard
        courtyard = Room(
            name="courtyard",
            long="Ironhold prison courtyard",
            initial="You find yourself in the Ironhold prison's courtyard.",
            description="You find yourself in the Ironhold prison's courtyard.",
            parent=self
        )
        courtyard.add_to_scope()

        cell_window = Window(
            name='window',
            long="dungeon window",
            initial="You observe an open window in the dungeon's walls.",
            description="The window seems to lead to the prison's courtyard.",
            parent=self
        )
        cell_window.connect_rooms(dungeon, courtyard)

    def parse(self, command):
        return parse(self, command, self.test)

    def get_all_game_object_instances(self):
        return list(self.world.object_map.values())

    def get(self, name):
        return self.object_map.get(name, name)

    def on_move_end(self):
        for obj in self.get_all_game_object_instances():
            obj.on_move_end()
        self.current_move += 1
        if self.current_move > self.MOVES_PER_TURN:
            self.current_move = 1
            self.on_turn_end()

    def on_turn_end(self):
        for obj in self.get_all_game_object_instances():
            obj.on_turn_end()


