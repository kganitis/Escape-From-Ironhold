import random


class Outcome:
    def __init__(self, outcome, verb=None, primary_object=None, secondary_object=None):
        self.outcome = outcome
        self.verb = verb
        self.primary_object = primary_object
        self.secondary_object = secondary_object

    def __str__(self):
        return f"{self.description}, {self.object_names}, {self.type}"

    def __eq__(self, other):
        return self.outcome == other.outcome and self.objects == other.objects

    @property
    def description(self):
        desc = self.outcome[0]
        if not desc:
            return False
        if not isinstance(desc, str):
            desc = desc[random.randint(0, len(desc)-1)]
        return desc

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
            secondary=self.secondary_object,
            verb=self.verb,
            room=self.primary_object.current_room if self.primary_object else None
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
INVALID_COMMAND = [
    "That doesn't make sense.",
    "That's not possible.",
    "Can't do that.",
    "Nope, that's not an option.",
    "Try something else.",
    "That doesn't work.",
    "Sorry, that won't work.",
    "Not a valid choice."
], INVALID

INVALID_OBJECTS = [
    "I've only understood you as far as wanting to {verb}."
    "Hmm, that's not ringing any bells. Give me more context.",
    "I don't understand what you are referring to.",
    "I'm not familiar with that. Could you clarify?",
    "I didn't get that. Can you try using different words?",
], INVALID

# Scope outcomes
OUT_OF_SCOPE = [
    "I don't see any {primary} around to {verb}.",
    "There doesn't seem to be a {primary} in sight to {verb}.",
    "You scan the {room}, but there's no sign of a {primary} to {verb}."
], FAIL

# Examine
CANT_EXAMINE_FROM_CURRENT_ROOM = [
    "Are you sure you're in the {primary}?",
    "This isn't the {primary}. You're in a different place altogether.",
    "You're in a different place. This isn't the {primary}."
], FAIL

# Take
NOT_OBTAINABLE = [
    "The {primary} is not something you can {verb}.",
    "The {primary} is not obtainable.",
    "You can't get your hands on the {primary}."
], FAIL

ALREADY_OBTAINED = [
    "You already have the {primary}.",
    "You possess the {primary} already.",
    "The {primary} is already in your possession.",
    "The {primary} is already part of your inventory."
], FAIL

NOT_OWNED_BY_OBJECT = [
    "The {secondary} doesn't have any {primary}.",
    "You search the {secondary} but find no {primary}.",
    "No {primary} foung in the {secondary}.",
    "You check the {secondary}, but there's no sign of {primary}."
], FAIL

# Drop
NOT_IN_POSSESSION = [
    "You don't have any {primary} with you.",
    "No {primary} can be found in your possession.",
    "The {primary} is nowhere to be seen in your belongings.",
    "You're currently lacking any {primary} in your inventory."
], FAIL

# Use
NOT_USABLE = [
    "You can't do anything with the {primary}.",
    "The {primary} isn't something you can use.",
    "Trying to use the {primary} leads to nothing.",
    "No luck with the {primary} – it's not usable in this context.",
    "Using the {primary} isn't possible in this context."
], FAIL

CANT_USE_OBJECT_ALONE = [
    "You must use the {primary} with something else.",
    "Using the {primary} alone won't do much.",
    "Hmm, try combining the {primary} with another object.",
    "To make progress, consider using the {primary} differently.",
    "Using the {primary} in isolation won't achieve anything.",
    "Explore other options by using the {primary} along with something.",
    "Think about how the {primary} can be used with other objects.",
    "Using the {primary} like that won't yield results. Try including something else in addition.",
    "You might need to use the {primary} with another object."
], FAIL

MUST_USE_OBJECT_ALONE = [
    "You must use the {primary} alone.",
    "Simplicity is the key. Use the {primary} alone.",
    "Just the {primary} will do for this task.",
    "Stick to using the {primary} by itself.",
    "Don't overcomplicate it. Try the {primary} alone."
], FAIL

