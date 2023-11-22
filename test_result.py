from world import World


def test_commands(*input_commands):
    world = World()
    world.populate()
    result = None
    for command in input_commands:
        result = world.parse(command)
    return result


def main():
    result = test_commands(
        "take the lockpick",
        "open the door with the lockpick",
        "go to the dungeon"
    )

    # Get the verb and the objects
    print()
    action = result.action
    print(action.command.verb)
    print(action.primary_object)
    print(action.secondary_object)

    # Get any object by giving its name
    print()
    print(result.action.world.get('dungeon'))

    # Get the description, type and the outcome objects
    print()
    outcome = result.outcome
    print(outcome)
    print(outcome.description)
    print(outcome.object_names)
    print(outcome.type)


if __name__ == "__main__":
    main()
