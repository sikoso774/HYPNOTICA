from ..constants.credits_const import *
from ..config.support import *
from ..config.settings import *
from .base_screen import BaseScreen

class Credits(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'credits'
        
        self.credit_data = CREDITS_CONTENT
        self.scrolling_speed = 1.5
        
        # Préparation du contenu (texte et images)
        self.prepare_credits = self._prepare_credits()
        
        # Calcul de la hauteur totale pour le scrolling
        _, self.screen_h = self.screen.get_size()
        self.total_height = sum(item['height'] for item in self.prepare_credits) + self.screen_h * 0.1
        
        # Position de départ (en bas de l'écran)
        self.credits_y = self.screen_h

    def _load_images(self) -> dict:
        # (Gardez votre méthode _load_images existante telle quelle)
        # ... [Code original _load_images] ...
        # Pour gagner de la place ici, je ne la réécris pas, mais copiez-la depuis votre fichier original.
        loaded_images = {}
        for item in CREDITS_CONTENT:
            if item['type'] == 'image' and 'image_path' in item:
                try:
                    img = pygame.image.load(item['image_path']).convert_alpha()
                    scaled_width = int(WINDOW_WIDTH * item.get('image_scale_factor', 1))
                    scaled_height = int(WINDOW_HEIGHT * item.get('image_scale_factor', 1))
                    img = pygame.transform.scale(img, (scaled_width, scaled_height))
                    loaded_images[item['value']] = img
                except pygame.error:
                    loaded_images[item['value']] = pygame.Surface((1, 1))
        return loaded_images

    def _prepare_credits(self):
        # (Gardez aussi votre méthode _prepare_credits existante)
        # ... [Code original _prepare_credits] ...
        # Juste une correction : utilisez self.screen pour récupérer la largeur si besoin
        prepared_list = []
        loaded_images = self._load_images()
        font_path = get_resource_path(DEFAULT_FONT_NAME)
        
        for item in self.credit_data:
            prepared_item = {'type': item['type']}
            if item['type'] == 'text':
                font_size = item.get('font_size', 36)
                current_font = pygame.font.Font(font_path, font_size)
                text_surf = current_font.render(item['value'], True, item.get('color', COLORS['white']))
                prepared_item['surface'] = text_surf
                prepared_item['height'] = text_surf.get_height() * 1.5
            elif item['type'] == 'image':
                image = loaded_images.get(item['value'])
                if image:
                    prepared_item['surface'] = image
                    prepared_item['height'] = image.get_height() + 20
                else:
                    prepared_item['surface'] = pygame.Surface((1, 1))
                    prepared_item['height'] = 0
            elif item['type'] == 'spacer':
                prepared_item['height'] = item.get('height', 0)
            
            prepared_list.append(prepared_item)
        return prepared_list

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                self.sound.stop_music()
                return "menu"
            elif event.key == pygame.K_q:
                self.quit_game()
        return None

    def update(self):
        # Logique de défilement
        self.credits_y -= self.scrolling_speed
        if self.credits_y < -self.total_height:
            self.credits_y = self.screen_h  # Reset pour boucler

    def draw(self):
        self.screen.fill(COLORS['black'])
        y_offset = self.credits_y
        
        for item in self.prepare_credits:
            center_x = self.screen.get_width() // 2
            
            if item['type'] == 'text':
                text_surf = item['surface']
                text_rect = text_surf.get_rect(center=(center_x, y_offset))
                self.screen.blit(text_surf, text_rect)
                y_offset += item['height']
                
            elif item['type'] == 'image':
                image = item['surface']
                # Centrage vertical ajusté
                image_rect = image.get_rect(center=(center_x, y_offset + image.get_height() // 2))
                self.screen.blit(image, image_rect)
                y_offset += item['height']
                
            elif item['type'] == 'spacer':
                y_offset += item['height']
