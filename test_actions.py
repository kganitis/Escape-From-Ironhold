from unittest import TestCase

from world import World
from actions import Action
from commands import Command
from items import *
from guard import *


class TestAction(TestCase):
    def setUp(self):
        self.commands = (None,)
        self.world = World(test=True)
        self.world.populate()

    def get(self, name):
        return self.world.get(name)

    def execute_commands(self):
        commands = list(self.commands) if isinstance(self.commands, tuple) else [self.commands]
        result = None
        for cmd in commands:
            result = self.world.parse(cmd)
        return result

    def assertOutcome(self, expected_outcome, expected_outcome_objects=None):
        if expected_outcome_objects is None:
            expected_outcome_objects = []

        # Get the actual result
        actual_result = self.execute_commands()
        actual = actual_result.outcome

        # Always assert if the outcome is a tuple
        self.assertIsInstance(actual.outcome, tuple)

        # Compare with the expected result
        self.assertEqual(expected_outcome, actual.outcome)
        self.assertEqual(expected_outcome_objects, actual.object_names)


class TestOutcome(TestCase):
    def test_outcome(self):
        world = World()
        world.populate()
        command = Command('open', ['door', 'lockpick'])

        door = world.get('door')
        lockpick = world.get('lockpick')
        other = world.get('barrel')
        other2 = world.get('stone')
        action = Action(world, command, door, lockpick)
        outcome_const = OPEN_SUCCESS

        # Test door, lockpick
        actual_outcome = action.create_outcome(outcome_const, door, lockpick).object_names
        expected_outcome = Outcome(outcome_const, door, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test lockpick, door
        actual_outcome = action.create_outcome(outcome_const, lockpick, door).object_names
        expected_outcome = Outcome(outcome_const, door, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test door
        actual_outcome = action.create_outcome(outcome_const, door).object_names
        expected_outcome = Outcome(outcome_const, door).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test lockpick
        actual_outcome = action.create_outcome(outcome_const, lockpick).object_names
        expected_outcome = Outcome(outcome_const, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other
        actual_outcome = action.create_outcome(outcome_const, other).object_names
        expected_outcome = Outcome(outcome_const, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test door, other
        actual_outcome = action.create_outcome(outcome_const, door, other).object_names
        expected_outcome = Outcome(outcome_const, door, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other, door
        actual_outcome = action.create_outcome(outcome_const, other, door).object_names
        expected_outcome = Outcome(outcome_const, door, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test lockpick, other
        actual_outcome = action.create_outcome(outcome_const, lockpick, other).object_names
        expected_outcome = Outcome(outcome_const, lockpick, other).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other, lockpick
        actual_outcome = action.create_outcome(outcome_const, other, lockpick).object_names
        expected_outcome = Outcome(outcome_const, other, lockpick).object_names
        self.assertEqual(expected_outcome, actual_outcome)

        # Test other, other2
        actual_outcome = action.create_outcome(outcome_const, other, other2).object_names
        expected_outcome = Outcome(outcome_const, other, other2).object_names
        self.assertEqual(expected_outcome, actual_outcome)


class TestExecute(TestAction):
    def test_invalid(self):
        self.commands = "take invalid"
        self.assertOutcome(INVALID_OBJECTS, ['invalid'])

    def test_out_of_scope(self):
        self.commands = "take barrel"
        self.assertOutcome(OUT_OF_SCOPE, ['barrel'])

    def test_command_transform(self):
        self.commands = "take lockpick", "use lockpick lock"
        self.assertOutcome(COMMAND_TRANSFORMED, ['lockpick', 'lock'])


class TextExamine(TestAction):
    def test_examine(self):
        self.commands = "examine"
        self.assertOutcome(NO_MESSAGE, ['cell'])

    def test_examine_current_room(self):
        self.commands = "examine cell"
        self.assertOutcome(NO_MESSAGE, ['cell'])

    def test_examine_another_room(self):
        self.commands = "examine dungeon"
        self.assertOutcome(CANT_EXAMINE_FROM_CURRENT_ROOM, ['dungeon'])

    def test_examine_object(self):
        self.commands = "examine key"
        self.assertOutcome(NO_MESSAGE, ['key'])


class TestTake(TestAction):
    def test_invalid(self):
        self.commands = "take"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_obtainable(self):
        self.commands = "take lockpick"
        self.assertOutcome(TAKE_SUCCESS, ['lockpick'])

    def test_non_obtainable(self):
        self.commands = "take lock"
        self.assertOutcome(NOT_OBTAINABLE, ['lock'])

    def test_already_obtained(self):
        self.commands = "take lockpick", "take lockpick"
        self.assertOutcome(ALREADY_OBTAINED, ['lockpick'])

    def test_take_from_owner(self):
        self.commands = "take lockpick from cell"
        self.assertOutcome(TAKE_FROM_OWNER_SUCCESS, ['lockpick', 'cell'])

    def test_take_from_owner_not_owned(self):
        self.commands = "take lockpick from wall"
        self.assertOutcome(NOT_OWNED_BY_OBJECT, ['lockpick', 'wall'])


class TestDrop(TestAction):
    def test_invalid(self):
        self.commands = "drop"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_dropable(self):
        self.commands = "take lockpick", "drop lockpick"
        self.assertOutcome(DROP_SUCCESS, ['lockpick'])

    def test_non_in_possession(self):
        self.commands = "drop lockpick"
        self.assertOutcome(NOT_IN_POSSESSION, ['lockpick'])


class TestUse(TestAction):
    def test_invalid(self):
        self.commands = "use"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_usable_on_target(self):
        pass

    def test_not_usable(self):
        self.commands = "use lock"
        self.assertOutcome(NOT_USABLE, ['lock'])

    def test_not_owned(self):
        self.commands = "use lockpick"
        self.assertOutcome(NOT_HELD, ['lockpick'])


class TestLock(TestAction):
    def test_invalid(self):
        self.commands = "lock"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_with_lockpick(self):
        self.commands = "take lockpick", "unlock lock", "lock lock lockpick"
        self.assertOutcome(CANT_LOCK_WITH_OBJECT, ['lockpick'])

    def test_with_key(self):
        self.commands = "take key", "unlock lock key", "lock lock key"
        self.assertOutcome(LOCK_SUCCESS, ['lock', 'key'])

    def test_with_lockpick_in_inventory(self):
        self.commands = "take lockpick", "unlock lock", "lock lock"
        self.assertOutcome(CANT_LOCK_WITH_OBJECT, ['lockpick'])

    def test_with_key_in_inventory(self):
        self.commands = "take key", "unlock lock", "lock lock"
        self.assertOutcome(LOCK_SUCCESS, ['lock', 'key'])

    def test_locking_tool_cant_lock(self):
        self.commands = "take lockpick", "unlock lock", "lock lock lockpick"
        self.assertOutcome(CANT_LOCK_WITH_OBJECT, ['lockpick'])

    def test_locking_tool_not_in_possession(self):
        self.commands = "take key", "unlock door", "lock lock lockpick"
        self.assertOutcome(NOT_IN_POSSESSION, ['lockpick'])

    def test_missing_locking_tool(self):
        self.commands = "take key", "unlock lock", "drop key", "lock lock"
        self.assertOutcome(MISSING_LOCKING_TOOL, [])

    def test_not_a_locking_tool(self):
        self.commands = "take stone", "take key", "unlock lock", "lock lock stone"
        self.assertOutcome(NOT_A_LOCKING_TOOL, ['stone'])

    def test_already_locked(self):
        self.commands = "take key", "lock lock key"
        self.assertOutcome(ALREADY_LOCKED, ['lock'])

    def test_not_lockable(self):
        self.commands = "take lockpick", "lock stone lockpick"
        self.assertOutcome(NOT_LOCKABLE, ['stone'])


class TestUnlock(TestAction):
    def test_invalid(self):
        self.commands = "unlock"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_with_lockpick(self):
        self.commands = "take lockpick", "unlock lock lockpick"
        self.assertOutcome(UNLOCK_SUCCESS, ['lock', 'lockpick'])

    def test_with_key(self):
        self.commands = "take key", "unlock lock key"
        self.assertOutcome(UNLOCK_SUCCESS, ['lock', 'key'])

    def test_with_lockpick_in_inventory(self):
        self.commands = "take lockpick", "unlock lock"
        self.assertOutcome(UNLOCK_SUCCESS, ['lock', 'lockpick'])

    def test_with_key_in_inventory(self):
        self.commands = "take key", "unlock lock"
        self.assertOutcome(UNLOCK_SUCCESS, ['lock', 'key'])

    def test_unlocking_tool_not_in_possession(self):
        self.commands = "unlock lock lockpick"
        self.assertOutcome(NOT_IN_POSSESSION, ['lockpick'])

    def test_missing_unlocking_tool(self):
        self.commands = "unlock lock"
        self.assertOutcome(MISSING_UNLOCKING_TOOL, [])

    def test_not_an_unlocking_tool(self):
        self.commands = "take stone", "unlock lock stone"
        self.assertOutcome(NOT_AN_UNLOCKING_TOOL, ['stone'])

    def test_not_lockable(self):
        self.commands = "take lockpick", "unlock stone lockpick"
        self.assertOutcome(NOT_LOCKABLE, ['stone'])


class TestOpen(TestAction):
    def test_invalid(self):
        self.commands = "open"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_open(self):
        self.commands = "take lockpick", "unlock door", "open door"
        self.assertOutcome(OPEN_SUCCESS, ['door'])

    def test_open_locked(self):
        self.commands = "take lockpick", "open door"
        self.assertOutcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_open_locked_with_opening_tool(self):
        self.commands = "take lockpick", "open door lockpick"
        self.assertOutcome(OPEN_SUCCESS, ['door', 'lockpick'])

    def test_already_open(self):
        self.commands = "take lockpick", "open door lockpick", "open door"
        self.assertOutcome(ALREADY_OPEN, ['door'])

    def test_not_openable(self):
        self.commands = "open stone"
        self.assertOutcome(NOT_OPENABLE, ['stone'])


class TestClose(TestAction):
    def test_invalid(self):
        self.commands = "close"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_close(self):
        self.commands = "take lockpick", "open door lockpick", "close door"
        self.assertOutcome(CLOSE_SUCCESS, ['door'])

    def test_already_closed(self):
        self.commands = "close door"
        self.assertOutcome(ALREADY_CLOSED, ['door'])

    def test_not_closable(self):
        self.commands = "close stone"
        self.assertOutcome(NOT_CLOSABLE, ['stone'])


class TestGo(TestAction):
    def test_invalid(self):
        self.commands = "go"
        self.assertOutcome(INVALID_COMMAND, [])

    def test_go(self):
        self.commands = "take lockpick", "open door lockpick", "go dungeon"
        self.assertOutcome(NO_MESSAGE, ['dungeon'])

    def test_connection_blocked(self):
        self.commands = "go dungeon"
        self.assertOutcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_not_connection_to_current_room(self):
        self.commands = "go courtyard"
        self.assertOutcome(NOT_ACCESSIBLE_FROM_CURRENT_ROOM, ['courtyard'])

    def test_already_in_room(self):
        self.commands = "go cell"
        self.assertOutcome(ALREADY_IN_ROOM, ['cell'])

    def test_not_accessible(self):
        self.commands = "go stone"
        self.assertOutcome(NOT_ACCESSIBLE, ['stone'])


class TestExit(TestAction):
    def test_exit(self):
        self.commands = "take key", "unlock door", "exit"
        self.assertOutcome(COMMAND_TRANSFORMED)

    def test_current_room(self):
        self.commands = "take key", "unlock door", "exit the cell"
        self.assertOutcome(COMMAND_TRANSFORMED)

    def test_specified_exit(self):
        self.commands = "take key", "unlock door", "exit from the door"
        self.assertOutcome(COMMAND_TRANSFORMED)

    def test_current_room_using_specified_exit(self):
        self.commands = "take key", "unlock door", "exit the cell from the door"
        self.assertOutcome(COMMAND_TRANSFORMED)

    def test_multiple_exits(self):
        self.commands = "take lockpick", "open door lockpick", "go dungeon", "exit dungeon"
        self.assertOutcome(UNSPECIFIED_EXIT, [])

    def test_another_room(self):
        self.commands = "exit the dungeon"
        self.assertOutcome(NOT_IN_LOCATION, ['dungeon'])


class TestThrow(TestAction):
    def test_throw(self):
        self.commands = "take stone", "throw stone"
        self.assertOutcome(COMMAND_TRANSFORMED, [])

    def test_throw_at_not_animate(self):
        self.commands = "take stone", "throw stone at door"
        self.assertOutcome(THROW_SUCCESS, ['stone', 'door'])

    def test_throw_not_in_possession(self):
        self.commands = "throw stone"
        self.assertOutcome(NOT_IN_POSSESSION, ['stone'])

    def test_throw_at_animate_target(self):
        self.commands = "take stone", "throw stone at guard"
        self.execute_commands()
        self.assertEqual(self.get('guard').attitude, -1)


class TestGuard(TestAction):
    def test_throw_multiple(self):
        self.commands = "take stone", "throw stone at guard"
        self.execute_commands()
        self.assertEqual(self.get('guard').attitude, -1)

        self.commands = "take lockpick", "throw lockpick at guard"
        self.execute_commands()
        self.assertEqual(self.get('guard').attitude, -2)

        self.commands = "take tag", "throw tag at guard"
        self.execute_commands()
        self.assertEqual(self.get('guard').attitude, -3)

    def test_throw_multiple_key_stolen(self):
        self.commands = "take key", "take stone", "throw stone at guard"
        self.execute_commands()
        self.commands = "take lockpick", "throw lockpick at guard"
        self.execute_commands()
        self.commands = "take tag", "throw tag at guard"
        self.execute_commands()
        self.assertTrue(self.get('key') in self.world.player.inventory)
        self.assertEqual(self.get('guard').attitude, -3)
        self.assertTrue(self.get('guard').parent == self.get('courtyard'))


class TestLockingTool(TestAction):
    def test_use_usable_alone(self):
        self.commands = "take lockpick", "use lockpick"
        self.assertOutcome(CANT_USE_OBJECT_ALONE, ["lockpick"])

    def test_use_on_not_lockable(self):
        self.commands = "take lockpick", "use lockpick stone"
        self.assertOutcome(CANT_USE_OBJECT_ON_TARGET, ['lockpick', 'stone'])


class TestDoor(TestAction):
    def test_blocked_locked(self):
        self.commands = "go dungeon"
        self.assertOutcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_blocked_closed(self):
        self.commands = "take lockpick", "unlock door", "go dungeon"
        self.assertOutcome(BLOCKED_OBJECT_CLOSED, ['door'])

    def test_open_locked(self):
        self.commands = "open door"
        self.assertOutcome(BLOCKED_OBJECT_LOCKED, ['door'])

    def test_open_locked_with_tool(self):
        self.commands = "take lockpick", "open door lockpick"
        self.assertOutcome(OPEN_SUCCESS, ['door', 'lockpick'])

    def test_lock_open(self):
        self.commands = "take key", "open door key", "lock door"
        self.assertOutcome(MUST_CLOSE_OBJECT, ['door', 'key'])


class TestMattress(TestAction):
    def test_examine(self):
        self.commands = "examine mattress"
        result = self.execute_commands()
        lockpick = result.action.world.get('lockpick')
        self.assertFalse(lockpick.concealed)


class TestStone(TestAction):
    def test_take(self):
        self.commands = "take stone"
        self.execute_commands()
        self.assertEqual(self.get('stone').parent, self.world.player)
