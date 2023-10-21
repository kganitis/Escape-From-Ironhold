# game.py module
from game.command import get_available_command_verbs
from game.locations import Cell
from game.player import Hero
from tests.generate_command_tree import generate_possible_commands


class Game:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Game, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    # noinspection PyAttributeOutsideInit
    def initialize(self):
        # A repository to hold every game element created
        # Using the element's name, we'll be able to retrieve the instance of the game element
        # Useful for matching command arguments to actual instances of game elements
        self.__game_elements_repository = {}

        # Initialize game elements here
        self.hero = Hero()
        self.starting_location = Cell()
        self.current_location = self.starting_location

    def reset(self):
        # Reset the game state to initial values
        self.initialize()

    def update_game_elements_repository(self, game_element):
        self.__game_elements_repository[game_element.name] = game_element

    def get_game_element(self, game_element_name):
        return self.__game_elements_repository.get(game_element_name, game_element_name)

    def get_all_game_elements(self):
        return self.__game_elements_repository.keys()

    def run(self):
        print("Escape From Ironhold: Prison Cell")
        self.current_location.describe()
        while True:
            print("\nWhat do you want to do? (type 'help' for commands)")
            input_command = input("> ").strip().lower()

            # TODO send command input string to nlp package for parsing

            # further parse the command to translate it into an in game action
            if input_command == "help":
                show_available_commands()
                continue
            elif input_command == "exit":
                print("Goodbye!")
                break
            elif input_command == '':
                print("Empty input!")
                continue
            else:
                result = parse_command(input_command)

            # TODO send result to chatbot for processing, for now we print the outcome here
            print("\n" + result.outcome)

    # Collect the results from all possible commands
    def generate_possible_results(self):
        results = []
        for command in generate_possible_commands():
            results.append(parse_command(command))
            self.reset()
        return results


def show_available_commands():
    print("Available commands:")
    print(", ".join([command for command in get_available_command_verbs()]))


def parse_command(input_command):
    # Split the command into words
    words = input_command.split()
    if not words:
        return None

    verb = words[0]  # The first word is the verb
    args = words[1:] if len(words) > 1 else None  # The rest of the words, if more exist, are arguments

    from game.command import Command
    command = Command(verb, args)
    return command.execute()
