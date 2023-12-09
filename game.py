from world import World


class Game:
    def __init__(self, test=False):
        self.test = test
        self.world = World()
        self.world.populate()

    def run(self):
        print("\nWelcome to ESCAPE FROM IRONHOLD\n")

        # Print help prompt
        print("\nType 'help' to see a list of the main verbs.\n\n")

        # First describe the initial room
        self.world.current_room.discover()

        # Start the game loop
        while True:
            # Input
            print("\nWhat do you want to do?")
            input_command = input("> ")

            # Parse
            self.world.parse(input_command)

            # End game check
            dead = self.world.player.dead
            if dead == 1:
                print("\nAnd so, as the final breath dissolves into the cosmic breath,\n"
                      "the essence of a singular journey merges with the universe,\n"
                      "leaving an indelible mark on the ever-expanding canvas of existence.\n"
                      "In the face of mortality's inevitability, may we find solace in the enigma\n"
                      "of our fleeting presence and the eternal dance that continues beyond the veil.\n")
                print(". . . GAME OVER . . .")
                break
            elif dead == 2:
                print("\n! ! ! YOU WIN ! ! !")
                break