CANT_USE_OBJECT_ON_TARGET = [
    "You can't use the {primary} on the {secondary}.",
    "Using the {primary} on the {secondary} won't work.",
    "It's not possible to use the {primary} on the {secondary}.",
    "The {primary} is ineffective when used on the {secondary}.",
    "No matter how hard you try, the {primary} won't work on the {secondary}.",
    "Using the {primary} on the {secondary} doesn't achieve anything.",
    "You consider using the {primary} on the {secondary}, but it's not the right approach.",
    "The {primary} has no effect on the {secondary}."
], FAIL

NOT_ACCESSIBLE = [
    "The {primary} is not something you can {verb}.",
    "You're unable to interact with the {primary} this way.",
    "You can't do that with the {primary}."
], FAIL

ALREADY_IN_ROOM = [
    "No need, you're already in the {primary}.",
    "You're already located in the {primary}.",
    "You're in the {primary} already."
], FAIL

NOT_ACCESSIBLE_FROM_CURRENT_ROOM = [
    "The {primary} is not accessible from the {secondary}.",
    "You can't reach the {primary} from the {secondary}.",
    "Accessing the {primary} from the {secondary} is not possible.",
    "No way to get to the {primary} from the {secondary}.",
    "The {secondary} doesn't provide access to the {primary}.",
    "You're unable to reach the {primary} through the {secondary}.",
    "No access to the {primary} is available via the {secondary}."
], FAIL

BLOCKED_CONNECTION = [
    "The {primary} is blocked.",
    "The access through the {primary} is blocked.",
    "The path through the {primary} is blocked."
], FAIL

BLOCKED_OBJECT_LOCKED = [
    "The {primary} is locked and must be unlocked first.",
    "You can't proceed with the locked {primary}. Unlock it first.",
    "Unlock the {primary} before attempting anything else.",
    "The {primary} is firmly locked. Find a way to unlock it.",
    "You need to unlock the {primary} first before continuing.",
    "The {primary} is secured and won't budge until unlocked.",
    "Unlock the {primary} to proceed in your adventure.",
    "The locked {primary} stands in your way. Unlock it to move forward.",
    "The {primary} is locked tight. You'll need to unlock it somehow."
], FAIL

BLOCKED_OBJECT_CLOSED = [
    "The {primary} is closed and must be opened first.",
    "Opening the {primary} should be your first step.",
    "Can't do that yet, the {primary} is closed.",
    "Opening the {primary} is necessary before proceeding.",
    "Make sure the {primary} is open before attempting that.",
    "The closed {primary} is preventing further action. Open it first.",
    "Ensure the {primary} is open before proceeding."
], FAIL

NOT_ENTERABLE = responses = [
    "The {primary} is not something you can {verb}.",
    "Entering the {primary} isn't allowed.",
    "The {primary} doesn't allow entry."
], FAIL

ALREADY_ENTERED = [
    "Already entered into the {primary}.",
    "You're already inside the {primary}.",
    "You're already in the {primary}."
], FAIL

NOT_IN_OBJECT = [
    "You're not inside a {primary}.",
    "You're not currently situated within a {primary}."
], FAIL

MUST_EXIT_ENTERABLE_FIRST = [
    "You must exit from the {primary} first.",
    "Exiting requires leaving the {primary} first.",
    "To exit, you need to depart from the {primary} initially.",
    "First, make your way out of the {primary}.",
    "Ensure you've left the {primary} before attempting to exit.",
    "Exiting requires being outside the {primary}."
], FAIL

NOT_IN_LOCATION = [
    "You're not in the {primary} right now.",
    "The {primary} is not your current location.",
    "You're not standing in the {primary} at the moment."
], FAIL

