class Outcome:
    def __init__(self, outcome, direct_object=None, indirect_object=None):
        self.outcome = outcome
        self.description = outcome[0]
        self.type = outcome[1]
        self.direct_object = direct_object
        self.indirect_object = indirect_object
        self.objects = [obj for obj in [direct_object, indirect_object] if obj is not None]

    def __str__(self):
        return f"{self.description}, {self.objects}, {self.type}"

    def __eq__(self, other):
        return self.outcome == other.outcome and self.objects == other.objects


# outcome types
SUCCESS = "SUCCESS"  # command executed successfully and the result advances the game state
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not advance the game state
FAIL = "FAIL"  # command is valid but failed to be executed
INVALID = "INVALID"  # invalid command


# outcomes (description, type)
# invalid outcomes
INVALID_COMMAND = f"Invalid command", INVALID
INVALID_OBJECTS = f"Invalid objects", INVALID
INVALID_ITEMS = f"Invalid items", INVALID
INVALID_LOCATION = f"Invalid location", INVALID

# scope outcomes
OUT_OF_SCOPE = "Object is out of scope", FAIL

# fail generic outcomes
NOT_OBTAINABLE = f"This object cannot be taken", FAIL
ALREADY_OBTAINED = f"This object is already in your possession", FAIL
NOT_HELD = f"You don't hold an object like that", FAIL
NOT_IN_POSSESSION = f"You don't possess an object like that", FAIL

NOT_USABLE = f"Object is not usable", FAIL
CANT_USE_OBJECT_ALONE = f"You must use that with something else", FAIL
MUST_USE_OBJECT_ALONE = f"You must use that alone", FAIL
CANT_USE_ON_TARGET = f"You can't use that on this target", FAIL

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
DROP_SUCCESS = f"Object dropped successfully", SUCCESS
OPEN_SUCCESS = f"Object opened", SUCCESS
OPEN_WITH_TOOL_SUCCESS = f"Object opened using a tool", SUCCESS
CLOSE_SUCCESS = f"You closed the door", SUCCESS
