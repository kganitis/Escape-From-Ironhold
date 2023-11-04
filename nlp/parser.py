# parse.py module
from game.commands import Command
from game.actions import Action
from game.outcomes import INVALID_COMMAND
from game.result import Result


def parse(world, input_command):
    # Split the command into words
    words = input_command.split()
    verb = words[0]  # The first word is the verb
    args = words[1:] if len(words) > 1 else None  # The rest of the words, if more exist, are arguments

    # Create the command and check syntax
    command = Command(verb, args)
    if not command.is_valid():
        outcome_text, outcome_type = INVALID_COMMAND
        return [Result(command, outcome_text, [], outcome_type)]

    # Map argument stings to actual instances of game objects, retrieved from the game objects repository
    game_objects = [world.game_objects_repository.get(arg, arg) for arg in command.args]
    # Execute the command
    action = Action(world, command, game_objects)
    return action.execute()