NOT_LOCKABLE = [
    "The {primary} is not something you can (un)lock",
    "The {primary} doesn't respond to your attempt to (un)lock.",
    "Attempting to (un)lock the {primary} proves futile."
], FAIL

ALREADY_LOCKED = [
    "The {primary} is already locked.",
    "It seems you missed it, but the {primary} is already locked.",
    "No luck. The {primary} is already locked.",
    "The {primary} seems to be locked, just as before.",
    "You double-check, but the {primary} is definitely locked."
], FAIL

ALREADY_UNLOCKED = [
    "The {primary} is already unlocked.",
    "You've already unlocked the {primary}.",
    "It seems you've unlocked the {primary} before.",
    "The {primary} was unlocked earlier.",
    "No need to unlock it again, the {primary} is already open."
], FAIL

NOT_A_LOCKING_TOOL = [
    "Nope, the {primary} isn't suitable for locking.",
    "You attempt to use the {primary} for locking, but it's not the right tool.",
    "Trying to lock something with the {primary} won't work.",
    "The {primary} isn't designed for locking things.",
    "Locking with the {primary}? Not a great idea.",
    "You consider using the {primary} for locking, but it's not the right fit.",
    "Using the {primary} for locking? That won't do the trick.",
    "You give it a shot, but the {primary} isn't the right tool for locking.",
    "Locking requires something other than the {primary}.",
    "Nice try, but the {primary} won't work for locking purposes."
], FAIL

NOT_AN_UNLOCKING_TOOL = [
    "The {primary} doesn't seem suitable for unlocking.",
    "Unlocking with the {primary} is not an option.",
    "You can't use the {primary} to unlock anything.",
    "Trying to unlock with the {primary} won't work.",
    "The {primary} isn't designed for unlocking tasks.",
    "Unlocking using the {primary} is not feasible.",
    "The {primary} isn't the right tool for unlocking.",
    "Using the {primary} to unlock won't yield any results."
], FAIL

MISSING_LOCKING_TOOL = [
    "You require an item with locking capabilities.",
    "You need a tool that can perform locking.",
    "Find something capable of locking to proceed.",
    "Search for an object that can be used to lock.",
    "You're missing an item with the ability to lock.",
    "Look for a suitable locking device or tool.",
    "You lack the necessary means to lock right now.",
    "Locate an item designed for locking purposes."
], FAIL

MISSING_UNLOCKING_TOOL = [
    "You need a tool for unlocking.",
    "You require something that can unlock.",
    "You're missing the right unlocking tool.",
    "You need an item capable of unlocking.",
    "Find a suitable unlocking device.",
    "You lack the means to unlock.",
    "Search for a tool to unlock with.",
    "You're missing the necessary unlocking tool."
], FAIL

CANT_LOCK_WITH_OBJECT = [
    "The {primary} isn't suitable for locking.",
    "Locking with the {primary} is not an option.",
    "You can't use the {primary} for locking purposes.",
    "Locking using the {primary} won't work.",
    "The {primary} is not designed for locking.",
    "Using the {primary} to lock is not feasible.",
    "Locking with the {primary} is beyond its capabilities.",
    "You can't lock anything with the {primary}.",
    "Locking isn't possible with the {primary}."
], FAIL

CANT_UNLOCK_WITH_OBJECT = [
    "The {primary} doesn't unlock anything.",
    "Using the {primary} for unlocking is not an option.",
    "You attempt to unlock with the {primary}, but it's ineffective.",
    "Unlocking with the {primary} is not a valid choice.",
    "The {primary} isn't the right tool for unlocking.",
    "No luck! The {primary} can't be used for unlocking.",
    "Using the {primary} won't get you anywhere in unlocking.",
    "You realize the {primary} is not suited for unlocking.",
    "Unlocking with the {primary} is a dead end.",
    "The {primary} proves useless for unlocking."
], FAIL

