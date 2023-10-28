# result types
SUCCESS = "SUCCESS"  # command executed successfully and the result advances the game state
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not advance the game state
FAIL = "FAIL"  # command is valid but failed to be executed
INVALID = "INVALID"  # invalid command


# outcomes
# invalid outcomes
INVALID_COMMAND = f"Invalid command", INVALID
INVALID_OBJECT = f"Invalid object", INVALID
INVALID_ITEMS = f"Invalid item(s)", INVALID
INVALID_LOCATION = f"Invalid location", INVALID


# fail generic outcomes
NOT_USABLE = f"Object is not usable", FAIL
CANT_USE_OBJECT = f"You can't use that this way", FAIL
CANT_USE_OBJECT_ALONE = f"You must use that with something else", FAIL
MUST_USE_OBJECT_ALONE = f"You must use that alone", FAIL

NOT_COMBINABLE = f"Items are not combinable", FAIL
MUST_BE_COMBINED = f"Must combine that with something else", FAIL
CANT_COMBINE = f"Can't combine these this way", FAIL

CANT_GO_TO_LOCATION = f"Can't go to that location", FAIL
ALREADY_IN_LOCATION = f"Already in this location", FAIL
CANT_ACCESS_FROM_HERE = f"Can't access that from your current location", FAIL
BLOCKED_LOCATION = f"Location is blocked", FAIL

NOT_LOCKABLE = f"Can't be (un)locked", FAIL
CANT_LOCK = f"You can't lock that this way", FAIL
MISSING_LOCKING_TOOL = f"Missing a locking tool", FAIL
ALREADY_LOCKED = "Object already locked", FAIL

NOT_UNLOCKABLE = f"Can't be unlocked", FAIL
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

# object specific outcomes
# door
DOOR_OPENED_SUCCESS = f"You opened the door", SUCCESS
DOOR_CLOSED_SUCCESS = f"You closed the door", SUCCESS
DOOR_LOCKED_FAIL = f"The door is locked and must be unlocked first", FAIL
DOOR_CLOSED_FAIL = f"The door is closed and must be opened first", FAIL
DOOR_OPEN_FAIL = f"The door is open and must be closed first", FAIL
