from abc import ABC
from .game_object import GameObject
from .attributes import Animate
from .outcomes import SUCCESS, NEUTRAL, NO_MESSAGE


class Guard(GameObject, Animate):
    # TODO
    #  - Make the guard move around, patroling the dungeon, exiting the dungeon and sleeping randomly
    #  - The player in cell can only see the guard if he's right next to the prison cell
    #       - The guard is always in scope, child of cell if next to the cell, else child of dungeon
    #           - If the player is in the dungeon, the guard does not become child of cell
    #  - Very slim chance that a thrown object will stun him.
    #  - Chance that a throw will miss.
    #  - Throw an object to distract him.
    #  - The player can only attack the guard if they're both in the dungeon
    #  - Attack has a slim chance of succeeding, medium chance of sent back to the cell and great chance of death
    #  - Implement different chance to steal the key when asleep and when awake
    #  - Any failed attempt to take the key results to medium chance of sent back to the cell and great chance of death
    #  - Very slim chance to steal the sword
    #  - What happens if you throw the sword at him?
    #  - What about throwing objects at him when not in the cell?

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
