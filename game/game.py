# game.py module
from game.locations import Cell
from game.player import Hero
from game.command import Command, show_available_commands
from game.actions import Action


class Game:
    def __init__(self):
        # A repository to hold every game element created
        # Using the element's name, we'll be able to retrieve the instance of the game element
        # Useful for matching command arguments to actual instances of game elements
        self.game_elements_repository = {}
        self.result_history = []

        # Initialize game elements here
        self.hero = Hero(self)
        self.starting_location = Cell(self)
        self.current_location = self.starting_location

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
                result = self.parse(input_command)

            # TODO send result to chatbot for processing, for now we print the outcome here
            print("\n" + result.outcome)

    def parse(self, input_command):
        # Split the command into words
        words = input_command.split()
        if not words:
            return None
        verb = words[0]  # The first word is the verb
        args = words[1:] if len(words) > 1 else None  # The rest of the words, if more exist, are arguments

        # Execute the command
        command = Command(verb, args)
        if command.is_valid():
            outcome = self.execute(command)
        else:
            outcome = (f"Invalid command: {command}", False)

        # Update, then return the result
        command.result.outcome, command.result.advance_game_state = outcome
        if command.result.advance_game_state:
            self.result_history.append(command.result)
        return command.result

    def execute(self, command):
        # Convert argument stings to actual instances of game elements, retrieved from game elements repository
        game_elements = [self.game_elements_repository.get(arg, arg) for arg in command.args]
        action = Action(command.verb, game_elements)
        if action.is_executable():
            outcome = action.execute()
        else:
            raise ValueError(f"Action not found for verb: {command.verb}")
        return outcome if isinstance(outcome, tuple) else (outcome, False)
