# Fichier: game/core/base_screen.py
import pygame
import sys
from ..config.settings import *

class BaseScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen  # Accès direct à l'écran via l'objet Game
        self.sound = game.sound    # Accès au gestionnaire de son
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        """Gestionnaire d'événements de base."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            # Hook pour les classes enfants (ex: appuie sur une touche)
            action = self.on_event(event)
            if action:
                return action
        return None

    def on_event(self, event):
        """À surcharger par les enfants pour gérer les inputs spécifiques."""
        return None

    def update(self):
        """Logique de mise à jour (animations, scroll, etc)."""
        pass

    def draw(self):
        """Dessin à l'écran."""
        pass

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        if hasattr(self, 'music_name') and self.music_name:
            self.sound.play_music(self.music_name)

        self.running = True
        while self.running:
            # 1. Events
            action = self.handle_events()
            if action: return action

            # 2. Update : Modifié pour capturer un retour (ex: fin d'intro)
            update_action = self.update()
            if update_action: return update_action # Si update renvoie "menu", on sort !

            # 3. Draw
            self.draw()
            
            # 4. Flip
            pygame.display.flip()
            self.clock.tick(FPS)