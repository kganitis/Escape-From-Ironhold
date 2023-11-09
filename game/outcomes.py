class Outcome:
    def __init__(self, outcome, primary_object=None, secondary_object=None):
        self.outcome = outcome
        self.description, self.type = outcome
        self.primary_object = primary_object
        self.secondary_object = secondary_object
        self.objects = [obj for obj in [primary_object, secondary_object] if obj is not None]

    def __str__(self):
        return f"{self.description}, {self.object_names}, {self.type}"

    def __eq__(self, other):
        return self.outcome == other.outcome and self.objects == other.objects

    @property
    def object_names(self):
        return [str(obj) for obj in self.objects]

    @property
    def formatted_description(self):
        formatted_description = self.description.format(
            primary=self.primary_object,
            secondary=self.secondary_object
        )
        return formatted_description


# outcome types
SUCCESS = "SUCCESS"  # command executed successfully and the result alters the game world
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not alter the game world
FAIL = "FAIL"  # command is valid but failed to be executed
INVALID = "INVALID"  # invalid command
TRANSFORMED = "TRANSFORMED"  # the initial command was transformed


# outcomes (description, type)
# special
COMMAND_TRANSFORMED = "", TRANSFORMED

# invalid outcome
INVALID_COMMAND = "Invalid command", INVALID
INVALID_OBJECTS = "Invalid objects", INVALID
INVALID_ITEMS = "Invalid items", INVALID
INVALID_LOCATION = "Invalid location", INVALID

# scope outcomes
OUT_OF_SCOPE = "The {primary} is out of scope", FAIL
NON_EXISTING_OBJECT = "There isn't any {primary} around", FAIL

# fail generic outcomes
NOT_OBTAINABLE = "The {primary} cannot be taken", FAIL
ALREADY_OBTAINED = "The {primary} is already in your possession", FAIL
NOT_HELD = "You're not holding any {primary}", FAIL
NOT_IN_POSSESSION = "There isn't any {primary} in your possession", FAIL

NOT_USABLE = "The {primary} is not usable", FAIL
CANT_USE_OBJECT_ALONE = "You must use the {primary} with something else", FAIL
MUST_USE_OBJECT_ALONE = "You must use the {primary} alone", FAIL
CANT_USE_OBJECT_ON_TARGET = "You can't use the {primary} on the {secondary}", FAIL

NOT_ACCESSIBLE = "The {primary} is not accessible", FAIL
ALREADY_IN_LOCATION = "Already in {primary}", FAIL
NOT_ACCESSIBLE_FROM_CURRENT_LOCATION = "The {primary} is not accessible from {secondary}", FAIL
BLOCKED_CONNECTION = "The {primary} is blocked", FAIL
BLOCKED_OBJECT_LOCKED = "The {primary} is locked and must be unlocked first", FAIL
BLOCKED_OBJECT_CLOSED = "The {primary} is closed and must be opened first", FAIL

NOT_IN_LOCATION = "You're not in the {primary} at the moment", FAIL
UNSPECIFIED_EXIT = "There are multiple exits from the {primary}. You must specify one", FAIL

NOT_LOCKABLE = "The {primary} can't be (un)locked", FAIL
ALREADY_LOCKED = "The {primary} is already locked", FAIL
ALREADY_UNLOCKED = "The {primary} is already unlocked", FAIL
NOT_A_LOCKING_TOOL = "The {primary} can't be used for locking", FAIL
NOT_AN_UNLOCKING_TOOL = "The {primary} can't be used for unlocking", FAIL
MISSING_LOCKING_TOOL = "You need something that can lock", FAIL
MISSING_UNLOCKING_TOOL = "You need something that can unlock", FAIL
CANT_LOCK_WITH_OBJECT = "The {primary} can't be used for locking", FAIL
CANT_UNLOCK_WITH_OBJECT = "The {primary} can't be used for unlocking", FAIL

NOT_OPENABLE = "The {primary} can't be opened", FAIL
ALREADY_OPEN = "The {primary} is already open", FAIL

NOT_CLOSABLE = "The {primary} can't be closed", FAIL
ALREADY_CLOSED = "The {primary} is already closed", FAIL

MUST_CLOSE_OBJECT = "The {primary} is open and must be closed first", FAIL

# successful generic outcomes
ACCESS_LOCATION_SUCCESS = "You accessed the {primary} successfully", SUCCESS
LOCK_SUCCESS = "You locked the {primary} successfully using the {secondary}", SUCCESS
UNLOCK_SUCCESS = "You unlocked the {primary} successfully using the {secondary}", SUCCESS
TAKE_SUCCESS = "You took the {primary} successfully", SUCCESS
DROP_SUCCESS = "You dropped the {primary} successfully", SUCCESS
OPEN_SUCCESS = "You opened the {primary} successfully", SUCCESS
OPEN_WITH_TOOL_SUCCESS = "You opened the {primary} successfully using the {secondary}", SUCCESS
CLOSE_SUCCESS = "You closed the {primary} successfully", SUCCESS
