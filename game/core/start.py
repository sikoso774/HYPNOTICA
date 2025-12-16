import pygame
import sys
from os.path import join
from ..config.settings import *
from ..config.support import get_resource_path

class SplashScreen:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.clock = pygame.time.Clock()

        self.DURATION = 3000 
        self.FADE_DURATION = 1000 
        self.ALPHA_SPEED = 255 / self.FADE_DURATION
        
        self.text_logo = "HYPNOTICA"
        self.text_dev = "Sikoso774"
        
        # Ressources
        font_path = get_resource_path(join("assets", "fonts", "MINDCONTROL.ttf"))
        try:
            self.font_logo = pygame.font.Font(font_path, 48)
            self.font_dev = pygame.font.Font(font_path, 36)
        except Exception:
            self.font_logo = pygame.font.Font(None, 48)
            self.font_dev = pygame.font.Font(None, 36)

        self.music_path = get_resource_path(join("assets", "audio", "Max Brhon - AI [NCS Release].mp3"))

        images_data = [
            ("Zoléni_Cyberpunk.jpg", (0.5, 0.5)),
            ("PP_Sikoso_77.jpg", (0.5, 0.5)),
            ("pygame_logo.png", (0.8, 0.8))
        ]
        self.images = []
        self._load_images(images_data)

    def _load_images(self, data):
        for filename, (fx, fy) in data:
            try:
                path = get_resource_path(join("assets", "images", filename))
                img = pygame.image.load(path).convert_alpha()
                target_w = int(WINDOW_WIDTH * fx)
                target_h = int(WINDOW_HEIGHT * fy)
                img_w, img_h = img.get_size()
                ratio = min(target_w / img_w, target_h / img_h)
                new_size = (int(img_w * ratio), int(img_h * ratio))
                img = pygame.transform.scale(img, new_size)
                self.images.append(img)
            except Exception as e:
                print(f"Erreur chargement image intro {filename}: {e}")

    def _draw_frame(self, image, current_time):
        self.screen.fill(COLORS['black'])
        
        alpha_img = 255
        if current_time < self.DURATION / 3:
            alpha_img = int(current_time * self.ALPHA_SPEED)
        elif current_time > 2 * self.DURATION / 3:
            alpha_img = 255 - int((current_time - 2 * self.DURATION / 3) * self.ALPHA_SPEED)
        alpha_img = max(0, min(255, alpha_img))

        temp_img = image.copy()
        temp_img.set_alpha(alpha_img)
        rect = temp_img.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(temp_img, rect)

        alpha_txt1 = 0
        if current_time > self.DURATION / 3:
            alpha_txt1 = int((current_time - self.DURATION / 3) * self.ALPHA_SPEED)
            alpha_txt1 = max(0, min(255, alpha_txt1))
        
        surf_logo = self.font_logo.render(self.text_logo, True, COLORS['white'])
        surf_logo.set_alpha(alpha_txt1)
        rect_logo = surf_logo.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6))
        self.screen.blit(surf_logo, rect_logo)

        alpha_txt2 = 0
        if current_time > 2 * self.DURATION / 3:
            alpha_txt2 = int((current_time - 2 * self.DURATION / 3) * self.ALPHA_SPEED)
            alpha_txt2 = max(0, min(255, alpha_txt2))
            
        surf_dev = self.font_dev.render(self.text_dev, True, COLORS['white'])
        surf_dev.set_alpha(alpha_txt2)
        rect_dev = surf_dev.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        self.screen.blit(surf_dev, rect_dev)

    def run(self):
        # Lancer la musique si elle ne joue pas déjà
        try:
            if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erreur musique intro: {e}")

        for image in self.images:
            start_time = pygame.time.get_ticks()
            running_phase = True
            while running_phase:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # CORRECTION : On N'ARRÊTE PAS la musique ici
                        return "menu"

                current_time = pygame.time.get_ticks() - start_time
                if current_time >= self.DURATION:
                    running_phase = False 
                else:
                    self._draw_frame(image, current_time)
                    pygame.display.flip()
                    self.clock.tick(FPS)

        # CORRECTION : On N'ARRÊTE PAS la musique à la fin
        return "menu"