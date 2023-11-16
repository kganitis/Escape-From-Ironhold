from .game_object import *
from .attributes import *


class Room(GameObject, Accessible, ABC):
    def __init__(self, name, initial, description, parent):
        super().__init__(name, initial, description, parent)
        self.room_connections = {}  # All the room connections to this room (room: connection)

    def add_connection(self, room_connection):
        other_room = next((room for room in room_connection.connected_rooms if room != self), None)
        self.room_connections[other_room] = room_connection

    @property
    def scope(self):
        """
        :return: direct relatives, connections and connected rooms
        """
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
        self.discover_children()
        for con in self.connections:
            con.discover()
        return NO_MESSAGE
