from random import random, choices

from attributes import Animate
from outcomes import NO_MESSAGE


class Guard(Animate):
    NOT_IN_DUNGEON = "NOT_IN_DUNGEON"
    NEAR_EXIT = "NEAR_EXIT"
    PATROLLING = "PATROLLING"
    NEAR_CELL = "NEAR_CELL"
    BACK_OF_DUNGEON = "BACK_OF_DUNGEON"

    guard_location: str = NEAR_CELL
    searching_for_key = False
    searching_for_player = False
    stunned = False

    def check_player_detected(self):
        """
        If the player is in the dungeon, he is always considered to be NEAR_CELL.
        There will be a chance of detection if both are in the dungeon, but not in the same spot.
        If the guard is NEAR_EXIT or BACK_OF_DUNGEON, the chance of detection is small.
        If the guard is PATROLLING, the chance of detection is great.
        If the guard is NEAR_CELL, he will spot the player immediately.
        :return: True if the player is detected, else False
        """
        cell = self.get('cell')
        dungeon = self.get('dungeon')
        cell_door = self.get('cell door')

        if self.asleep or self.stunned or self.searching_for_key or self.guard_location == self.NOT_IN_DUNGEON:
            return False

        chance_of_detection = {
            self.NOT_IN_DUNGEON: 0,
            self.NEAR_EXIT: 0.125,
            self.PATROLLING: 0.25,
            self.NEAR_CELL: 1,
            self.BACK_OF_DUNGEON: 0.125,
        }
        player_in_barrel = self.player in self.get('barrel').contents

        def print_detection_status():
            print(
                f"room: {self.parent}\n"
                f"location: {self.guard_location}\n"
                f"player in barrel: {player_in_barrel}\n"
                f"searching for player: {self.searching_for_player}\n"
                f"cell door open: {cell_door.is_open}"
            )

        player_detected = random() < (
                    chance_of_detection[self.guard_location] * (not player_in_barrel or self.searching_for_player))
        cell_door_open_detected = random() < (
                    chance_of_detection[self.guard_location] * cell_door.is_open * (not self.searching_for_player))
        if self.current_room == dungeon:
            if not (player_detected or cell_door_open_detected):
                return False
            if player_detected:
                if player_in_barrel:
                    self.message(f"The {self} spots you inside the barrel!")
                else:
                    self.message(f"The {self} spots you outside of your cell!")
                # print_detection_status()
            elif cell_door_open_detected:
                self.message(f"The {self} spots the open door of your cell!")
                # print_detection_status()
                if player_in_barrel:
                    self.message(f"He starts patrolling the whole dungeon with dedication.")
                    self.searching_for_player = True
                    self.guard_location = self.PATROLLING
                    return False

        elif self.current_room == cell and cell_door.is_open:
            if not cell_door_open_detected:
                return False
            self.message(f"The {self} spots the open door of your cell!")
            # print_detection_status()

        else:
            return False

        dead_chance = 0.25
        if random() < dead_chance:
            self.player.dead = True
            self.message(f"He rushes to your location, swiftly drawing his sword.\n"
                         f"\"Are you going somewhere, dirty mouse?\n"
                         f"This is not going to end well for you!\"\n"
                         f"In a cruel twist, he severs your hand,\n"
                         f"leaving you to bleed slowly to death.")
            return True

        drags_you_into_cell = ", then drags you into your cell." if self.current_room == dungeon else "."
        locks_you_or_kills_you = f"\"You're lucky to be alive\", he says as he locks your cell."
        if cell_door.key not in self.owned:
            self.player.dead = True
            locks_you_or_kills_you = f"\"Damn it, I must have dropped the key somewhere.\n" \
                                     f"I can't leave you here alone and unlocked.\n" \
                                     f"I'll have to kill you, dirty mouse!\"\n" \
                                     f"He draws his sword and, in a sudden move, he stabs you in the chest, " \
                                     f"leaving you to bleed slowly to death."
        self.message(f"\"Are you going somewhere, dirty mouse?\n"
                     f"This is not going to end well for you!\"\n"
                     f"He hits you with his fist and you drop on the ground{drags_you_into_cell}\n"
                     f"{locks_you_or_kills_you}")

        self.move_to(cell)
        self.guard_location = self.NEAR_CELL
        cell.go()
        cell_door.close()
        cell_door.lock(cell_door.key)
        return True

    def on_move_end(self):
        """
        Check if the guard is NEAR_CELL while the player is also in the cell,
        then make him child of cell in order for the player to be able to interact with him easily.
        On the first move of each turn, chance to fall sleep if he's sitting somewhere.
        """
        cell = self.get('cell')
        dungeon = self.get('dungeon')

        # win condition
        if self.current_room.winning_room:
            return

        if self.guard_location == self.NEAR_CELL:
            if self.current_room == cell:
                self.move_to(cell)
            elif self.current_room == dungeon:
                self.move_to(dungeon)

        if self.searching_for_key:
            self.searching_for_key -= 1

        if self.stunned:
            self.stunned -= 1
            if not self.stunned:
                self.message(f"The {self} recovers from the stun.")

        self.check_player_detected()

        if self.searching_for_player or (self.guard_location == self.PATROLLING and not self.is_last_move_of_turn):
            self.message(f"You can hear the {self}'s footsteps going back and forth in the dungeon corridor.")
        elif self.asleep:
            if not self.is_last_move_of_turn:
                guard_or_someone = f"the {self}" if self.discovered else "someone"
                snoring_location = "outside of your cell" if self.NEAR_CELL and self.current_room == cell else "while sleeping on his seat"
                still = " still" if self.world.current_move in range(2, 5) else ""
                self.message(f"You can{still} hear {guard_or_someone} snoring {snoring_location}.")
            elif self.discovered:
                self.message(f"The {self} subtly adjusts his position on his chair.")

    def print_status(self):
        print(
            f"room: {self.parent}\n"
            f"location: {self.guard_location}\n"
            f"asleep: {self.asleep}\n"
            f"stunned: {self.stunned}\n"
            f"searching: {self.searching_for_key}\n"
        )

    def on_turn_end(self):
        # win condition
        if self.current_room == self.get('courtyard'):
            return

        location_probabilities = {
            self.NOT_IN_DUNGEON: 0.1,
            self.NEAR_EXIT: 0.2,
            self.PATROLLING: 0.3,
            self.NEAR_CELL: 0.2,
            self.BACK_OF_DUNGEON: 0.2,
        }
        locations, weights = zip(*location_probabilities.items())
        new_location = choices(locations, weights)[0]

        # Location didn't change
        if new_location == self.guard_location:
            return

        # Wake up before moving
        woken_up = self.asleep
        if woken_up:
            self.asleep = False
            # Check again if the player is in sight, because now he's awake
            if self.check_player_detected():
                return

        # Don't change locations while stunned or searching for the key or the player
        if self.searching_for_key or self.stunned or self.searching_for_player:
            return

        # Hold the rooms into local variables for ease of access and read
        cell = self.get('cell')
        dungeon = self.get('dungeon')
        courtyard = self.get('courtyard')

        # Save the previous location, it will be needed
        previous_location = self.guard_location
        self.guard_location = new_location

        # Move the guard to the new location
        # Two cases: the player is in the cell, or in the dungeon
        player_in_cell = self.world.current_room == cell
        if player_in_cell:
            if new_location == self.NEAR_CELL:
                self.move_to(cell)
                # Check again if the player is in sight
                self.message(f"The {self} returns to sit on the chair next to your cell.")
                self.check_player_detected()
                return

            self.move_to(courtyard) if new_location == self.NOT_IN_DUNGEON else self.move_to(dungeon)
            if previous_location == self.NEAR_CELL:
                wakes_or_stands = "wakes up" if woken_up else "stands up"
                self.message(f"The {self} {wakes_or_stands} and leaves, disappearing from your view.")
            return

        # player in dungeon
        if new_location == self.NOT_IN_DUNGEON:
            self.move_to(courtyard)
            wakes_up = " wakes up and" if woken_up else ""
            self.message(f"The {self}{wakes_up} leaves the dungeon\n"
                         f"from the door that seems to lead to the courtyard.")
            return

        self.move_to(dungeon)

        # The part of the message describing the previous location
        if previous_location == self.NOT_IN_DUNGEON:
            prev_message = f"The {self} returns into the dungeon"
        elif previous_location == self.PATROLLING:
            prev_message = f"The {self} halts his patrol"
        else:
            prev_message = f"The {self} wakes up" if woken_up else f"The {self} stands up"

        # The part of the message describing the new location
        if new_location == self.PATROLLING:
            new_message = "and resumes patrolling."
        elif new_location == self.BACK_OF_DUNGEON:
            new_message = "and takes a seat at the far end of the dungeon."
        elif new_location == self.NEAR_EXIT:
            new_message = "and positions himself next to the exit door."
        else:  # NEAR_CELL:
            new_message = "and settles down on a chair near your cell."

        def put_randomly_into_sleep():
            chance_to_sleep = 0.5
            sleeping_locations = [self.NEAR_EXIT, self.NEAR_CELL, self.BACK_OF_DUNGEON]
            if self.guard_location in sleeping_locations and random() < chance_to_sleep:
                self.asleep = True
                return True
            return False

        sleeps = ""
        if put_randomly_into_sleep():
            sleeps = "\nHe immediately falls into sleep."
        self.message(f"{prev_message} {new_message}{sleeps}")

        if not self.asleep:
            self.check_player_detected()

    @property
    def initial(self):
        article = "The" if self.discovered else "A"
        is_sleeping = "He seems to be in a deep sleep." if self.asleep else ""

        if self.stunned:
            return f"The {self} appears to be stunned."

        player_in_cell = self.world.current_room == self.get('cell')
        if player_in_cell and self.guard_location == self.NEAR_CELL:
            return f"{article} {self} sits beside your cell's barred door. {is_sleeping}"

        # player in dungeon
        if self.guard_location == self.NOT_IN_DUNGEON:
            return ""

        if self.guard_location == self.PATROLLING:
            return f"{article} {self} patrols the dungeon, meticulously inspecting each cell. {is_sleeping}"
        elif self.guard_location == self.BACK_OF_DUNGEON:
            return f"{article} {self} rests at the far end of the dungeon. {is_sleeping}"
        elif self.guard_location == self.NEAR_EXIT:
            return f"{article} {self} sits near the dungeon's exit. {is_sleeping}"
        else:  # NEAR_CELL:
            return f"{article} {self} is positioned beside your cell's barred door. {is_sleeping}"

    @property
    def description(self):
        if self.stunned:
            return f"The {self} is stunned at the moment, trying to recover."

        player_in_cell = self.world.current_room == self.get('cell')
        if player_in_cell:
            if self.guard_location == self.NEAR_CELL:
                return f"The {self} is in a deep sleep on a chair near your cell's barred door." if self.asleep \
                    else f"The {self} sits beside your cell's barred door.\n" \
                         f"He doesn't seem to enjoy his presence here."

            return f"You can't spot the {self} outside your cell. Who knows where he's gone..."

        # player in dungeon
        if self.guard_location == self.NOT_IN_DUNGEON:
            return f"The {self} has left through a door leading to the courtyard."

        if self.guard_location == self.PATROLLING:
            return f"The {self} patrols the dungeon, inspecting each cell with a vigilant gaze. " \
                   f"He doesn't appear to enjoy his duty."

        elif self.guard_location == self.BACK_OF_DUNGEON:
            return f"The {self} is in a deep sleep on a chair\n" \
                   f"at the far end of the dungeon." if self.asleep \
                else f"The {self} rests at the far end of the dungeon.\n" \
                     f"He doesn't seem to enjoy his presence here."

        elif self.guard_location == self.NEAR_EXIT:
            return f"The {self} is in a deep sleep right next to the dungeon's exit door." if self.asleep \
                else f"The {self} sits near the dungeon's exit door.\n" \
                     f"He doesn't seem to enjoy his presence here."

        else:  # NEAR_CELL:
            return f"The {self} is in a deep sleep on a chairv" \
                   f"next to your cell's barred door." if self.asleep \
                else f"The {self} sits beside your cell's barred door.\n" \
                     f"He doesn't seem to enjoy his presence here."

    @property
    def in_scope(self):
        return self.current_room == self.parent

    def attack(self, weapon):
        if not self.in_scope:
            self.describe()
            return NO_MESSAGE

        both_in_cell = self.guard_location == self.NEAR_CELL and self.current_room == self.get('cell')
        if both_in_cell and not self.get('cell door').is_open:
            self.message(f"You can't attack the {self} from your cell with the door closed.")
            return NO_MESSAGE

        sleep_modifier = 0.1 if self.asleep else 0
        attack_outcome_probabilities = {
            'SUCCESS': 0.1 + sleep_modifier,
            'SENT_BACK_TO_CELL': 0.6 - sleep_modifier / 2,
            'DEATH': 0.3 - sleep_modifier / 2
        }
        outcomes, weights = zip(*attack_outcome_probabilities.items())
        attack_outcome = choices(outcomes, weights)[0]

        waked_him = " but it waked him up" if self.asleep else ""
        self.asleep = False

        stun_duration = "for a while"
        if self.stunned:
            attack_outcome = 'SUCCESS'
            stun_duration = "even more"

        if attack_outcome == 'SUCCESS':
            self.stunned += 5
            self.attitude -= 3
            self.message(f"Your attack managed to land a hit to the {self}, stunning him {stun_duration}.")
            return NO_MESSAGE

        if attack_outcome == 'SENT_BACK_TO_CELL':
            drags_you_into_cell = ", then drags you into your cell." if self.current_room == self.get('dungeon') else ""
            locks_you_or_kills_you = f"\"You're lucky to be alive\", he says as he locks your cell."
            if self.get('keys') not in self.owned:
                self.player.dead = True
                locks_you_or_kills_you = f"\"Damn it, I must have dropped the key somewhere.\n" \
                                         f"I can't leave you here alone and unlocked.\n" \
                                         f"I'll have to kill you, dirty mouse!\"\n" \
                                         f"He draws his sword and, in a sudden move, he stabs you in the chest,\n" \
                                         f"leaving you to bleed slowly to death."
            self.move_to(self.get('cell'))
            self.guard_location = self.NEAR_CELL
            self.get('cell').go()
            self.get('cell door').close()
            self.get('cell door').lock(self.get('iron key'))
            self.message(f"Your attack nearly missed the {self}{waked_him} and now he's furious.\n"
                         f"\"You're gonna pay for that, dirty mouse!\n"
                         f"This is not going to end well for you!\"\n"
                         f"He hits you with his fist and you drop on the ground{drags_you_into_cell}\n"
                         f"{locks_you_or_kills_you}")
            return NO_MESSAGE

        if attack_outcome == 'DEATH':
            self.player.dead = True
            self.message(f"Your attack manages to land a hit to the {self},\n"
                         f"surprising him, but he recovers quickly.\n"
                         f"\"You're gonna pay for that, dirty mouse!\n"
                         f"This is not going to end well for you!\"\n"
                         f"He draws his sword and, in a sudden move, he stabs you in the chest,\n"
                         f"leaving you to bleed slowly to death.")
            return NO_MESSAGE

    def wake(self):
        if not self.in_scope or self.stunned:
            self.describe()
            return NO_MESSAGE

        self.asleep = False
        self.message(f"The {self} startles awake, quickly composing himself as if he was never sleeping.")
        return NO_MESSAGE

    def ask(self):
        if not self.in_scope or self.asleep or self.stunned:
            self.describe()
            return NO_MESSAGE
        self.message(
            f"The {self} pointedly ignores your attempts at conversation.\n"
            f"It seems he's not in the mood for chatting.")
        return NO_MESSAGE

    def tell(self):
        if not self.in_scope or self.asleep or self.stunned:
            self.describe()
            return NO_MESSAGE
        self.message("He dismissively waves off whatever you're saying.\n"
                     "It's clear he has no interest in your words.")
        return NO_MESSAGE

    def throw(self, thrown_object):
        if not self.in_scope:
            self.describe()
            return NO_MESSAGE

        woken_up = self.asleep
        self.asleep = False
        self.attitude -= 1

        chance_to_stun = 0.1
        if random() < chance_to_stun:
            self.stunned += 5
            self.attitude -= 2
            self.message(f"Your throw managed to land a critical hit to the {self}, stunning him for a while.")
            return NO_MESSAGE

        both_in_dungeon = self.guard_location != self.NOT_IN_DUNGEON and self.current_room == self.get('dungeon')
        if both_in_dungeon:
            self.player.dead = True
            wake_up_message = f" wakes him up and" if woken_up else ""
            self.message(
                f"The {thrown_object} you throw at the {self}\n"
                f"{wake_up_message} notifies him of your presence.\n"
                f"He rushes to your location, swiftly drawing his sword.\n"
                f"\"How did you get you out of your cell, dirty mouse? Are you going somewhere?\"\n"
                f"In a cruel twist, he severs your hand, leaving you to bleed slowly to death.")
            return NO_MESSAGE

        if self.attitude == -1:
            wake_up_message = "and it startles him awake" if woken_up else ""
            self.message(f"You throw the {thrown_object} at the {self}\n"
                         f"{wake_up_message}, but he remains unfazed.\n"
                         "\"Sit down, little scum. You're not getting anywhere,\" he sneers.")
            return NO_MESSAGE

        if self.attitude == -2:
            wake_up_message = ", catching him off guard," if woken_up else ""
            self.message(f"The {self} reacts to the {thrown_object}\n"
                         f"you threw at him{wake_up_message} with a warning:\n"
                         f"\"This is your last warning, filthy person.\n"
                         f"Try this again, and you'll regret it.\"")
            return NO_MESSAGE

        if self.attitude <= -3 and self.get('keys').is_attached_to(self):
            self.player.dead = True
            wake_up_message = "and fully waked him up" if woken_up else ""
            self.message(f"The {thrown_object} you threw at the {self}\n"
                         f"{wake_up_message} was the final straw.\n"
                         f"He storms into your cell, swiftly drawing his sword.\n"
                         f"In a cruel twist, he severs your hand,\n"
                         f"leaving you to bleed slowly to death.")
            return NO_MESSAGE

        wake_up_message = " and fully waked him up" if woken_up else ""
        self.move_to(self.get('courtyard'))
        self.guard_location = self.NOT_IN_DUNGEON
        self.searching_for_key = 10
        self.message(f"The {thrown_object} you threw at the {self}\n"
                     f"{wake_up_message} was the final straw.\n"
                     f"He attempts to enter your cell, but realization dawns on his face.\n"
                     f"\"Damn it, I must have dropped the key at the toilets!\"\n"
                     f"He hastily exits the prison dungeon to search for the key,\n"
                     f"leaving you with an opportunity...")
        return NO_MESSAGE
