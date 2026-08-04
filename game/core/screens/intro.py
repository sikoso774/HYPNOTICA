import pygame as pg
from os.path import join
from game.config import *
from .base_screen import BaseScreen


class Intro(BaseScreen):
    """Splash-screen intro sequence: fades through a set of images before the main menu."""

    def __init__(self, game):
        super().__init__(game)
        self.music_name = 'intro' # Will be started automatically by BaseScreen.run()

        # Duration configuration
        self.DURATION = 3000      # Time per image
        self.FADE_DURATION = 1000
        self.ALPHA_SPEED = 255 / self.FADE_DURATION

        # Texts
        self.text_logo = "HYPNOTICA"
        self.text_dev = "Sikoso774"
        self._init_fonts()

        # Loading images
        images_data = [
            ("Zoléni_Cyberpunk.jpg", (0.5, 0.5)),
            ("PP_Sikoso_77.jpg", (0.5, 0.5)),
            ("pygame_logo.png", (0.8, 0.8))
        ]
        self.images = []
        self._load_images(images_data)

        # Sequence state management
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

                # Proportional resizing
                target_w = int(WIDTH * fx)
                target_h = int(HEIGHT * fy)
                img_w, img_h = img.get_size()
                ratio = min(target_w / img_w, target_h / img_h)
                new_size = (int(img_w * ratio), int(img_h * ratio))

                img = pg.transform.scale(img, new_size)
                self.images.append(img)
            except Exception as e:
                print(f"Error loading intro image {filename}: {e}")

    def run(self):
        """Overrides run to initialize the timer on start."""
        self.phase_start_time = pg.time.get_ticks()
        self.image_index = 0
        # Calls the parent's run, which handles the main loop
        return super().run()

    def on_event(self, event):
        # Allows skipping the intro with Space or Escape
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                self.sound.play_sfx('confirm')
                return "menu"
        return None

    def update(self):
        """Handles the intro's timing logic."""
        current_time = pg.time.get_ticks()
        elapsed = current_time - self.phase_start_time

        # If the current image's time has elapsed
        if elapsed >= self.DURATION:
            self.image_index += 1
            if self.image_index >= len(self.images):
                # End of sequence -> force the BaseScreen loop to end
                # Trick: BaseScreen.run() loops on self.running.
                # But BaseScreen has no built-in automatic return without an event.
                # We could tweak BaseScreen slightly or use a trick here.
                # Cleanest approach: simulate a return action.
                return "menu"

            # Reset for the next image
            self.phase_start_time = current_time

    def draw(self):
        # Careful: if update() detected the end, image_index can be out of bounds
        # for one frame before run() returns. Safety check:
        if self.image_index >= len(self.images):
            return

        self.screen.fill(COLORS['black'])

        current_img = self.images[self.image_index]
        elapsed = pg.time.get_ticks() - self.phase_start_time

        # 1. Image Alpha Calculation (Fade In / Static / Fade Out)
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

        # 2. Logo Text (delayed Fade In)
        alpha_txt1 = 0
        if elapsed > self.DURATION / 3:
            alpha_txt1 = int((elapsed - self.DURATION / 3) * self.ALPHA_SPEED)
            alpha_txt1 = max(0, min(255, alpha_txt1))

        surf_logo = self.font_logo.render(self.text_logo, True, COLORS['white'])
        surf_logo.set_alpha(alpha_txt1)
        rect_logo = surf_logo.get_rect(center=(WIDTH // 2, HEIGHT // 6))
        self.screen.blit(surf_logo, rect_logo)

        # 3. Dev Text (even more delayed Fade In)
        alpha_txt2 = 0
        if elapsed > 2 * self.DURATION / 3:
            alpha_txt2 = int((elapsed - 2 * self.DURATION / 3) * self.ALPHA_SPEED)
            alpha_txt2 = max(0, min(255, alpha_txt2))

        surf_dev = self.font_dev.render(self.text_dev, True, COLORS['white'])
        surf_dev.set_alpha(alpha_txt2)
        rect_dev = surf_dev.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.screen.blit(surf_dev, rect_dev)