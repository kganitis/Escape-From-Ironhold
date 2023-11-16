from abc import ABC
from .game_object import GameObject
from .attributes import Animate
from .outcomes import SUCCESS, NO_MESSAGE


class Guard(GameObject, Animate):
    def attack(self):
        return NO_MESSAGE

    def wake(self):
        self.asleep = False
        return "You startled the guard and he's now pretending he was never sleeping.", SUCCESS

    def ask(self):
        return NO_MESSAGE

    def tell(self):
        return NO_MESSAGE

    def throw(self, thrown_object):
        woken_up = self.asleep
        self.asleep = False
        self.attitude -= 1

        if self.attitude == -1:
            wake_up_message = " and it wakes him up" if woken_up else ""
            return f"You throw the {thrown_object} at the {self}{wake_up_message} but he doesn't seem to care.\n" \
                   "\"Sit down little scum, you're not getting anywhere.\"", SUCCESS

        if self.attitude == -2:
            wake_up_message = ", while he was sleeping," if woken_up else ""
            return f"The {self} reacts to the {thrown_object} you threw at him{wake_up_message} by warning you:\n" \
                   f"\"This is your last warning filthy person. Try this again and you're going to regret it.\"", SUCCESS

        if self.attitude == -3 and self.world.get('key').is_attached_to(self):
            self.player.dead_flag = 1
            wake_up_message = " and waked him up" if woken_up else ""
            return f"The {thrown_object} you threw at the {self}{wake_up_message} was the last straw.\n" \
                   f"He enters your cell and cuts your hand off with his sword.\n" \
                   f"He leaves you there alone and you bleed slowly to death.", SUCCESS

        wake_up_message = " and waked him up" if woken_up else ""
        self.move_to(self.world.get('courtyard'))
        return f"The {thrown_object} you threw at the {self}{wake_up_message} was the last straw.\n" \
               f"He attempts to enter your cell but he can't find the key.\n" \
               f"\"Damn it, I must have dropped the key at the toilets!\"\n" \
               f"He leaves the prison dungeon to go and search for the key.\n" \
               f"Now is the time...", SUCCESS
