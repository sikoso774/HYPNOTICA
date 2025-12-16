from ..config.settings import *
from ..config.support import *
from ..components.sprites.sprites import Player, Phone
from ..components.elements.satiety import Satiety
from ..components.sprites.sprites import Background
from ..components.sprites.groups import AllSprites

class Game:
    _is_pygame_initialized_by_us = False

    def __init__(self):
        # 1. Initialisation Pygame & Écran (déjà corrigé)
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption(GAME_TITLE)
            
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000
        self.running = False

        # 2. Initialisation des éléments
        self.all_sprites = AllSprites()
        self.satiety_bar = Satiety()
        self.music = pygame.mixer.music.load(get_resource_path(join(AUDIO_DIR, "Max Brhon - AI [NCS Release].mp3")))
        
        # Background
        self.background = Background(self.all_sprites, self.screen) 

        # 3. Groupes de sprites et éléments
        self.player = Player(self.all_sprites)
        self.phone = Phone(self.all_sprites)


    def _handle_events(self):
        """
        Gère les événements Pygame (clavier, souris, etc.).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                # Quitte pygame et le système si ce module l'a initialisé
                if Game._is_pygame_initialized_by_us:
                    pygame.quit()
                sys.exit()  # Quitte l'application

            elif event.type == pygame.KEYDOWN:
                # La gestion continue du mouvement est faite dans _update_game_state avec pygame.key.get_pressed()
                pass

    def _update_game_state(self):
        """
        Met à jour la logique du jeu (mouvement, collisions, satiété).
        """
        self.all_sprites.update(self.dt)
        # Diminution de la satiété
        self.satiety_bar.decrease()

        # Vérification des collisions
        # rect.colliderect est suffisant si nous n'avons qu'un joueur et un téléphone
        if self.player.rect.colliderect(self.phone.rect):
            self.satiety_bar.increase()
            self.phone.reset_position()  # Réinitialise la position du téléphone après la collecte

        # Vérification de la condition de fin de jeu
        if self.satiety_bar.is_empty():
            self.running = False  # Arrête la boucle de jeu

        # Mise à jour de l'arrière-plan animé

    def _draw_elements(self):
        """
        Dessine tous les éléments du jeu sur l'écran.
        """
        # Dessine l'arrière-plan en premier
        # Dessine le joueur et le téléphone
        self.all_sprites.draw()

        # Dessine la barre de satiété
        self.satiety_bar.draw(self.screen)

    def run(self):
        pygame.mixer.music.play(-1)
        # except pygame.error as e:
        #     print(f"Echec du chargment de la musique : {e}")
        """
        Démarre et gère la boucle de jeu principale.
        Retourne True si le jeu doit être relancé, False sinon.
        """
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Quitte pygame et le système si ce module l'a initialisé
                if Game._is_pygame_initialized_by_us:
                    pygame.quit()
                    sys.exit()  # Quitte l'application
                elif event.type == pygame.KEYDOWN:
                    pass
                
            self._update_game_state()
            self._draw_elements()

            pygame.display.flip()
            self.clock.tick(FPS)

        # Si la boucle se termine (satiété à zéro ou quit), retourne l'état de fin
        if self.satiety_bar.is_empty():
            return "game_over"  # Indique à main.py que c'est un game over

        # Si on a quitté le jeu via la croix
        return "quit"

# --- Bloc de test pour l'exécution indépendante (optionnel) ---
if __name__ == "__main__":
    game_instance = Game()
    result = game_instance.run()
    if result == "game_over":
        print("Game Over! Satiété à zéro.")
    elif result == "quit":
        print("Jeu quitté par l'utilisateur.")
    pygame.quit()  # S'assure que Pygame est quitté après le test