import pygame as pg
from game.components import CREDITS_CONTENT
from game.config import *
from .base_screen import BaseScreen

class Credits(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'credits'
        
        self.credit_data = CREDITS_CONTENT
        self.scrolling_speed = 1.5
        
        # Préparation du contenu
        self.prepare_credits = self._prepare_credits()
        
        # Calcul de la hauteur
        _, self.screen_h = self.screen.get_size()
        self.total_height = sum(item['height'] for item in self.prepare_credits) + self.screen_h * 0.1
        
        # Initialisation de la variable (sera reset dans run)
        self.credits_y = self.screen_h

    # --- AJOUTEZ CETTE MÉTHODE ICI ---
    def run(self):
        """
        Surcharge de run() : 
        On remet le texte en bas de l'écran avant de lancer la boucle.
        """
        self.credits_y = self.screen_h  # RESET : Retour au départ
        return super().run()            # Lancement standard (boucle + musique)
    # ---------------------------------

    # ... Le reste des méthodes (_load_images, _prepare_credits, on_event, update, draw) reste identique ...
    def _load_images(self) -> dict:
        # [Votre code existant...]
        loaded_images = {}
        for item in CREDITS_CONTENT:
            if item['type'] == 'image' and 'image_path' in item:
                try:
                    img = pg.image.load(item['image_path']).convert_alpha()
                    scaled_width = int(WIDTH * item.get('image_scale_factor', 1))
                    scaled_height = int(HEIGHT * item.get('image_scale_factor', 1))
                    img = pg.transform.scale(img, (scaled_width, scaled_height))
                    loaded_images[item['value']] = img
                except pg.error:
                    loaded_images[item['value']] = pg.Surface((1, 1))
        return loaded_images

    def _prepare_credits(self):
        # [Votre code existant...]
        prepared_list = []
        loaded_images = self._load_images()
        font_path = get_resource_path(DEFAULT_FONT_NAME) # Assurez-vous d'utiliser get_resource_path
        
        for item in self.credit_data:
            # ... (Copiez le contenu de votre fonction existante) ...
            prepared_item = {'type': item['type']}
            if item['type'] == 'text':
                font_size = item.get('font_size', 36)
                try:
                    current_font = pg.font.Font(font_path, font_size)
                except:
                    current_font = pg.font.Font(None, font_size)

                text_surf = current_font.render(item['value'], True, item.get('color', COLORS['white']))
                prepared_item['surface'] = text_surf
                prepared_item['height'] = text_surf.get_height() * 1.5
            elif item['type'] == 'image':
                image = loaded_images.get(item['value'])
                if image:
                    prepared_item['surface'] = image
                    prepared_item['height'] = image.get_height() + 20
                else:
                    prepared_item['surface'] = pg.Surface((1, 1))
                    prepared_item['height'] = 0
            elif item['type'] == 'spacer':
                prepared_item['height'] = item.get('height', 0)
            
            prepared_list.append(prepared_item)
        return prepared_list

    def on_event(self, event):
        if event.type == pg.KEYDOWN:
            # Touche M ou ESC pour revenir au menu
            if event.key == pg.K_m or event.key == pg.K_ESCAPE:
                self.sound.play_sfx('click')
                return "menu"
            elif event.key == pg.K_q:
                self.quit_game()
        return None

    def update(self):
        self.credits_y -= self.scrolling_speed
        # Si tout est passé, on peut soit boucler, soit revenir au menu automatiquement
        if self.credits_y < -self.total_height:
             # Option A : Boucle infinie
             self.credits_y = self.screen_h 
             
             # Option B : Retour automatique au menu (décommentez ci-dessous)
             # return "menu"

    def draw(self):
        self.screen.fill(COLORS['black'])
        y_offset = self.credits_y
        
        center_x = self.screen.get_width() // 2
        
        for item in self.prepare_credits:
            if item['type'] == 'text':
                text_surf = item['surface']
                text_rect = text_surf.get_rect(center=(center_x, y_offset))
                self.screen.blit(text_surf, text_rect)
                y_offset += item['height']
                
            elif item['type'] == 'image':
                image = item['surface']
                image_rect = image.get_rect(center=(center_x, y_offset + image.get_height() // 2))
                self.screen.blit(image, image_rect)
                y_offset += item['height']
                
            elif item['type'] == 'spacer':
                y_offset += item['height']