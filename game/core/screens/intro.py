import pygame as pg
from os.path import join
from game.config import *
from .base_screen import BaseScreen

class Intro(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'intro' # Sera lancé automatiquement par BaseScreen.run()

        # Configuration des durées
        self.DURATION = 3000      # Temps par image
        self.FADE_DURATION = 1000 
        self.ALPHA_SPEED = 255 / self.FADE_DURATION
        
        # Textes
        self.text_logo = "HYPNOTICA"
        self.text_dev = "Sikoso774"
        self._init_fonts()
        
        # Chargement des images
        images_data = [
            ("Zoléni_Cyberpunk.jpg", (0.5, 0.5)),
            ("PP_Sikoso_77.jpg", (0.5, 0.5)),
            ("pygame_logo.png", (0.8, 0.8))
        ]
        self.images = []
        self._load_images(images_data)

        # Gestion de l'état de la séquence
        self.image_index = 0
        self.phase_start_time = 0
        self.sequence_finished = False

    def _init_fonts(self):
        self.font_logo = get_font(DEFAULT_FONT_NAME, 48)
        self.font_dev = get_font(DEFAULT_FONT_NAME, 36)

    def _load_images(self, data):
        for filename, (fx, fy) in data:
            try:
                path = get_resource_path(join("assets", "images", filename))
                img = pg.image.load(path).convert_alpha()
                
                # Redimensionnement proportionnel
                target_w = int(WIDTH * fx)
                target_h = int(HEIGHT * fy)
                img_w, img_h = img.get_size()
                ratio = min(target_w / img_w, target_h / img_h)
                new_size = (int(img_w * ratio), int(img_h * ratio))
                
                img = pg.transform.scale(img, new_size)
                self.images.append(img)
            except Exception as e:
                print(f"Erreur chargement image intro {filename}: {e}")

    def run(self):
        """Surcharge de run pour initialiser le timer au démarrage."""
        self.phase_start_time = pg.time.get_ticks()
        self.image_index = 0
        # On appelle le run du parent qui gère la boucle principale
        return super().run()

    def on_event(self, event):
        # Permet de passer l'intro avec Espace ou echap
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                self.sound.play_sfx('confirm')
                return "menu"
        return None

    def update(self):
        """Gère la logique temporelle de l'intro."""
        current_time = pg.time.get_ticks()
        elapsed = current_time - self.phase_start_time

        # Si le temps de l'image actuelle est écoulé
        if elapsed >= self.DURATION:
            self.image_index += 1
            if self.image_index >= len(self.images):
                # Fin de la séquence -> on force la fin de la boucle du BaseScreen
                # Astuce: BaseScreen.run() boucle sur self.running.
                # Mais BaseScreen n'a pas prévu de retour automatique sans event.
                # On va modifier légèrement BaseScreen ou utiliser une astuce ici.
                # Le plus propre : simuler une action de retour.
                return "menu" 
            
            # Reset pour la prochaine image
            self.phase_start_time = current_time

    def draw(self):
        # Attention : si update() a détecté la fin, image_index peut être hors limite 
        # le temps d'une frame avant que run() ne retourne. Sécurité :
        if self.image_index >= len(self.images):
            return

        self.screen.fill(COLORS['black'])
        
        current_img = self.images[self.image_index]
        elapsed = pg.time.get_ticks() - self.phase_start_time
        
        # 1. Calcul Alpha Image (Fade In / Static / Fade Out)
        alpha_img = 255
        if elapsed < self.DURATION / 3: # Fade In
            alpha_img = int(elapsed * self.ALPHA_SPEED)
        elif elapsed > 2 * self.DURATION / 3: # Fade Out
            alpha_img = 255 - int((elapsed - 2 * self.DURATION / 3) * self.ALPHA_SPEED)
        alpha_img = max(0, min(255, alpha_img))

        temp_img = current_img.copy()
        temp_img.set_alpha(alpha_img)
        rect = temp_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(temp_img, rect)

        # 2. Texte Logo (Fade In retardé)
        alpha_txt1 = 0
        if elapsed > self.DURATION / 3:
            alpha_txt1 = int((elapsed - self.DURATION / 3) * self.ALPHA_SPEED)
            alpha_txt1 = max(0, min(255, alpha_txt1))
        
        surf_logo = self.font_logo.render(self.text_logo, True, COLORS['white'])
        surf_logo.set_alpha(alpha_txt1)
        rect_logo = surf_logo.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        self.screen.blit(surf_logo, rect_logo)

        # 3. Texte Dev (Fade In encore plus retardé)
        alpha_txt2 = 0
        if elapsed > 2 * self.DURATION / 3:
            alpha_txt2 = int((elapsed - 2 * self.DURATION / 3) * self.ALPHA_SPEED)
            alpha_txt2 = max(0, min(255, alpha_txt2))
            
        surf_dev = self.font_dev.render(self.text_dev, True, COLORS['white'])
        surf_dev.set_alpha(alpha_txt2)
        rect_dev = surf_dev.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.screen.blit(surf_dev, rect_dev)