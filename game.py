from world import World


class Game:
    def __init__(self, test=False):
        self.test = test
        self.world = World()
        self.world.populate()

    def run(self):
        print("\nWelcome to ESCAPE FROM IRONHOLD\n")

        # Print help prompt
        print("\nType 'help' to see a list of available commands.\n\n")

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
                print("\n. . . GAME OVER . . .")
                break
            elif dead == 2:
                print("\n! ! ! YOU WIN ! ! !")
                break
