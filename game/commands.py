# Quantifier functions
# Check if an arguments list contains certain arguments count
# Used to ensure that a command is followed by a valid count of arguments
def words_count_is_at_most(words, quantity):  # useful to represent the '?' quantifier, meaning 0 or 1
    return len(words) <= quantity


def words_count_is_at_least(words, quantity):  # useful to represent the '+' quantifier, meaning 1 or more
    return len(words) >= quantity


def words_count_is_not_zero_and_at_most(words, quantity):
    return len(words) > 0 and len(words) <= quantity


def words_count_is_exactly(words, quantity):  # useful to check if a command must be followed by exactly 0 or 1 argument
    return len(words) == quantity


# Define rules for the required number of arguments for each command.
# The key is the command's verb, and the value is a rule (quantifier, quantity).
# The quantifier checks if the word count follows the quantity limitation.
# For example, the "examine" command must be followed by 1 word at most.
_available_commands = {
    "go": {
        "rule": (words_count_is_exactly, 1),
        "description": "Go to a specific room or in a particular direction.",
        "syntax": "go to {direction}|{room}"
    },
    "exit": {
        "rule": (words_count_is_at_most, 2),
        "description": "Exit the current room from a specified exit",
        "syntax": "exit {room} from {connection}?"
    },
    "examine": {
        "rule": (words_count_is_at_most, 1),
        "description": "Examine an item or the current room.",
        "syntax": "examine {item}?|{room}?"
    },
    "take": {
        "rule": (words_count_is_at_least, 1),
        "description": "Take the specified items.",
        "syntax": "take {item}+"
    },
    "drop": {
        "rule": (words_count_is_at_least, 1),
        "description": "Drop the specified items.",
        "syntax": "drop {item}+"
    },
    "use": {
        "rule": (words_count_is_at_least, 1),
        "description": "Use an object or perform an action using one or more objects.",
        "syntax": "use {item}+|{room_connection}+"
    },
    "lock": {
        "rule": (words_count_is_not_zero_and_at_most, 2),
        "description": "Lock a lockable object",
        "syntax": "lock {object} with {item}?"
    },
    "unlock": {
        "rule": (words_count_is_not_zero_and_at_most, 2),
        "description": "Unlock an lockable object",
        "syntax": "unlock {object} with {item}?"
    },
    "open": {
        "rule": (words_count_is_not_zero_and_at_most, 2),
        "description": "Open an object.",
        "syntax": "open {object} with {item}?"
    },
    "close": {
        "rule": (words_count_is_exactly, 1),
        "description": "Close an object.",
        "syntax": "close {object}"
    },
    "wait": {
        "rule": (words_count_is_exactly, 0),
        "description": "Wait for some hours.",
        "syntax": "wait"
    },
    "inventory": {
        "rule": (words_count_is_exactly, 0),
        "description": "Show player's inventory of items.",
        "syntax": "inventory"
    },
    "help": {
        "rule": (words_count_is_exactly, 0),
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
    def __init__(self, verb, words=None):
        self.verb = verb
        # Make sure words is a list
        if words is None:
            words = []
        if not isinstance(words, list):
            words = [word for word in words]
        self.words = words

    def __str__(self):
        return f"{self.verb} {' '.join(self.words)}"

    def is_valid(self):
        if self.verb not in get_available_command_verbs():
            return False

        quantifier_function, words_count_limitation = _available_commands[self.verb]["rule"]
        if not quantifier_function(self.words, words_count_limitation):
            return False

        return True
