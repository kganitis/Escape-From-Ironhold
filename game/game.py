# game.py module
from chatbot.chatbot import *
from game.locations import Cell
from game.character import Hero
from game.command import Command, show_available_commands
from game.actions import Action
from game.outcomes import *


class Game:
    def __init__(self):
        # A repository to hold every game element created
        # Using the element's name, we'll be able to retrieve the instance of the game element
        # Useful for matching command arguments to actual instances of game elements
        self.game_elements_repository = {}

        self.result_history = []

        # Initialize game elements here
        self.player = Hero(self)
        self.current_location = Cell(self)

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

            print(f"\nOutcome: {result.outcome}")
            message = generate_message(result)
            print(f"Message: {message}")

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
            outcome = INVALID_COMMAND

        # Update the result, then return it
        command.result.outcome, command.result.type = outcome
        if isinstance(command.result.outcome, tuple):
            raise ValueError(f"Outcome {command.result.outcome} is a tuple [Command: ({command})")
        self.result_history.append(command.result)
        return command.result

    def execute(self, command):
        # Convert argument stings to actual instances of game elements, retrieved from the game elements repository
        game_elements = [self.game_elements_repository.get(arg, arg) for arg in command.args]

        action = Action(command.verb, game_elements)
        if action.is_executable():
            outcome = action.execute()
        else:
            raise ValueError(f"Action not found for verb: {command.verb}")

        if not isinstance(outcome, tuple):
            raise ValueError(f"Outcome {outcome} does not have a type")
        return outcome
