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
        "description": "Go to the specified room.",
        "syntax": "go to the {room}",
        "examples": ["Go to the dungeon"]
    },
    "exit": {
        "rule": (words_count_is_at_most, 2),
        "description": "Exit the current room (from a specified exit).",
        "syntax": "exit the {room}? from the {connection}?",
        "examples": ["Exit", "Exit the cell", "Exit the dungeon from the window"]
    },
    "examine": {
        "rule": (words_count_is_at_most, 1),
        "description": "Examine the current room (or an object).",
        "syntax": "examine the {object}?|{room}?",
        "examples": ["Examine", "Examine the cell", "Examine the door"]
    },
    "take": {
        "rule": (words_count_is_exactly, 1),
        "description": "Take the specified item.",
        "syntax": "take the {item}",
        "examples": ["Take the lockpick"]
    },
    "drop": {
        "rule": (words_count_is_exactly, 1),
        "description": "Drop the specified item.",
        "syntax": "drop the {item}",
        "examples": ["Drop the lockpick"]
    },
    "use": {
        "rule": (words_count_is_not_zero_and_at_most, 2),
        "description": "Use an object (with/on another object).",
        "syntax": "use the {object} on/with the {object}?",
        "examples": ["Use the lockpick", "Use the lockpick on the lock"]
    },
    "lock": {
        "rule": (words_count_is_not_zero_and_at_most, 2),
        "description": "Lock a lockable object (with a specified item).",
        "syntax": "lock the {object} with the {item}?",
        "examples": ["Lock the door", "Lock the door with the key"]
    },
    "unlock": {
        "rule": (words_count_is_not_zero_and_at_most, 2),
        "description": "Unlock an unlockable object (with a specified item).",
        "syntax": "unlock the {object} with the {item}?",
        "examples": ["Unlock the lock", "Unlock the lock with the lockpick"]
    },
    "open": {
        "rule": (words_count_is_not_zero_and_at_most, 2),
        "description": "Open an object (with a specified item).",
        "syntax": "open the {object} with the {item}?",
        "examples": ["Open the door", "Open the door with the lockpick"]
    },
    "close": {
        "rule": (words_count_is_exactly, 1),
        "description": "Close an object.",
        "syntax": "close the {object}"
    },
    # "wait": {
    #     "rule": (words_count_is_exactly, 0),
    #     "description": "Wait for some hours.",
    #     "syntax": "wait"
    # },
    # "inventory": {
    #     "rule": (words_count_is_exactly, 0),
    #     "description": "Show player's inventory of items.",
    #     "syntax": "inventory"
    # },
    "help": {
        "rule": (words_count_is_at_most, 2),
        "description": "See available commands or get help for a specific command.",
        "syntax": "help {command}? {examples}?",
        "examples": ["Help", "Help take", "Help take examples"]
    }
}


def get_available_command_verbs():
    available_command_verbs = list(_available_commands.keys())
    return available_command_verbs


def show_available_commands():
    print("Available commands:")
    print(", ".join([command for command in get_available_command_verbs()]))


def show_syntax_for_verb(verb):
    print(f"Syntax for {verb}:")
    print(_available_commands[verb]['syntax'])


def show_examples_for_verb(verb):
    print(f"Examples for {verb}:")
    print(", ".join([example for example in _available_commands[verb]['examples']]))


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
