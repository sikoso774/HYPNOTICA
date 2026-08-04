import os

import pygame as pg

from ..config.settings import *

HYPNOSIS_FOLDER_NAME = "hypnose_frames"


class AnimationGif:
    """Loads a folder of image frames and cycles through them like a GIF."""

    def __init__(self, folder_path, screen):
        self.screen = screen
        self.folder_path = folder_path
        self.frames = self.loader_gif_images(folder_path)
        self.frame_counter = 0
        self.animation_frame = 0
        self.animation_speed = 2 # Number of ticks before switching frame

    def loader_gif_images(self, folder_path):
        """
        Loads all images from a given folder (the GIF frames).
        """
        frames = []

        # walk traverses the folders and files
        for root, _, files in os.walk(self.folder_path):
            sorted_files = sorted(files)

            for file_name in sorted_files:
                if file_name.endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        # Full path to the image
                        full_path = join(root, file_name)

                        # Load and convert the image (optimization for Pygame)
                        img = pg.image.load(full_path).convert()

                        # Resize the image to the screen size if needed
                        img = pg.transform.scale(img, (self.screen.get_width(), self.screen.get_height()))

                        frames.append(img)
                    except pg.error as e:
                        print(f"Error loading GIF frame '{file_name}': {e}")

            # If the folder is empty, this list will be empty, which causes the KeyError
            if not frames:
                print(f"WARNING: No image found in the GIF folder: {folder_path}")
                # Create a fallback black surface to avoid crashing
                placeholder = pg.Surface((self.screen.get_width(), self.screen.get_height()))
                placeholder.fill(COLORS['black'])
                frames.append(placeholder)

            return frames

    def animate(self):
        """
        Updates the frame index to display based on the configured speed.
        """
        # 1. Increment the game's frame counter
        self.frame_counter += 1

        # 2. Check whether enough time has passed to switch GIF frame
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0

            # Avoid KeyError by ensuring there are frames to animate
            self.animation_frame += 1
            self.animation_frame %= len(self.frames)