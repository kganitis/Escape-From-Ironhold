# result types
SUCCESS = "SUCCESS"  # command executed successfully and the result advances the game state
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not advance the game state
FAIL = "FAIL"  # command is valid but failed to be executed
INVALID = "INVALID"  # invalid command


def create_outcome(outcome_const, *args):
    outcome_text, outcome_type = outcome_const
    args = args[0] if args and isinstance(args[0], list) else list(args)
    args = [f"{arg}" for arg in args]
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

NOT_USABLE = f"Object is not usable", FAIL
CANT_USE_OBJECT = f"You can't use that this way", FAIL
CANT_USE_OBJECT_ALONE = f"You must use that with something else", FAIL
MUST_USE_OBJECT_ALONE = f"You must use that alone", FAIL

CANT_GO_TO_LOCATION = f"Can't go to that location", FAIL
ALREADY_IN_LOCATION = f"Already in this location", FAIL
CANT_ACCESS_FROM_HERE = f"Can't access that from your current location", FAIL
BLOCKED_LOCATION = f"Location is blocked", FAIL

NOT_LOCKABLE = f"Can't be (un)locked", FAIL
CANT_LOCK = f"You can't lock that this way", FAIL
ALREADY_LOCKED = "Object already locked", FAIL
MISSING_LOCKING_TOOL = f"Missing a locking tool", FAIL

NOT_UNLOCKABLE = f"Can't be (un)locked", FAIL
CANT_UNLOCK = f"You can't unlock that this way", FAIL
ALREADY_UNLOCKED = "Object already unlocked", FAIL

LOCKING_TOOL_LOCK_FAIL = f"Can't lock with that", FAIL
LOCKING_TOOL_UNLOCK_FAIL = f"Can't unlock with that", FAIL

NOT_OPENABLE = f"Can't be opened", FAIL
CANT_OPEN_OBJECT = f"You can't open that now", FAIL
ALREADY_OPEN = "Object already open", FAIL

NOT_CLOSABLE = f"Can't be closed", FAIL
CANT_CLOSE_OBJECT = f"You can't close that now", FAIL
ALREADY_CLOSED = "Object already closed", FAIL


# successful generic outcomes
ACCESSED_LOCATION = f"Accessed the location", SUCCESS
LOCK_SUCCESS = f"Object locked", SUCCESS
UNLOCK_SUCCESS = f"Object unlocked", SUCCESS
TAKE_SUCCESS = f"Object taken", SUCCESS

# object specific outcomes
# door
DOOR_OPENED_SUCCESS = f"You opened the door", SUCCESS
DOOR_CLOSED_SUCCESS = f"You closed the door", SUCCESS
DOOR_LOCKED_FAIL = f"The door is locked and must be unlocked first", FAIL
DOOR_CLOSED_FAIL = f"The door is closed and must be opened first", FAIL
DOOR_OPEN_FAIL = f"The door is open and must be closed first", FAIL


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
