from .game_object import *


class Room(GameObject, Accessible, ABC):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)
        self.room_connections = {}  # All the room connections to this room (room: connection)

    def add_connection(self, room_connection):
        other_room = next((room for room in room_connection.connected_rooms if room != self), None)
        self.room_connections[other_room] = room_connection

    @property
    def scope(self):
        scope = super().scope
        for con in self.connections:
            scope.update(con.scope)
        scope.update(self.connected_rooms)
        return scope

    @property
    def connections(self):
        return list(self.room_connections.values())

    @property
    def connected_rooms(self):
        return list(self.room_connections.keys())

    def get_connection_to(self, room):
        return self.room_connections.get(room)

    def examine(self):
        super().examine()
        for con in self.connections:
            con.discover()
        return EXAMINE_SUCCESS


class Cell(Room):
    def __init__(self, parent):
        super().__init__(
            name="cell",
            initial=None,
            description="You find yourself in a small, dimly lit prison cell with cold stone walls.\n"
                        "A narrow slit near the ceiling lets in feeble moonlight, revealing a straw-covered floor.\n"
                        "Iron bars separate you from the dungeon outside, and the air carries a metallic scent,\n"
                        "a reminder of the fortress's stern grip.",
            parent=parent
        )


class Dungeon(Room):
    def __init__(self, parent):
        super().__init__(
            name="dungeon",
            initial="You can see a prison dungeon.",
            description="You find yourself in the prison dungeon.",
            parent=parent
        )


class Courtyard(Room):
    def __init__(self, parent):
        super().__init__(
            name="courtyard",
            initial="You can see Ironhold prison's courtyard.",
            description="You find yourself in Ironhold prison's courtyard.",
            parent=parent
        )
