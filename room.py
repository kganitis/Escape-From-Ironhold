from attributes import *


class Room(Accessible, ABC):
    def __init__(self, name, long, initial, description, parent, visited=False):
        super().__init__(name, long, initial, description, parent)
        self.visited = visited
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

    def discover(self):
        self.message(self.initial)
        self.discovered = True

    def examine(self):
        self.describe()
        for con in self.connections:
            con.discover()
        self.discover_children()
        return NO_MESSAGE
