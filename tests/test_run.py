import copy
import csv

from game.command import *
from game.game import Game
from game.outcomes import *


def sample_possible_commands():
    return [
        "use lock lockpick",
        "use door",
        "go dungeon",
        "nonsense"
    ]


def more_possible_commands():
    return [
        "combine lockpick lock",
        "combine nonsense nonsense",
        "combine lock lock",
        "combine lock",
        "combine nonsense",
        "combine",
        "use lock lockpick",
        "use nonsense nonsense",
        "use lock lock",
        "use door",
        "use lockpick",
        "use nonsense",
        "use",
        "go cell",
        "go dungeon",
        "go nonsense",
        "go",
        "nonsense"
    ]


def prefilter_invalid_commands(unfiltered_commands):
    filtered_commands = []
    for cmd in unfiltered_commands:
        words = cmd.split()
        if not words:
            return None
        verb = words[0]
        args = words[1:] if len(words) > 1 else None

        command = Command(verb, args)
        if command.is_valid():
            filtered_commands.append(cmd)
    return filtered_commands


def generate_possible_commands():
    # Get available command verbs
    available_commands = get_available_command_verbs()

    # Get game element names from the game elements repository
    game_element_names = list(Game().game_elements_repository.keys())

    # Initialize a list to store all possible commands
    possible_commands = []

    # Generate all possible 1-word commands
    possible_commands.extend(available_commands)
    possible_commands.extend(game_element_names)
    possible_commands.append("nonsense")  # a word to simulate unsupported words

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


def generate_results(available_commands, max_depth, file_name, filter_invalid=False, filter_failed=False):
    def save_results_to_csv(results=None):
        # Write all the fields of all result instances in the same row of the csv file
        all_result_fields = []
        for r in results:
            all_result_fields.extend([r.command, r.outcome, r.type, '.                                           .'])
        writer.writerow(all_result_fields)

    def explore(game_instance, possible_commands, all_results, current_results, depth, prev_result=None):
        # end recursion
        if prev_result and (prev_result.is_fail_or_error() or not possible_commands or depth >= max_depth):
            all_results.append(current_results)
            # save_results_to_csv(current_results)
            return

        for cmd in possible_commands:
            game_copy = copy.deepcopy(game_instance)
            rlt = game_copy.parse(cmd)
            if filter_invalid and rlt.type == INVALID:
                continue
            if filter_failed and rlt.type == FAIL:
                continue
            current_results.append(rlt)
            result_set.add((rlt.command, rlt.outcome, rlt.type))
            outcome_set.add((rlt.outcome, rlt.type))
            explore(game_copy, possible_commands, all_results, current_results, depth + 1, rlt)
            current_results.pop()

    result_set = set()
    outcome_set = set()

    # Initialize result tree csv with the headers and pass it to the explore method
    with open(file_name + "_tree.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['command', 'outcome', 'type', ''] * max_depth)
        explore(Game(test=True), available_commands, [], [], 0)

    # Write the result set
    with open(file_name + "_set.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['command', 'outcome', 'type'])
        for result in result_set:
            writer.writerow(result)

    # Write the outcome set
    with open(file_name + "_outcome_set.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['outcome', 'type'])
        for outcome in outcome_set:
            writer.writerow(outcome)

    print(f"{file_name} generated successfully")


def main():
    max_depth = 3
    possible_commands = generate_possible_commands()
    filtered_commands = prefilter_invalid_commands(possible_commands)
    generate_results(possible_commands, max_depth, "all_results")
    generate_results(filtered_commands, max_depth, "valid_results", filter_invalid=True)
    generate_results(filtered_commands, max_depth, "successful_results", filter_invalid=True, filter_failed=True)


if __name__ == "__main__":
    main()
