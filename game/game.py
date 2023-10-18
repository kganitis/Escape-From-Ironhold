# game.py module
from game.command import get_available_command_verbs, Command
from game.items import LockPick
from game.locations import Cell
from game.player import Hero


class Game:
    def __init__(self):
        # Initialize game elements here
        self.hero = Hero()
        self.starting_location = Cell()
        self.current_location = self.starting_location

        self.hero.add_item_to_inventory(LockPick())

    def run(self):
        print("Escape From Ironhold: Prison Cell")
        self.current_location.describe()
        while True:
            input_command = input("What do you want to do? (type 'help' for commands): ").lower()

            # TODO command input string is sent to nlp package for parsing, for now we do it here
            if input_command == "help":
                show_available_commands()
            elif input_command == "exit":
                print("Goodbye!")
                break
            else:
                parse_command(input_command)


def show_available_commands():
    print("Available commands:")
    print(", ".join([command for command in get_available_command_verbs()]))


def parse_command(input_command):
    # convert input_command to a command instance

    # Split the command into words
    words = input_command.lower().split()
    if not words:
        return None  # No input provided

    verb = words[0]  # The first word is the verb
    args = words[1:]  # The rest of the words are arguments

    command = Command(verb, args)
    command.execute()
