import pygame as pg
from game.core.screens import BaseScreen
from game.config.settings import *
from game.raycasting_engine import *

class Level_3D(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'game'
        # Charge la police pour le Timer (utilise celle des settings ou celle par défaut)
        try:
            self.font = pg.font.Font(DEFAULT_FONT_NAME, 40)
        except:
            self.font = pg.font.Font(None, 40)
        self.reset()

    def reset(self):
        """Réinitialise le niveau et le Timer."""
        
        # --- TIMER CONFIG ---
        self.time_left = 60.0  # Temps en secondes (ex: 60 secondes)
        
        self.map = Map(self.game)
        self.game.map = self.map
        
        self.player = Player(self.game)
        self.game.player = self.player
        
        self.raycaster = RayCasting(self.game)

    def update(self):
        fps = self.clock.get_fps()
        pg.display.set_caption(f'{GAME_TITLE} | FPS : {fps}')
        # Récupère le temps écoulé depuis la dernière frame (en millisecondes)
        dt_ms = self.clock.get_time()
        # On stocke dt en secondes pour les calculs de vitesse du joueur
        self.game.dt = dt_ms 

        # --- LOGIQUE TIMER ---
        # On soustrait le temps écoulé (converti en secondes)
        self.time_left -= dt_ms / 1000.0

        # Si le temps est écoulé, on déclenche le Game Over
        if self.time_left <= 0:
            self.time_left = 0 # Pour ne pas afficher de nombre négatif
            return "game_over" # Renvoie l'action au Game Controller

        # Mise à jour du reste du jeu
        self.player.update()
        self.raycaster.update()
        
        return None

    def draw(self):
        # 1. Fond et Raycasting
        self.screen.fill('black') 
        pg.draw.rect(self.screen, (30,30,30), (0, HEIGHT//2, WIDTH, HEIGHT//2))
        self.raycaster.update()

        # 2. Debug (Optionnel, à commenter pour le rendu final)
        # self.map.draw()
        # self.player.draw()

        # 3. INTERFACE UTILISATEUR (UI) - Le Timer
        # On formate le texte (ex: "TIME: 45.2")
        timer_text = f"TEMPS: {self.time_left:.1f}"
        
        # Changement de couleur : Rouge si < 10 secondes, sinon Blanc
        text_color = COLORS['red'] if self.time_left < 10 else COLORS['white']
        
        # Création de la surface texte
        text_surface = self.font.render(timer_text, True, text_color)
        
        # Positionnement en haut au centre
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
        
        # Affichage
        self.screen.blit(text_surface, text_rect)