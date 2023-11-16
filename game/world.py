from nlp.simple_parser import parse
from .player import *
from .items import *
from .room_connections import *
from .room import *
from .person import *


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
        # Initialize room and player
        cell = Room(
            name="cell",
            initial=None,
            description="You find yourself in a small, dimly lit prison cell with cold stone walls.\n"
                        "A narrow slit near the ceiling lets in feeble moonlight, revealing a straw-covered floor.\n"
                        "Iron bars separate you from the dungeon outside, and the air carries a metallic scent,\n"
                        "a reminder of the fortress's stern grip.",
            parent=self
        )
        self.room = cell
        self.hero = Player(
            name="Hero",
            initial=None,
            description="You are a brave hero trying to escape from the Ironhold prison",
            parent=cell
        )

        # Dungeon
        dungeon = Room(
            name="dungeon",
            initial="You can see a prison dungeon.",
            description="You find yourself in the prison dungeon.",
            parent=self
        )

        # Cell door
        cell_door_lock = Lock(
            name='lock',
            initial="You observe a simple lock.",
            description="The lock could be picked with a lockpick, if I had one...",
            parent=None
        )
        cell_door = Door(
            name="door",
            initial="You observe a heavy barred iron cell door.",
            description="A heavy barred iron cell door.",
            parent=self,
            lock=cell_door_lock
        )
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

        dog_tag = DogTag(
            name='tag',
            initial="You observe some kind of a dog tag on the ground, near the cell's corner.",
            description="The text is worn off. Seems it was left here by a soldier...",
            parent=cell
        )

        barrel = Barrel(
            name='barrel',
            initial="You observe a wooden barrel.",
            description="The barrel is just large enough to fit a person.",
            parent=dungeon
        )

        # Guard
        guard = Guard(
            name='guard',
            initial="There's a guard sleeping right next to the cell's barred door.",
            description="The guard seems to be in deep sleep.",
            parent=cell
        )
        guard.asleep = True
        guard.add_to_scope()

        cell_door_key = Key(
            name='key',
            initial="A key hangs from the guard's belt. Maybe it's within your reach.",
            description="An old iron key. I wonder where it fits...",
            parent=guard,
        )
        cell_door_key.fits_into = cell_door_lock
        guard.attach(cell_door_key)

        # Courtyard
        courtyard = Room(
            name="courtyard",
            initial="You can see Ironhold prison's courtyard.",
            description="You find yourself in Ironhold prison's courtyard.",
            parent=self
        )
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
