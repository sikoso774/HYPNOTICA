import pygame
import sys
from game.config.settings import WIDTH, HEIGHT

# Main Class
from main import Game

# Screens imports
from game.core.screens import *
from game.core import Level3D, WorldMap

class Debugger:
    """Interactive console picker for jumping directly to any screen."""

    def __init__(self):
        self.screens = {
            "1": ("Intro (Splash)", Intro),
            "2": ("Main Menu", MainMenu),
            "3": ("Instructions", Instructions),
            "4": ("Game (Level)", Level3D),
            "5": ("Game Over", GameOver),
            "6": ("Credits", Credits),
            "7": ("World Map", WorldMap),
        }

    def run_debug(self):
        try:
            game_instance = Game()
            while True:
                print("\nWhich screen do you want to test?")
                for key, (name, _) in self.screens.items():
                    print(f"[{key}] {name}")
                print("[Q] Quit Debugger")

                choice = input("Your choice: ").lower()

                if choice == 'q':
                    print("Closing for good.")
                    pygame.quit()
                    sys.exit()

                if choice in self.screens:
                    screen_name, screen_class = self.screens[choice]
                    print(f"\n>>> Launching: {screen_name}...")
                    print("    (Press the close button or ESC to come back here)")

                    # ----Error handling
                    try:
                        # 1. Make sure Pygame is alive
                        if not pygame.get_init():
                            pygame.init()
                            # Recreate the window if it was closed
                            game_instance.screen = pygame.display.set_mode((WIDTH, HEIGHT))

                        # 2. Launch the screen
                        current_screen = screen_class(game_instance)

                        # Small trick: disable music for debugging if you want
                        # current_screen.music_name = None

                        current_screen.run()

                    except SystemExit:
                        # This is where we catch the game's sys.exit() call!
                        print(">>> Game exit intercepted. Returning to debug menu.")

                    except KeyboardInterrupt:
                        print("Script stop requested (CTRL+C)")
                        sys.exit()

                    except Exception as e:
                        print(f">>> Unexpected error: {e}")

                    # 3. Post-crash repair
                    # If the game called pygame.quit(), we need to restart it for the next round
                    if not pygame.get_init() or not pygame.display.get_surface():
                        print(">>> Reinitializing the graphics engine...")
                        pygame.init()
                        game_instance.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        # Make sure sound is also restarted if needed
                        try:
                            pygame.mixer.init()
                        except:
                            pass

                else:
                    print("Invalid choice.")

        except KeyboardInterrupt:
            print("Script stop requested (CTRL + C)")
            sys.exit(0)

        except Exception as e:
            print(f"An error occurred while running the script: {e}")
            sys.exit(1)


if __name__ == "__main__":
    debugger = Debugger()
    debugger.run_debug()