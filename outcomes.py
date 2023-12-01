class Outcome:
    def __init__(self, outcome, primary_object=None, secondary_object=None):
        self.outcome = outcome
        self.primary_object = primary_object
        self.secondary_object = secondary_object

    def __str__(self):
        return f"{self.description}, {self.object_names}, {self.type}"

    def __eq__(self, other):
        return self.outcome == other.outcome and self.objects == other.objects

    @property
    def description(self):
        return self.outcome[0]

    @property
    def type(self):
        return self.outcome[1]

    @property
    def objects(self):
        return [obj for obj in [self.primary_object, self.secondary_object] if obj is not None]

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


# Outcome types
SUCCESS = "SUCCESS"  # command executed successfully and the result alters the game world
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not alter the game world
FAIL = "FAIL"  # command is valid but failed to be executed
INVALID = "INVALID"  # invalid command
TRANSFORMED = "TRANSFORMED"  # the initial command was transformed to a new command to be executed in its place instead

# Special outcomes
COMMAND_TRANSFORMED = False, TRANSFORMED

# Invalid outcomes
INVALID_COMMAND = "You can't do that.", INVALID
INVALID_OBJECTS = "I don't understand what you're talking about.", INVALID

# Scope outcomes
OUT_OF_SCOPE = "I don't see any {primary} around", FAIL
NON_EXISTING_OBJECT = "There isn't any {primary} around", FAIL

# Fail outcomes
CANT_EXAMINE_FROM_CURRENT_ROOM = "You can't examine the {primary} from here", FAIL

NOT_OBTAINABLE = "The {primary} cannot be taken", FAIL
ALREADY_OBTAINED = "The {primary} is already in your possession", FAIL
NOT_HELD = "You're not holding any {primary}", FAIL
NOT_IN_POSSESSION = "There isn't any {primary} in your possession", FAIL
NOT_OWNED_BY_OBJECT = "The {secondary} doesn't have any {primary}", FAIL

NOT_USABLE = "The {primary} is not usable", FAIL
CANT_USE_OBJECT_ALONE = "You must use the {primary} with something else", FAIL
MUST_USE_OBJECT_ALONE = "You must use the {primary} alone", FAIL
CANT_USE_OBJECT_ON_TARGET = "You can't use the {primary} on the {secondary}", FAIL

NOT_ACCESSIBLE = "The {primary} is not accessible", FAIL
ALREADY_IN_ROOM = "Already in {primary}", FAIL
NOT_ACCESSIBLE_FROM_CURRENT_ROOM = "The {primary} is not accessible from the {secondary}", FAIL
BLOCKED_CONNECTION = "The {primary} is blocked", FAIL
BLOCKED_OBJECT_LOCKED = "The {primary} is locked and must be unlocked first", FAIL
BLOCKED_OBJECT_CLOSED = "The {primary} is closed and must be opened first", FAIL

NOT_ENTERABLE = "The {primary} is not an object you can enter into.", FAIL
ALREADY_ENTERED = "Already entered into the {primary}.", FAIL
NOT_IN_OBJECT = "You're not into a {primary}.", FAIL
MUST_EXIT_ENTERABLE_FIRST = "You must exit from the {primary} first.", FAIL

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
NOT_FITTING_KEY = "The {secondary} doesn't fit in the {primary}.", FAIL

NOT_OPENABLE = "The {primary} can't be opened", FAIL
ALREADY_OPEN = "The {primary} is already open", FAIL

NOT_CLOSABLE = "The {primary} can't be closed", FAIL
ALREADY_CLOSED = "The {primary} is already closed", FAIL

MUST_CLOSE_OBJECT = "The {primary} is open and must be closed first", FAIL

NOT_ANIMATE = "You can't do that to a lifeless object.", FAIL
NOT_ASLEEP = "The {primary} isn't sleeping", FAIL

# Neutral outcomes
NOTHING_HAPPENS = "Nothing happens", NEUTRAL
NO_MESSAGE = False, NEUTRAL  # False because we don't want to print a description.
WAIT = "You choose to wait for something to happen.", NEUTRAL

# Successful outcomes
ACCESS_SUCCESS = "You accessed the {primary}.", SUCCESS
ENTER_SUCCESS = "You entered into the {primary}.", SUCCESS
EXIT_SUCCESS = "You got out of the {primary}.", SUCCESS
LOCK_SUCCESS = "You locked the {primary} using the {secondary}", SUCCESS
UNLOCK_SUCCESS = "You unlocked the {primary} using the {secondary}", SUCCESS
TAKE_SUCCESS = "You took the {primary}.", SUCCESS
TAKE_FROM_OWNER_SUCCESS = "You took the {primary} from the {secondary}.", SUCCESS
DROP_SUCCESS = "You dropped the {primary}.", SUCCESS
OPEN_SUCCESS = "You opened the {primary}.", SUCCESS
CLOSE_SUCCESS = "You closed the {primary}.", SUCCESS
THROW_SUCCESS = "You threw the {primary} at the {secondary}.", SUCCESS
THROW_AT_TARGET_SUCCESS = "You threw the {secondary} at the {primary}.", SUCCESS
