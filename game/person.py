import random
from random import choices

from .attributes import Animate
from .outcomes import SUCCESS, NEUTRAL, NO_MESSAGE


class Guard(Animate):
    # TODO
    #  - Examine details:
    #       - The player in cell can only see the guard if he's right next to the prison cell
    #       - The guard is always in scope, child of cell if next to the cell, else child of dungeon
    #       - If the player is in the dungeon, the guard does not become child of cell
    #  - Very slim chance that a thrown object will stun him.
    #  - Chance that a throw will miss.
    #  - Throw an object to distract him.
    #  - The player can only attack the guard if they're both in the dungeon
    #  - Attack has a slim chance of succeeding, medium chance of being sent back to the cell and great chance of death
    #  - Implement different chance to steal the keys when asleep and when awake
    #  - Any failed attempt to take the keys results in medium chance of being sent back to the cell and great chance of death
    #  - Very slim chance to steal the sword
    #  - What happens if you throw the sword at him?
    #  - What about throwing objects at him when not in the cell?

    NOT_IN_DUNGEON = "NOT_IN_DUNGEON"
    NEAR_EXIT = "NEAR_EXIT"
    PATROLLING = "PATROLLING"
    NEAR_CELL = "NEAR_CELL"
    BACK_OF_DUNGEON = "BACK_OF_DUNGEON"

    current_location = NEAR_CELL

    def on_move_end(self):
        # When the guard is located NEAR_CELL, we want him to be child of cell if player is also in the cell
        # (move_to alters the object tree and moves the object to another parent)
        if self.current_location == self.NEAR_CELL:
            if self.world.current_room == self.world.get('cell'):
                self.move_to(self.world.get('cell'))
            else:
                self.move_to(self.world.get('dungeon'))

        # Put self randomly into sleep if near exit, cell, or back of dungeon
        chance_to_sleep = 0.5
        sleeping_locations = [self.NEAR_EXIT, self.NEAR_CELL, self.BACK_OF_DUNGEON]
        if not self.asleep \
                and self.world.current_move == 1 \
                and self.current_location in sleeping_locations \
                and random.random() < chance_to_sleep:
            self.asleep = True
        # print(
        #     f"asleep: {self.asleep}\n"
        #     f"location: {self.current_location}\n"
        #     f"room: {self.parent}"
        # )

    def on_turn_end(self):
        # Get a new random location
        location_probabilities = {
            self.NOT_IN_DUNGEON: 0.1,
            self.NEAR_EXIT: 0.2,
            self.PATROLLING: 0.3,
            self.NEAR_CELL: 0.2,
            self.BACK_OF_DUNGEON: 0.2,
        }
        locations, weights = zip(*location_probabilities.items())
        new_location = choices(locations, weights)[0]

        # Not changing location
        if new_location == self.current_location:
            return

        previous_location = self.current_location
        self.current_location = new_location

        # Wake up before moving
        woken_up = self.asleep
        if self.asleep:
            self.asleep = False

        cell = self.world.get('cell')
        dungeon = self.world.get('dungeon')
        courtyard = self.world.get('courtyard')

        # Move the guard to the new location
        # Two cases: the player is in the cell, or in the dungeon

        # First case: the player is in the cell
        if self.world.current_room == cell:
            if new_location == self.NEAR_CELL:
                self.move_to(cell)
                self.message(f"The {self} returns to sit on the chair next to your cell.")
                return

            self.move_to(courtyard) if new_location == self.NOT_IN_DUNGEON else self.move_to(dungeon)
            if previous_location == self.NEAR_CELL:
                wakes_or_stands = "wakes up" if woken_up else "stands up"
                self.message(f"The {self} {wakes_or_stands} and leaves, disapearring from your view.")
            return

        # Second case: the player is in the dungeon (probably hidden)
        if new_location == self.NOT_IN_DUNGEON:
            self.move_to(courtyard)
            wakes_up = "wakes up and" if woken_up else ""
            self.message(f"The {self} {wakes_up} leaves the dungeon from the door that seems to lead to the courtyard.")
            return

        self.move_to(dungeon)

        # The part of the message describing the previous location
        if previous_location == self.NOT_IN_DUNGEON:
            prev_message = f"The {self} returns into the dungeon"
        elif previous_location == self.PATROLLING:
            prev_message = f"The {self} halts his patrol"
        else:
            wakes_or_stands = "wakes up" if woken_up else "stands up"
            prev_message = f"The {self} {wakes_or_stands}"

        # The part of the message describing the new location
        if new_location == self.PATROLLING:
            new_message = "and resumes patrolling."
        elif new_location == self.BACK_OF_DUNGEON:
            new_message = "and takes a seat at the far end of the dungeon."
        elif new_location == self.NEAR_EXIT:
            new_message = "and positions himself next to the exit door."
        else:  # new_location == self.NEAR_CELL:
            new_message = f"and settles down on a chair near your cell."

        self.message(f"{prev_message} {new_message}")

    def attack(self):
        return NO_MESSAGE

    def wake(self):
        self.asleep = False
        return "The guard startles awake, quickly composing himself as if he was never sleeping.", SUCCESS

    def ask(self):
        if self.asleep:
            self.describe()
            return NO_MESSAGE
        return "The guard pointedly ignores your attempts at conversation. It seems he's not in the mood for chatting.", NEUTRAL

    def tell(self):
        if self.asleep:
            self.describe()
            return NO_MESSAGE
        return "He dismissively waves off whatever you're saying. It's clear he has no interest in your words.", NEUTRAL

    def throw(self, thrown_object):
        woken_up = self.asleep
        self.asleep = False
        self.attitude -= 1

        if self.attitude == -1:
            wake_up_message = " and it startles him awake" if woken_up else ""
            return f"You throw the {thrown_object} at the {self}{wake_up_message}, but he remains unfazed.\n" \
                   "\"Sit down, little scum. You're not getting anywhere,\" he sneers.", SUCCESS

        if self.attitude == -2:
            wake_up_message = ", catching him off guard," if woken_up else ""
            return f"The {self} reacts to the {thrown_object} you threw at him{wake_up_message} with a warning:\n" \
                   f"\"This is your last warning, filthy person. Try this again, and you'll regret it.\"", SUCCESS

        if self.attitude == -3 and self.world.get('key').is_attached_to(self):
            self.player.dead_flag = 1
            wake_up_message = " and fully wakes him up" if woken_up else ""
            return f"The {thrown_object} you threw at the {self}{wake_up_message} was the last straw.\n" \
                   f"He storms into your cell, swiftly drawing his sword.\n" \
                   f"In a cruel twist, he severs your hand, leaving you to bleed slowly to death.", SUCCESS

        wake_up_message = " and fully wakes him up" if woken_up else ""
        self.move_to(self.world.get('courtyard'))
        return f"The {thrown_object} you threw at the {self}{wake_up_message} was the final straw.\n" \
               f"He attempts to enter your cell, but realization dawns on his face.\n" \
               f"\"Damn it, I must have dropped the key at the toilets!\"\n" \
               f"He hastily exits the prison dungeon to search for the key, leaving you with an opportunity...", SUCCESS
