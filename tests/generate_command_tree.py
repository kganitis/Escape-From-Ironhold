from itertools import product

from game.command import get_available_command_verbs


def generate_possible_commands():
    # Get available command verbs
    available_commands = get_available_command_verbs()

    # Get game element names from the game elements repository
    from game.game import Game
    game_element_names = list(Game().game_elements_repository.keys())

    # Initialize a list to store all possible commands
    possible_commands = []

    # Generate all possible 1-word commands
    possible_commands.extend(available_commands)
    possible_commands.extend(game_element_names)
    possible_commands.append("nonsense")  # Add a nonsense word to simulate unsupported words

    # Generate all possible 2-word commands
    two_word_commands = []
    for word1 in possible_commands:
        for word2 in possible_commands:
            two_word_commands.append(f"{word1} {word2}")

    # Generate all possible 3-word commands
    three_word_commands = []
    for word1 in possible_commands:
        for word2 in possible_commands:
            for word3 in possible_commands:
                three_word_commands.append(f"{word1} {word2} {word3}")

    possible_commands.extend(two_word_commands)
    possible_commands.extend(three_word_commands)

    # You now have a list of all possible commands
    return possible_commands