NOT_FITTING_KEY = [
    "The {secondary} doesn't fit in the {primary}.",
    "Trying to put the {secondary} into the {primary} proves futile.",
    "No matter how you try, the {secondary} won't go into the {primary}.",
    "You attempt to insert the {secondary} into the {primary}, but it just doesn't fit.",
    "You can't force the {secondary} into the {primary} - they simply don't go together."
], FAIL

NOT_OPENABLE = [
    "The {primary} is not something that can be opened.",
    "Opening the {primary} is not possible.",
    "Opening the {primary} is not a valid action.",
    "You discover that the {primary} is not meant to be opened.",
    "The {primary} doesn't have an opening mechanism."
], FAIL

ALREADY_OPEN = [
    "The {primary} is already open.",
    "It seems the {primary} is open already.",
    "The {primary} was already open to begin with.",
    "You see that the {primary} is already open."
], FAIL

NOT_CLOSABLE = [
    "The {primary} is not something that can be closed.",
    "Closing the {primary} is not possible.",
    "Closing the {primary} is not a valid action.",
    "You discover that the {primary} is not meant to be closed.",
    "The {primary} doesn't have a closure mechanism."
], FAIL

ALREADY_CLOSED = [
    "The {primary} is already closed.",
    "It looks like the {primary} is closed.",
    "You find that the {primary} is already shut.",
    "The {primary} won't budge; it's closed.",
    "No need to worry about the {primary} – it's closed."
], FAIL

MUST_CLOSE_OBJECT = [
    "The {primary} is open and must be closed first.",
    "You need to close the {primary} before trying to {verb}.",
    "Closing the {primary} is necessary before attempting to {verb}.",
    "Can't {verb} until you close the {primary}.",
    "Ensure the {primary} is closed before trying to {verb}.",
    "Closing the {primary} should be your first step before attempting to {verb}.",
    "You find the {primary} open; close it before trying to {verb}.",
    "Make sure the {primary} is closed before attempting to {verb}."
], FAIL

NOT_ANIMATE = [
    "You can't do that to a lifeless object.",
    "You attempt to interact with the {primary}, but it's lifeless and unresponsive.",
    "Your efforts to involve the {primary} prove futile; it's devoid of life.",
    "It seems the {primary} is immune to your attempts—it lacks the spark of life.",
    "Interacting with the lifeless {primary} yields no results.",
    "Lifeless and unanimated, the {primary} shows no response to your actions.",
    "Your actions have no effect on the lifeless state of the {primary}."
], FAIL

NOT_ASLEEP = [
    "The {primary} isn't sleeping.",
    "You don't find the {primary} sleeping.",
    "The {primary} is wide awake.",
    "The {primary} is not catching any Z's."
], FAIL

# Neutral outcomes
NO_MESSAGE = False, NEUTRAL  # False because we don't want to print a description.

WAIT = [
    "You decide to wait patiently.",
    "You opt for waiting and see what unfolds.",
    "Waiting is your chosen course of action.",
    "You settle in for a moment of anticipation.",
    "You decide to bide your time and see what transpires.",
    "Patience is your current strategy; you wait for developments.",
    "You choose to wait and observe the surroundings.",
    "You take a moment to wait and see what happens next.",
    "You decide to take your time to think.",
    "It's a good idea to wait once in a while.",
], NEUTRAL

# Successful outcomes
ACCESS_SUCCESS = [
    "You {verb} the {primary}.",
    "You find yourself in the {primary}.",
    "You are now in the {primary}."
], SUCCESS

ENTER_SUCCESS = [
    "You enter into the {primary}.",
    "You're now inside the {primary}.",
    "You hide into the {primary}"
], SUCCESS

EXIT_SUCCESS = [
    "You successfully get out of the {primary}.",
    "Exiting the {primary} successfully.",
    "You're out of the {primary} now.",
    "You exit the {primary} without a problem.",
    "You're no longer in the {primary}."
], SUCCESS

