# result types
SUCCESS = "SUCCESS"  # command executed successfully and the result advances the game state
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not advance the game state
FAIL = "FAIL"  # command is valid but failed to be executed
INVALID = "INVALID"  # invalid command


def create_outcome(outcome_const, *args):
    outcome_text, outcome_type = outcome_const
    args = args[0] if args and isinstance(args[0], list) else list(args)
    args = [f"{arg}" for arg in args if arg]
    return outcome_text, args, outcome_type


# outcomes
# invalid outcomes
INVALID_COMMAND = f"Invalid command", INVALID
INVALID_OBJECTS = f"Invalid objects", INVALID
INVALID_ITEMS = f"Invalid items", INVALID
INVALID_LOCATION = f"Invalid location", INVALID

# scope outcomes
OUT_OF_SCOPE = f"Object is out of scope", FAIL

# fail generic outcomes
NOT_OBTAINABLE = f"This object cannot be taken", FAIL
ALREADY_OBTAINED = f"This object is already in your possession", FAIL

NOT_HELD = f"You don't hold an object like that", FAIL

NOT_USABLE = f"Object is not usable", FAIL
CANT_USE_OBJECT_ALONE = f"You must use that with something else", FAIL
MUST_USE_OBJECT_ALONE = f"You must use that alone", FAIL

NOT_ACCESSIBLE = f"Location is not accessible", FAIL
ALREADY_IN_LOCATION = f"Already in this location", FAIL
NOT_ACCESSIBLE_FROM_CURRENT_LOCATION = f"Location is not accessible from your current location", FAIL
BLOCKED_CONNECTION = f"Connection between locations is blocked", FAIL
BLOCKED_OBJECT_LOCKED_FAIL = f"The object is locked and must be unlocked first", FAIL
BLOCKED_OBJECT_CLOSED_FAIL = f"The object is closed and must be opened first", FAIL

NOT_LOCKABLE = f"Can't be (un)locked", FAIL
ALREADY_LOCKED = "Object already locked", FAIL
ALREADY_UNLOCKED = "Object already unlocked", FAIL
NOT_A_LOCKING_TOOL = f"Can't use that for locking", FAIL
NOT_AN_UNLOCKING_TOOL = f"Can't use that for unlocking", FAIL
MISSING_LOCKING_TOOL = f"Missing a locking tool", FAIL
MISSING_UNLOCKING_TOOL = f"Missing an unlocking tool", FAIL
LOCKING_TOOL_LOCK_FAIL = f"Can't lock with that", FAIL
LOCKING_TOOL_UNLOCK_FAIL = f"Can't unlock with that", FAIL

NOT_OPENABLE = f"Can't be opened", FAIL
ALREADY_OPEN = "Object already open", FAIL

NOT_CLOSABLE = f"Can't be closed", FAIL
ALREADY_CLOSED = "Object already closed", FAIL

OBJECT_OPEN_FAIL = f"The object is open and must be closed first", FAIL

# successful generic outcomes
ACCESSED_LOCATION_SUCCESS = f"Accessed the location", SUCCESS
LOCK_SUCCESS = f"Object locked", SUCCESS
UNLOCK_SUCCESS = f"Object unlocked", SUCCESS
TAKE_SUCCESS = f"Object taken from its previous owner", SUCCESS
OPEN_SUCCESS = f"Object opened", SUCCESS
OPEN_WITH_TOOL_SUCCESS = f"Object opened using a tool", SUCCESS
CLOSE_SUCCESS = f"You closed the door", SUCCESS


def test_outcome_function():
    # Test a single outcome constant without arguments
    result = create_outcome(NOT_OBTAINABLE)
    assert result == (NOT_OBTAINABLE[0], [], NOT_OBTAINABLE[1])

    # Test a single outcome constant with a single argument
    result = create_outcome(NOT_OBTAINABLE, "arg1")
    assert result == (NOT_OBTAINABLE[0], ["arg1"], NOT_OBTAINABLE[1])

    # Test a single outcome constant with arguments as separate parameters
    result = create_outcome(NOT_OBTAINABLE, "arg1", "arg2", "arg3")
    assert result == (NOT_OBTAINABLE[0], ["arg1", "arg2", "arg3"], NOT_OBTAINABLE[1])

    # Test a single outcome constant with a list of arguments
    result = create_outcome(NOT_OBTAINABLE, ["arg1", "arg2", "arg3"])
    assert result == (NOT_OBTAINABLE[0], ["arg1", "arg2", "arg3"], NOT_OBTAINABLE[1])


test_outcome_function()
