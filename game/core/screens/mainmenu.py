import pygame as pg
from game.config.utils import display_text_center as center_text
from game.config.settings import *
from game.components import *
from .base_screen import BaseScreen  # Import de la classe mère

class MainMenu(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'menu'  # Référence à la clé dans SoundHandler
        
        # 1. Assets (GIF)
        GIF_PATH = get_resource_path(join(IMAGES_DIR, "hypnose_frames"))
        self.gif_animator = Animation_GIF(GIF_PATH, self.screen)
        
        # 2. Boutons
        self.buttons = []
        # On centre les boutons par rapport à la largeur de l'écran
        center_x = self.screen.get_width() // 2 - BUTTON_WITDH // 2
        
        for bouton_data in BUTTONS_MENU:
            self.buttons.append(
                Button(center_x, bouton_data['y_offset'], BUTTON_WITDH, BUTTON_HEIGHT, 
                       bouton_data['text'], bouton_data['action'])
            )

    def on_event(self, event):
        # Gestion des clics sur les boutons
        for button in self.buttons:
            action = button.manage_event(event)
            if action:
                self.sound.play_sfx('click') # Petit bonus : son de clic !
                return action
        
        # Raccourci clavier (Q pour quitter)
        if event.type == pg.KEYDOWN and event.key == pg.K_q:
            self.quit_game()
            
        return None

    def update(self):
        # Mise à jour de l'animation GIF à chaque frame
        self.gif_animator.animate()

    def draw(self):
        # 1. Fond (GIF)
        frame_index = self.gif_animator.animation_frame
        self.screen.blit(self.gif_animator.frames[frame_index], (0, 0))
        
        # 2. Textes
        center_text(self.screen, "HYPNOTICA", COLORS['white'], self.screen.get_height() // 4,
                    font_path=get_resource_path(DEFAULT_FONT_NAME))
        center_text(self.screen, "Zoléni KOKOLO ZASSI - 2025", COLORS['white'], 
                    self.screen.get_height() // 4 + 50, font_size=28)
        
        # 3. Boutons
        for button in self.buttons:
            button.draw(self.screen, self.gif_animator.frames[frame_index])