import copy
import csv

from outcomes import INVALID, FAIL
from world import World


def test_sample_commands():
    return [
        "take lockpick",
        "take keys",
        "take stone",
        'take tag',
        "drop iron key",
        "drop silver key",
        "use lockpick on door",
        "use lockpick on wooden door",
        "open door with iron key",
        "open wooden door with silver key",
        "close door",
        "go dungeon",
        "go courtyard",
        "go cell",
        "exit",
        "exit cell",
        "enter barrel",
        "exit barrel",
        "attack guard",
        "throw stone at guard",
        "throw lockpick at guard",
        "throw tag at guard",
        "ask guard",
        "tell guard",
        "wake up guard"
    ]


def generate_results(possible_commands, max_depth, file_name, filter_invalid=False, filter_failed=False):
    def save_results_to_csv(results=None):
        # Write all the fields of all result instances in the same row of the csv file
        all_result_fields = []
        for r in results:
            all_result_fields.extend(['', r.outcome.description, r.outcome.type, '.                                           .'])
        writer.writerow(all_result_fields)

    def explore(world, all_results, current_results, depth, prev_result=None):
        # end recursion
        if prev_result and (prev_result.is_fail_or_invalid() or not possible_commands or depth >= max_depth):
            all_results.append(current_results)
            # save_results_to_csv(current_results)
            return

        for cmd in possible_commands:
            world_copy = copy.deepcopy(world)
            # print(cmd)
            rlt = world_copy.parse(cmd)
            if filter_invalid and rlt.outcome.type == INVALID:
                continue
            if filter_failed and rlt.outcome.type == FAIL:
                continue
            current_results.append(rlt)
            result_set.add(('', rlt.outcome.description, rlt.outcome.type))
            outcome_set.add((rlt.outcome.description, rlt.outcome.type))
            explore(world_copy, all_results, current_results, depth + 1, rlt)
            current_results.pop()

    result_set = set()
    outcome_set = set()

    path = "results_tree/"
    # Initialize result tree csv with the headers and pass it to the explore method
    with open(path + file_name + "_tree.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['command', 'outcome', 'type', ''] * max_depth)
        world = World(silent=True)
        world.populate()
        explore(world, [], [], 0)

    # Write the result set
    with open(path + file_name + "_set.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['command', 'outcome', 'type'])
        for result in result_set:
            writer.writerow(result)

    # Write the outcome set
    with open(path + file_name + "_outcome_set.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['outcome', 'type'])
        for outcome in outcome_set:
            writer.writerow(outcome)

    print(f"{file_name} generated successfully")


def main():
    max_depth = 5
    possible_commands = test_sample_commands()
    generate_results(possible_commands, max_depth, "all_results")
    # generate_results(possible_commands, max_depth, "valid_results", filter_invalid=True)
    # generate_results(possible_commands, max_depth, "successful_results", filter_invalid=True, filter_failed=True)


if __name__ == "__main__":
    main()
