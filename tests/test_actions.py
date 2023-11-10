from unittest import TestCase

from game.outcomes import *
from game.world import World
from game.actions import Action
from game.commands import Command
from game.items import *


class TestAction(TestCase):

    def assert_outcome(self, expected_outcome, expected_outcome_objects=None):
        # Initialization
        if expected_outcome_objects is None:
            expected_outcome_objects = []
        commands = list(self.commands) if isinstance(self.commands, tuple) else [self.commands]
        world = World(test=True)
        world.populate()
        actual_outcome = None
        actual_outcome_objects = []

        # Get the actual result
        for cmd in commands:
            actual_result = world.parse(cmd)
            actual_outcome = actual_result.outcome
            actual_outcome_objects = [f"{obj}" for obj in actual_outcome.objects]

        # Compare with the expected result
        self.assertEqual(expected_outcome, actual_outcome.outcome)
        self.assertEqual(expected_outcome_objects, actual_outcome_objects)


class TestOutcome(TestCase):
    def test_outcome(self):
        world = World()
        world.populate()
        command = Command('open', ['door', 'lockpick'])

        door = world.get_object_by_name('door')
        lockpick = world.get_object_by_name('lockpick')
        other = world.get_object_by_name('barel')
        other2 = world.get_object_by_name('stone')
        action = Action(world, command, door, lockpick)
        outcome_const = OPEN_WITH_TOOL_SUCCESS

        # Test door, lockpick
        actual_outcome = action.outcome(outcome_const, door, lockpick).object_names
        expected_outcome = Outcome(outcome_const, door, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test lockpick, door
        actual_outcome = action.outcome(outcome_const, lockpick, door).object_names
        expected_outcome = Outcome(outcome_const, door, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test door
        actual_outcome = action.outcome(outcome_const, door).object_names
        expected_outcome = Outcome(outcome_const, door).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test lockpick
        actual_outcome = action.outcome(outcome_const, lockpick).object_names
        expected_outcome = Outcome(outcome_const, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other
        actual_outcome = action.outcome(outcome_const, other).object_names
        expected_outcome = Outcome(outcome_const, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test door, other
        actual_outcome = action.outcome(outcome_const, door, other).object_names
        expected_outcome = Outcome(outcome_const, door, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other, door
        actual_outcome = action.outcome(outcome_const, other, door).object_names
        expected_outcome = Outcome(outcome_const, door, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test lockpick, other
        actual_outcome = action.outcome(outcome_const, lockpick, other).object_names
        expected_outcome = Outcome(outcome_const, lockpick, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other, lockpick
        actual_outcome = action.outcome(outcome_const, other, lockpick).object_names
        expected_outcome = Outcome(outcome_const, other, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other, other2
        actual_outcome = action.outcome(outcome_const, other, other2).object_names
        expected_outcome = Outcome(outcome_const, other, other2).object_names
        self.assertEqual(expected_outcome, actual_outcome)


class TestExecute(TestAction):
    def test_invalid(self):
        self.commands = "take invalid"
        self.assert_outcome(INVALID_OBJECTS, ['invalid'])

    def test_out_of_scope(self):
        self.commands = "take barel"
        self.assert_outcome(OUT_OF_SCOPE, ['barel'])

    def test_command_transform(self):
        self.commands = "take lockpick", "use lockpick lock"
        self.assert_outcome(COMMAND_TRANSFORMED, ['lockpick', 'lock'])


class TextExamine(TestAction):
    def test_examine(self):
        self.commands = "examine"
        self.assert_outcome(EXAMINE_SUCCESS, ['cell'])

    def test_examine_current_room(self):
        self.commands = "examine cell"
        self.assert_outcome(EXAMINE_SUCCESS, ['cell'])

    def test_examine_another_room(self):
        self.commands = "examine dungeon"
        self.assert_outcome(CANT_EXAMINE_FROM_CURRENT_ROOM, ['dungeon'])

    def test_examine_object(self):
        self.commands = "examine key"
        self.assert_outcome(EXAMINE_SUCCESS, ['key'])


class TestTake(TestAction):
    def test_invalid(self):
        self.commands = "take"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_obtainable(self):
        self.commands = "take lockpick"
        self.assert_outcome(TAKE_SUCCESS, ['lockpick'])

    def test_non_obtainable(self):
        self.commands = "take lock"
        self.assert_outcome(NOT_OBTAINABLE, ['lock'])

    def test_already_obtained(self):
        self.commands = "take lockpick", "take lockpick"
        self.assert_outcome(ALREADY_OBTAINED, ['lockpick'])


class TestDrop(TestAction):
    def test_invalid(self):
        self.commands = "drop"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_dropable(self):
        self.commands = "take lockpick", "drop lockpick"
        self.assert_outcome(DROP_SUCCESS, ['lockpick'])

    def test_non_in_possession(self):
        self.commands = "drop lockpick"
        self.assert_outcome(NOT_IN_POSSESSION, ['lockpick'])


class TestUse(TestAction):
    def test_invalid(self):
        self.commands = "use"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_usable_on_target(self):
        pass

    def test_not_usable(self):
        self.commands = "use lock"
        self.assert_outcome(NOT_USABLE, ['lock'])

    def test_not_owned(self):
        self.commands = "use lockpick"
        self.assert_outcome(NOT_HELD, ['lockpick'])


class TestLock(TestAction):
    def test_invalid(self):
        self.commands = "lock"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_with_lockpick(self):
        self.commands = "take lockpick", "unlock lock", "lock lock lockpick"
        self.assert_outcome(CANT_LOCK_WITH_OBJECT, ['lockpick'])

    def test_with_key(self):
        self.commands = "take key", "unlock lock key", "lock lock key"
        self.assert_outcome(LOCK_SUCCESS, ['lock', 'key'])

    def test_with_lockpick_in_inventory(self):
        self.commands = "take lockpick", "unlock lock", "lock lock"
        self.assert_outcome(CANT_LOCK_WITH_OBJECT, ['lockpick'])

    def test_with_key_in_inventory(self):
        self.commands = "take key", "unlock lock", "lock lock"
        self.assert_outcome(LOCK_SUCCESS, ['lock', 'key'])

    def test_locking_tool_cant_lock(self):
        self.commands = "take lockpick", "unlock lock", "lock lock lockpick"
        self.assert_outcome(CANT_LOCK_WITH_OBJECT, ['lockpick'])

    def test_locking_tool_not_in_possession(self):
        self.commands = "take key", "unlock door", "lock lock lockpick"
        self.assert_outcome(NOT_IN_POSSESSION, ['lockpick'])

    def test_missing_locking_tool(self):
        self.commands = "take key", "unlock lock", "drop key", "lock lock"
        self.assert_outcome(MISSING_LOCKING_TOOL, [])

    def test_not_a_locking_tool(self):
        self.commands = "take stone", "take key", "unlock lock", "lock lock stone"
        self.assert_outcome(NOT_A_LOCKING_TOOL, ['stone'])

    def test_already_locked(self):
        self.commands = "take key", "lock lock key"
        self.assert_outcome(ALREADY_LOCKED, ['lock'])

    def test_not_lockable(self):
        self.commands = "take lockpick", "lock stone lockpick"
        self.assert_outcome(NOT_LOCKABLE, ['stone'])


class TestUnlock(TestAction):
    def test_invalid(self):
        self.commands = "unlock"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_with_lockpick(self):
        self.commands = "take lockpick", "unlock lock lockpick"
        self.assert_outcome(UNLOCK_SUCCESS, ['lock', 'lockpick'])

    def test_with_key(self):
        self.commands = "take key", "unlock lock key"
        self.assert_outcome(UNLOCK_SUCCESS, ['lock', 'key'])

    def test_with_lockpick_in_inventory(self):
        self.commands = "take lockpick", "unlock lock"
        self.assert_outcome(UNLOCK_SUCCESS, ['lock', 'lockpick'])

    def test_with_key_in_inventory(self):
        self.commands = "take key", "unlock lock"
        self.assert_outcome(UNLOCK_SUCCESS, ['lock', 'key'])

    def test_unlocking_tool_not_in_possession(self):
        self.commands = "unlock lock lockpick"
        self.assert_outcome(NOT_IN_POSSESSION, ['lockpick'])

    def test_missing_unlocking_tool(self):
        self.commands = "unlock lock"
        self.assert_outcome(MISSING_UNLOCKING_TOOL, [])

    def test_not_an_unlocking_tool(self):
        self.commands = "take stone", "unlock lock stone"
        self.assert_outcome(NOT_AN_UNLOCKING_TOOL, ['stone'])

    def test_not_lockable(self):
        self.commands = "take lockpick", "unlock stone lockpick"
        self.assert_outcome(NOT_LOCKABLE, ['stone'])


class TestOpen(TestAction):
    def test_invalid(self):
        self.commands = "open"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_open(self):
        self.commands = "take lockpick", "unlock door", "open door"
        self.assert_outcome(OPEN_SUCCESS, ['door'])

    def test_open_locked(self):
        self.commands = "take lockpick", "open door"
        self.assert_outcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_open_locked_with_opening_tool(self):
        self.commands = "take lockpick", "open door lockpick"
        self.assert_outcome(OPEN_WITH_TOOL_SUCCESS, ['door', 'lockpick'])

    def test_already_open(self):
        self.commands = "take lockpick", "open door lockpick", "open door"
        self.assert_outcome(ALREADY_OPEN, ['door'])

    def test_not_openable(self):
        self.commands = "open stone"
        self.assert_outcome(NOT_OPENABLE, ['stone'])


class TestClose(TestAction):
    def test_invalid(self):
        self.commands = "close"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_close(self):
        self.commands = "take lockpick", "open door lockpick", "close door"
        self.assert_outcome(CLOSE_SUCCESS, ['door'])

    def test_already_closed(self):
        self.commands = "close door"
        self.assert_outcome(ALREADY_CLOSED, ['door'])

    def test_not_closable(self):
        self.commands = "close stone"
        self.assert_outcome(NOT_CLOSABLE, ['stone'])


class TestGo(TestAction):
    def test_invalid(self):
        self.commands = "go"
        self.assert_outcome(INVALID_COMMAND, [])

    def test_go(self):
        self.commands = "take lockpick", "open door lockpick", "go dungeon"
        self.assert_outcome(ACCESS_ROOM_SUCCESS, ['dungeon'])

    def test_connection_blocked(self):
        self.commands = "go dungeon"
        self.assert_outcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_not_connection_to_current_room(self):
        self.commands = "go courtyard"
        self.assert_outcome(NOT_ACCESSIBLE_FROM_CURRENT_ROOM, ['courtyard'])

    def test_already_in_room(self):
        self.commands = "go cell"
        self.assert_outcome(ALREADY_IN_ROOM, ['cell'])

    def test_not_accessible(self):
        self.commands = "go stone"
        self.assert_outcome(NOT_ACCESSIBLE, ['stone'])


class TestExit(TestAction):
    def test_exit(self):
        self.commands = "take key", "unlock door", "exit"
        self.assert_outcome(COMMAND_TRANSFORMED)

    def test_current_room(self):
        self.commands = "take key", "unlock door", "exit the cell"
        self.assert_outcome(COMMAND_TRANSFORMED)

    def test_specified_exit(self):
        self.commands = "take key", "unlock door", "exit from the door"
        self.assert_outcome(COMMAND_TRANSFORMED)

    def test_current_room_using_specified_exit(self):
        self.commands = "take key", "unlock door", "exit the cell from the door"
        self.assert_outcome(COMMAND_TRANSFORMED)

    def test_multiple_exits(self):
        self.commands = "take lockpick", "open door lockpick", "go dungeon", "exit dungeon"
        self.assert_outcome(UNSPECIFIED_EXIT, [])

    def test_another_room(self):
        self.commands = "exit the dungeon"
        self.assert_outcome(NOT_IN_LOCATION, ['dungeon'])


class TestLockingTool(TestAction):
    def test_use_usable_alone(self):
        self.commands = "take lockpick", "use lockpick"
        self.assert_outcome(CANT_USE_OBJECT_ALONE, ["lockpick"])

    def test_use_on_not_lockable(self):
        self.commands = "take lockpick", "use lockpick stone"
        self.assert_outcome(CANT_USE_OBJECT_ON_TARGET, ['lockpick', 'stone'])


class TestDoor(TestAction):
    def test_blocked_locked(self):
        self.commands = "go dungeon"
        self.assert_outcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_blocked_closed(self):
        self.commands = "take lockpick", "unlock door", "go dungeon"
        self.assert_outcome(BLOCKED_OBJECT_CLOSED, ['door'])

    def test_open_locked(self):
        self.commands = "open door"
        self.assert_outcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_open_locked_with_tool(self):
        self.commands = "take lockpick", "open door lockpick"
        self.assert_outcome(OPEN_WITH_TOOL_SUCCESS, ['door', 'lockpick'])

    def test_lock_open(self):
        self.commands = "take key", "open door key", "lock door"
        self.assert_outcome(MUST_CLOSE_OBJECT, ['door', 'key'])
