# result types
SUCCESS = "SUCCESS"  # command executed successfully and the result advances the game state
NEUTRAL = "NEUTRAL"  # command executed successfully but the result does not advance the game state
FAIL = "FAIL"  # command is valid but failed to be executed
INVALID = "ERROR"  # invalid command

# outcomes
# invalid outcomes
INVALID_COMMAND = f"Invalid command", INVALID
INVALID_OBJECT = f"Invalid object", INVALID
# INVALID_OBJECT_DETAILED = f"Invalid object: {object_to_use}", INVALID
INVALID_ITEMS = f"Invalid item(s)", INVALID
# INVALID_ITEM_DETAILED = f"Invalid item(s): {', '.join(invalid_items)}", INVALID
INVALID_LOCATION = f"Invalid location", INVALID
# INVALID_LOCATION_DETAILED = f"Invalid location: {location_to_go}", INVALID

# fail generic outcomes
CANT_USE_OBJECT = f"Can't use that", FAIL
# CANT_USE_OBJECT_DETAILED = f"Can't use {object_to_use}", FAIL
MUST_BE_COMBINED = f"Must combine that with something else", FAIL
# MUST_BE_COMBINED_DETAILED = f"Must combine {items_to_combine[0]} with something else", FAIL
CANT_COMBINE = f"Can't combine these", FAIL
# CANT_COMBINE_DETAILED = f"Can't combine {item1} and {item2}", FAIL
CANT_GO_TO_LOCATION = f"Can't go to that location", FAIL
# CANT_GO_TO_LOCATION_DETAILED = f"Can't go to {location_to_go}", FAIL
ALREADY_IN_LOCATION = f"Already in this location", FAIL
# ALREADY_IN_LOCATION_DETAILED = f"Already in {new_location}", FAIL
CANT_ACCESS_FROM_HERE = f"Can't access that from your current location", FAIL
# CANT_ACCESS_FROM_HERE_DETAILED = f"Can't access {new_location} from {current_location}", FAIL
BLOCKED_LOCATION = f"Location is blocked", FAIL
# BLOCKED_LOCATION_DETAILED = f"{self} is blocked", FAIL

# successful generic outcomes
ACCESSED_LOCATION = f"Accessed the location", SUCCESS
# ACCESSED_LOCATION_DETAILED = f"Accessed the {new_location}", SUCCESS

# object specific outcomes
# lockpick
LOCK_LOCKPICK_SUCCESS = "lock unlocked with lockpick", SUCCESS
LOCK_LOCKPICK_FAIL = "lock already unlocked"

# door
DOOR_OPENED_SUCCESS = f"You opened the door"
# OPENED_SUCCESS = f"You opened the {self}"
DOOR_CLOSED_SUCCESS = f"You opened the door"
# CLOSED_SUCCESS = f"You closed the {self}"
DOOR_LOCKED_FAIL = f"The door is locked", FAIL
# LOCKED_FAIL = f"The {self} is locked", FAIL
DOOR_CLOSED_FAIL = f"The door is closed", FAIL
# CLOSED_FAIL = f"The {self} is closed", FAIL
