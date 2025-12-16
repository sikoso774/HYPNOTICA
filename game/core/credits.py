from ..constants.credits_const import *
from ..config.support import *
from ..config.settings import *

class Credits:
    def __init__(self, game):
        # general setup
        self.game = game
        self.screen = self.game.screen
        self.credit_data = CREDITS_CONTENT
        self.loaded_images = self._load_images()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # scrolling setup
        self.prepare_credits = self._prepare_credits()
        self.scrolling_speed = 1.5
        self.credits_y, self.hauteur = self.screen.get_size()
        self.total_height = sum(item['height'] for item in self.prepare_credits) + self.hauteur * 0.1 # Ajout d'une marge de fin)
        
        # Musics
        self.music_path = get_resource_path(join(AUDIO_DIR, "waera - harinezumi [NCS Release].mp3"))
         
    def _load_images(self)-> dict:
        """
        Charge l'image de fond principale et la musique des crédits.
        Redimensionne l'image si nécessaire.
        Retourne (image_credits, music_path, loaded_font_cache).
        """
        loaded_images = {}
        # Charger l'image principale référencée dans CREDITS_CONTENT
        for item in CREDITS_CONTENT:
            if item['type'] == 'image' and 'image_path' in item:
                try:
                    img = pygame.image.load(item['image_path']).convert_alpha()
                    # Redimensionnement selon le facteur d'échelle défini dans les constantes
                    scaled_width = int(WINDOW_WIDTH * item.get('image_scale_factor', 1))
                    scaled_height = int(WINDOW_HEIGHT * item.get('image_scale_factor', 1))
                    img = pygame.transform.scale(img, (scaled_width, scaled_height))
                    loaded_images[item['value']] = img
                except pygame.error as e:
                    print(f"Erreur de chargement d'image pour les crédits ({item['image_path']}): {e}")
                    loaded_images[item['value']] = pygame.Surface((1, 1), pygame.SRCALPHA) # Image vide

        return loaded_images
    
    def scroll(self):
        self.credits_y -= self.scrolling_speed
        if self.credits_y < -self.total_height:
            self.credits_y = self.hauteur  # Réinitialiser pour boucler
    
    def _prepare_credits(self):
        """
        Prépare toutes les surfaces de texte et d'image une seule fois, 
        et calcule la hauteur exacte de chaque élément.
        """
        prepared_list = []
        loaded_images = self._load_images() # Réutiliser votre méthode de chargement d'images
        font_path = get_resource_path(DEFAULT_FONT_NAME)
        
        for item in self.credit_data: # credit_data est votre CREDITS_CONTENT
            prepared_item = {'type': item['type']}
            
            if item['type'] == 'text':
                font_size = item.get('font_size', 36)
                current_font = pygame.font.Font(font_path, font_size)
                
                text_surf = current_font.render(item['value'], True, item.get('color', COLORS['white']))
                
                prepared_item['surface'] = text_surf
                prepared_item['height'] = text_surf.get_height() * 1.5 # Hauteur du texte + espacement
                
            elif item['type'] == 'image':
                image = loaded_images.get(item['value'])
                if image:
                    prepared_item['surface'] = image
                    prepared_item['height'] = image.get_height() + 20 # Hauteur de l'image + espacement
                else:
                    # Gérer l'image manquante si nécessaire
                    prepared_item['surface'] = pygame.Surface((1, 1))
                    prepared_item['height'] = 0
                    
            elif item['type'] == 'spacer':
                height = item.get('height', 0)
                prepared_item['height'] = height
                
            prepared_list.append(prepared_item)
            
        return prepared_list
    
    def draw(self):
        self.screen.fill(COLORS['black'])
        y_offset = self.credits_y
        
        for item in self.prepare_credits:
            if item['type'] == 'text':
                text_surf = item['surface']
                text_rect = text_surf.get_rect(center=(self.screen.get_width() // 2, y_offset))
                self.screen.blit(text_surf, text_rect)
                y_offset += item['height'] # Utiliser la hauteur calculée
                
            elif item['type'] == 'image':
                image = item['surface']
                # Le point central doit être y_offset + moitié de la hauteur de l'image
                image_rect = image.get_frect(center=(self.screen.get_width() // 2, y_offset + image.get_height() // 2))
                self.screen.blit(image, image_rect)
                y_offset += item['height'] # Utiliser la hauteur calculée
                
            elif item['type'] == 'spacer':
                y_offset += item['height'] # Utiliser la hauteur calculée

    def run(self):
        self.credits_y = self.hauteur
        """
        Contient la boucle principale de l'écran de crédits.
        Gère les événements, le défilement et le dessin.
        Retourne 'menu' si l'utilisateur appuie sur 'M'.
        """
        try:
            # Assurez-vous de CHARGER la bonne piste
            pygame.mixer.music.load(self.music_path)
            # PUIS de la jouer
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erreur de lecture de la musique des crédits: {e}")
                
        while self.running:
            # 1. Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Arrêter la musique et quitter le jeu
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # Quitter le jeu avec la touche Q
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_m:
                        pygame.mixer.music.stop()
                            
                        return "menu" # Retourne un signal à la boucle principale du jeu

            # draw & scroll
            self.scroll()
            self.draw()
            # update
            pygame.display.update()
            
            self.clock.tick(FPS) 
            
        return None

# Test du défilement des crédits
if __name__ == "__main__":
    import sys
    import pygame
    sys.path.append('')
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Test des Crédits")
    clock = pygame.time.Clock()
    
    credits = Credits(screen)
    action = credits.run()
    print(f"Action retournée par les crédits: {action}")