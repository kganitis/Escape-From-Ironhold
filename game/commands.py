# Quantifier functions
# Check if an arguments list contains certain arguments count
# Used to ensure that a command is followed by a valid count of arguments
def args_count_is_at_most(args, quantity):  # useful to represent the '?' quantifier, meaning 0 or 1
    return len(args) <= quantity


def args_count_is_at_least(args, quantity):  # useful to represent the '+' quantifier, meaning 1 or more
    return len(args) >= quantity


def args_count_is_not_zero_and_at_most(args, quantity):
    return len(args) > 0 and len(args) <= quantity


def args_count_is_exactly(args, quantity):  # useful to check if a command must be followed by exactly 0 or 1 argument
    return len(args) == quantity


# Define rules for the required number of arguments for each command.
# The key is the command's verb, and the value is a rule (quantifier, quantity).
# The quantifier checks if the argument count follows the quantity limitation.
# For instance, the "look" command allows at most 1 argument.
_available_commands = {
    "go": {
        "rule": (args_count_is_exactly, 1),
        "description": "Go to a specific location or in a particular direction.",
        "syntax": "go to {direction}|{location}"
    },
    "exit": {
        "rule": (args_count_is_at_most, 2),
        "description": "Exit the current location from a specified exit",
        "syntax": "exit {location} from {connection}?"
    },
    "examine": {
        "rule": (args_count_is_at_most, 1),
        "description": "Examine an item or the current location.",
        "syntax": "examine {item}?|{location}?"
    },
    "take": {
        "rule": (args_count_is_at_least, 1),
        "description": "Take the specified items.",
        "syntax": "take {item}+"
    },
    "drop": {
        "rule": (args_count_is_at_least, 1),
        "description": "Drop the specified items.",
        "syntax": "drop {item}+"
    },
    "use": {
        "rule": (args_count_is_at_least, 1),
        "description": "Use an object or perform an action using one or more objects.",
        "syntax": "use {item}+|{location_connection}+"
    },
    "lock": {
        "rule": (args_count_is_not_zero_and_at_most, 2),
        "description": "Lock a lockable object",
        "syntax": "lock {object} with {item}?"
    },
    "unlock": {
        "rule": (args_count_is_not_zero_and_at_most, 2),
        "description": "Unlock an lockable object",
        "syntax": "unlock {object} with {item}?"
    },
    "open": {
        "rule": (args_count_is_not_zero_and_at_most, 2),
        "description": "Open an object.",
        "syntax": "open {object} with {item}?"
    },
    "close": {
        "rule": (args_count_is_exactly, 1),
        "description": "Close an object.",
        "syntax": "close {object}"
    },
    "wait": {
        "rule": (args_count_is_exactly, 0),
        "description": "Wait for some hours.",
        "syntax": "wait"
    },
    "inventory": {
        "rule": (args_count_is_exactly, 0),
        "description": "Show player's inventory of items.",
        "syntax": "inventory"
    },
    "help": {
        "rule": (args_count_is_exactly, 0),
        "description": "Get assistance or see available commands.",
        "syntax": "help {command}?"
    },
}


def get_available_command_verbs():
    available_command_verbs = _available_commands.keys()
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
