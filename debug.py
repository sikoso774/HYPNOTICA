import pygame
import sys
from game.config.settings import WIDTH, HEIGHT

# Main Class
from main import Game

# Screens imports
from game.core.screens import *
from game.core import Level_3D

class Debugger:
    def __init__(self):
        self.screens = {
            "1": ("Intro (Splash)", Intro),
            "2": ("Menu Principal", MainMenu),
            "3": ("Instructions", Instructions),
            "4": ("Jeu (Level)", Level_3D),
            "5": ("Game Over", GameOver),
            "6": ("Crédits", Credits),
        }
    
    def run_debug(self):
        try:
            game_instance = Game()
            while True:
                print("\nQuel écran voulez-vous tester ?")
                for key, (name, _) in self.screens.items():
                    print(f"[{key}] {name}")
                print("[Q] Quitter le Debugger")

                choice = input("Votre choix : ").lower()

                if choice == 'q':
                    print("Fermeture définitive.")
                    pygame.quit()
                    sys.exit()

                if choice in self.screens:
                    screen_name, screen_class = self.screens[choice]
                    print(f"\n>>> Lancement de : {screen_name}...")
                    print("    (Appuyez sur la croix ou ESC pour revenir ici)")

                    # ----Gestion des erreurs
                    try:
                        # 1. On s'assure que Pygame est vivant
                        if not pygame.get_init():
                            pygame.init()
                            # On recrée la fenêtre si elle a été fermée
                            game_instance.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        
                        # 2. On lance l'écran
                        current_screen = screen_class(game_instance)
                        
                        # Petite astuce : on désactive la musique pour le debug si vous voulez
                        # current_screen.music_name = None
                        
                        current_screen.run()
                    
                    except SystemExit:
                        # C'est ici qu'on capture le sys.exit() du jeu !
                        print(">>> Sortie du jeu interceptée. Retour au menu de debug.")
                        
                    except KeyboardInterrupt:
                        print("Arrêt du script demandé (CTRL+C)")
                        sys.exit()
                        
                    except Exception as e:
                        print(f">>> Erreur inattendue : {e}")

                    # 3. Réparation post-crash
                    # Si le jeu a appelé pygame.quit(), on doit le relancer pour le prochain tour
                    if not pygame.get_init() or not pygame.display.get_surface():
                        print(">>> Réinitialisation du moteur graphique...")
                        pygame.init()
                        game_instance.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        # On s'assure que le son est aussi relancé si besoin
                        try:
                            pygame.mixer.init()
                        except:
                            pass
                    
                else:
                    print("Choix invalide.")
                
        except KeyboardInterrupt:
            print("Arrêt du script demandé (CTRL + C)")
            sys.exit(0)
            
        except Exception as e:
            print(f"Une erreur est survenue lors de l'exécution du script: {e}")
            sys.exit(1)


if __name__ == "__main__":
    debugger = Debugger()
    debugger.run_debug()