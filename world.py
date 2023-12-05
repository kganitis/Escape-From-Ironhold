from simple_parser import parse
from guard import *
from items import *
from player import *
from room import *
from room_connections import *


class World(GameObject):
    def __init__(self, silent=False):
        name = "Ironhold"
        long = "Ironhold fortress"
        super().__init__(name, long)

        self.silent = silent

        # A dictionary to hold every game object linked to the object tree
        # It maps the object's name to the actual instance of the game object for instant access
        self.object_map = {}

        # Variables to hold current room and player
        self.room = None
        self.hero = None

        # Hold last primary used if needed for future referal
        self.last_primary = None

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
        cell_door_lock = CellLock(
            name='lock',  # TODO change this after parser integration
            long="simple iron cell lock",  # TODO check names like this for naming conflicts during parsing
            initial="It has a simple iron lock.",
            parent=self
        )
        cell_door = CellDoor(
            name='door',
            long="heavy barred iron cell door",
            parent=self,
            lock=cell_door_lock
        )

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
            long="cell wall walls",
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

        keys = Keys(
            name='keys',
            long="old keys pair",
            description="A pair of old keys. I wonder where they fit...",
            parent=guard,
        )
        guard.attach(keys)
        # keys.fits_into = cell_door_lock

        cell_key = Key(
            name='key',  # TODO change this after parser integration
            long='old iron key',
            description='An old iron key. I wonder where it fits... Maybe into an iron lock.',
            parent=guard
        )
        cell_key.fits_into = cell_door_lock
        cell_key.concealed = True

        # Courtyard
        courtyard = Room(
            name="courtyard",
            long="Ironhold prison courtyard",
            initial="You find yourself in the Ironhold prison's courtyard, taking a taste of freedom.\n"
                    "The world is yours to explore. Good luck!",
            description="",
            parent=self,
            winning_room=True
        )
        courtyard.add_to_scope()

        # Dungeon door
        dungeon_door_lock = DungeonLock(
            name='lock2',  # TODO change this after parser integration
            long="silver dungeon lock",
            initial="It has a silver lock.",
            parent=None
        )
        dungeon_door = DungeonDoor(
            name='door2',
            long='heavy wooden dungeon door',
            parent=self,
            lock=dungeon_door_lock
        )
        dungeon_door.connect_rooms(dungeon, courtyard)
        # connect the cell to the dungeon only after the courtyard is connected to the dungeon,
        # so that the courtyard is the default exit
        cell_door.connect_rooms(cell, dungeon)

        dungeon_key = Key(
            name='key2',  # TODO change this after parser integration
            long='old silver key',
            description='An old silver key. I wonder where it fits... Maybe into a silver lock.',
            parent=guard
        )
        dungeon_key.fits_into = dungeon_door_lock
        dungeon_key.concealed = True

    def parse(self, command, advance_time=True):
        return parse(self, command, self.silent, advance_time)

    def get_all_game_object_instances(self):
        return list(self.world.object_map.values())

    def get_game_object_lexicon(self):
        game_object_dict = {}
        for obj in self.get_all_game_object_instances():
            game_object_dict[obj] = {'long': obj.long.split(), 'score': 0}
        return game_object_dict

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


