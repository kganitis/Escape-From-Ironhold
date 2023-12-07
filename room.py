from attributes import *


class Room(Accessible, ABC):
    def __init__(self, name, long, initial, description, parent, visited=False, winning_room=False):
        super().__init__(name, long, initial, description, parent)
        self.visited = visited
        self.room_doors = {}   # A dictionary that maps another room to the door that connects it with self (room1: door1, room2: door2 ...)
        self.winning_room = winning_room

    def add_door(self, room_door):
        other_room = next((room for room in room_door.connected_rooms if room != self), None)
        self.room_doors[other_room] = room_door

    @property
    def scope(self):
        """
        :return: direct relatives, doors and connected rooms
        """
        scope = super().scope
        for con in self.doors:
            scope.update(con.scope)
        scope.update(self.connected_rooms)
        return scope

    @property
    def doors(self):
        return list(self.room_doors.values())

    @property
    def connected_rooms(self):
        return list(self.room_doors.keys())

    def get_door_to(self, room):
        return self.room_doors.get(room, None)

    def discover(self):
        self.message(self.initial)
        self.discovered = True

    def examine(self):
        self.describe()
        for con in self.doors:
            con.discover()
        self.discover_children()
        return NO_MESSAGE

    def go(self):
        outcome = super().go()
        if self.winning_room:
            self.player.dead = 2
        return outcome
