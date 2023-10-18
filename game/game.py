# game.py module
from game.command import get_available_command_verbs
from game.items import LockPick
from game.locations import Cell
from game.player import Hero


class Game:
    def __init__(self):
        # Initialize game elements here
        self.hero = Hero()
        self.starting_location = Cell()
        self.current_location = self.starting_location
        self.available_commands = get_available_command_verbs()

        self.hero.add_item_to_inventory(LockPick())

    def run(self):
        print("Escape From Ironhold: Prison Cell")
        self.current_location.describe()
        while True:
            command = input("What do you want to do? (type 'help' for commands): ").lower()
            if command == "help":
                self.show_available_commands()
            elif command == "exit":
                print("Goodbye!")
                break
            else:
                self.process_command(command)

    def show_available_commands(self):
        print("Available commands:")
        print(", ".join([command.name for command in self.available_commands]))

    def process_command(self, command):
        for cmd in self.available_commands:
            if command == cmd.name:
                pass  # execute the action corresponding to the command
        else:
            print("Command not recognized. Type 'help' for available commands.")
