# commands.py module
from game.result import Result


# Quantifier functions
# Check if an arguments list contains certain arguments count
# Used to ensure that a command is followed by a valid count of arguments
def __args_count_is_at_most(args, quantity):  # useful to represent the '?' quantifier, meaning 0 or 1
    return len(args) <= quantity


def __args_count_is_at_least(args, quantity):  # useful to represent the '+' quantifier, meaning 1 or more
    return len(args) >= quantity


def __args_count_is_not_zero_and_at_most(args, quantity):
    return len(args) > 0 and len(args) <= quantity


def __args_count_is_exactly(args, quantity):  # useful to check if a command must be followed by exactly 0 or 1 argument
    return len(args) == quantity


# Define rules for the required number of arguments for each command.
# The key is the command's verb, and the value is a rule (quantifier, quantity).
# The quantifier checks if the argument count follows the quantity limitation.
# For instance, the "look" command allows at most 1 argument.
_available_commands = {
    "go": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Go to a specific location or in a particular direction.",
        "syntax": "go {direction}|{location}"
    },
    "examine": {
        "rule": (__args_count_is_at_most, 1),
        "description": "Examine an item or the current location.",
        "syntax": "examine {item}?|{location}?"
    },
    "take": {
        "rule": (__args_count_is_at_least, 1),
        "description": "Take the specified items.",
        "syntax": "take {item}+"
    },
    "use": {
        "rule": (__args_count_is_at_least, 1),
        "description": "Use an object or perform an action using one or more objects.",
        "syntax": "use {item}+|{location_connection}+"
    },
    "combine": {
        "rule": (__args_count_is_at_least, 1),
        "description": "Combine two or more items.",
        "syntax": "combine {item} {item}+"
    },
    "lock": {
        "rule": (__args_count_is_not_zero_and_at_most, 2),
        "description": "Lock a lockable object",
        "syntax": "lock {object} with {item}?"
    },
    "unlock": {
        "rule": (__args_count_is_not_zero_and_at_most, 2),
        "description": "Unlock an lockable object",
        "syntax": "unlock {object} {item}?"
    },
    "open": {
        "rule": (__args_count_is_not_zero_and_at_most, 2),
        "description": "Open an object.",
        "syntax": "open {object} {item}?"
    },
    "close": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Close an object.",
        "syntax": "close {object}"
    },
    "talk": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Talk to a character.",
        "syntax": "talk {character}"
    },
    "fight": {
        "rule": (__args_count_is_exactly, 1),
        "description": "Engage in a fight with a character.",
        "syntax": "fight {character}"
    },
    "wait": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Wait for some hours.",
        "syntax": "wait"
    },
    "inventory": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Show player's inventory of items.",
        "syntax": "inventory"
    },
    "help": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Get assistance or see available commands.",
        "syntax": "help {command}?"
    },
    "exit": {
        "rule": (__args_count_is_exactly, 0),
        "description": "Exit the game.",
        "syntax": "help"
    }
}


def get_available_command_verbs():
    available_command_verbs = _available_commands.keys()
    available_command_verbs = ["take", "use", "lock", "unlock", "open", "close", "go"]  # TODO delete this once all commands have been implemented
    return available_command_verbs


def show_available_commands():
    print("Available commands:")
    print(", ".join([command for command in get_available_command_verbs()]))


class Command:
    def __init__(self, verb, args=None):
        self.verb = verb
        # Make sure args is a list
        if args is None:
            args = []
        if not isinstance(args, list):
            args = [arg for arg in args]
        self.args = args

    def __str__(self):
        return f"{self.verb} {' '.join(self.args)}"

    def is_valid(self):
        if self.verb not in get_available_command_verbs():
            return False

        quantifier_function, args_count_limitation = _available_commands[self.verb]["rule"]
        if not quantifier_function(self.args, args_count_limitation):
            return False

        return True
