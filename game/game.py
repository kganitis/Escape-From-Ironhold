# game.py module
from game.command import get_available_command_verbs, Command
from game.locations import Cell
from game.player import Hero


class Game:
    def __init__(self):
        # Initialize game elements here
        self.hero = Hero()
        self.starting_location = Cell()
        self.current_location = self.starting_location

    def run(self):
        print("Escape From Ironhold: Prison Cell")
        self.current_location.describe()
        while True:
            print("\nWhat do you want to do? (type 'help' for commands)")
            input_command = input("> ").lower()

            # TODO send command input string to nlp package for parsing

            # further parse the command to translate it into an in game action
            if input_command == "help":
                show_available_commands()
                continue
            elif input_command == "exit":
                print("Goodbye!")
                break
            else:
                result = parse_command(input_command)

            # TODO send result to chatbot for processing, for now we print the outcome here
            print()
            print(result.outcome)


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
    args = words[1:] if len(words) > 1 else None  # The rest of the words, if more exist, are arguments

    command = Command(verb, args)
    return command.execute()