LOCK_SUCCESS = [
    "You locked the {primary} using the {secondary}.",
    "Locking the {primary} with the {secondary} was successful.",
    "You successfully locked the {primary} by using the {secondary}.",
    "The {primary} is locked, and you've got the {secondary} to thank for it."
], SUCCESS

UNLOCK_SUCCESS = [
    "You unlocked the {primary} using the {secondary}.",
    "Using the {secondary}, you successfully unlocked the {primary}.",
    "With the {secondary} in hand, you opened the {primary}.",
    "The {secondary} did the trick, unlocking the {primary}.",
    "Unlocking the {primary} was a breeze with the {secondary}.",
    "You used the {secondary} to unlock the {primary}.",
    "The {primary} yielded to the {secondary}'s influence and unlocked.",
    "With a twist of the {secondary}, the {primary} opened up.",
    "Successfully unlocked the {primary} by employing the {secondary}.",
    "Unlocking the {primary} was as simple as using the {secondary}.",
    "The {primary} gave way to the {secondary}'s unlocking power.",
    "Using the {secondary}, you unlocked the {primary} without a hitch.",
    "The {primary} succumbed to the unlocking force of the {secondary}.",
    "You successfully unlocked the {primary} with the {secondary}."
], SUCCESS

TAKE_SUCCESS = [
    'The {primary} is now yours. Maybe you can find a use for it.',
    'You {verb} the {primary} successfully.',
    "You {verb} the {primary} and add it to your inventory.",
    "You now have the {primary} in your possession."
]

TAKE_FROM_OWNER_SUCCESS = [
    "You {verb} the {primary} from the {secondary} successfully.",
    "You successfully {verb} the {primary} from the {secondary}.",
    "The {primary} is now in your possession, taken from the {secondary}.",
    "You manage to {verb} the {primary} from the {secondary}.",
    "You {verb} the {primary} from the {secondary} without a hitch."
], SUCCESS

DROP_SUCCESS = [
    "You successfully {verb} the {primary}.",
    "You {verb} the {primary}, removing it from your inventory.",
    "You {verb} the {primary}, leaving it behind."
], SUCCESS

OPEN_SUCCESS = [
    "You successfully open the {primary}.",
    "With ease, you open the {primary}.",
    "The {primary} opens without any issues."
], SUCCESS

CLOSE_SUCCESS = [
    "You successfully close the {primary}.",
    "The {primary} is now closed.",
    "Closing the {primary} was a success.",
    "You've closed the {primary} without any issues.",
    "The {primary} is now shut tight.",
    "Successfully closed the {primary}.",
    "You close the {primary} with ease.",
    "Closing the {primary} is done successfully."
], SUCCESS

THROW_SUCCESS = [
    "You successfully throw the {primary} at the {secondary}.",
    "With precision, you throw the {primary} at the {secondary}.",
    "The {primary} soars through the air and hits the {secondary}.",
    "You aim true, hitting the {secondary} with the {primary}.",
    "The {primary} finds its mark, striking the {secondary}.",
    "Effortlessly, you throw the {primary} and hit the {secondary}.",
    "A well-aimed throw hits the {primary} with the {secondary}.",
    "You skillfully hurl the {primary}, striking the {secondary}."
], SUCCESS

THROW_AT_TARGET_SUCCESS = [
    "You successfully throw the {secondary} at the {primary}.",
    "With precision, you throw the {secondary} at the {primary}.",
    "The {secondary} sails through the air and hits the {primary}.",
    "You launch the {secondary} towards the {primary} with accuracy.",
    "Aiming carefully, you throw the {secondary} at the {primary}.",
    "The {secondary} finds its mark as it hits the {primary}.",
    "You execute a successful throw, hitting the {primary} with the {secondary}.",
    "With a swift motion, the {secondary} is thrown and strikes the {primary}.",
    "You skillfully hurl the {secondary} at the {primary}."
], SUCCESS
