import pygame as pg
from os.path import join
from game.config import get_resource_path


class Sound:
    """Manages music playback and sound effects for the game."""

    def __init__(self, game):
        self.game = game
        pg.mixer.init()

        # Base path definitions
        self.audio_dir = get_resource_path(join("assets", "audio"))
        self.sfx_dir = get_resource_path(join("assets", "audio", "sounds"))

        # Music track dictionary
        self.music_tracks = {
            'intro': "Max Brhon - AI [NCS Release].mp3",
            'menu': "Max Brhon - AI [NCS Release].mp3",
            'game_over': "More Plastic - Rewind [NCS Release].mp3",
            'credits': "waera - harinezumi [NCS Release].mp3",
            'game': "DEAF KEV - Invincible [NCS Release].mp3"
            # Add other tracks here if needed
        }

        # Loading sound effects (SFX)
        self.sfx = {}
        self._load_sfx()

        self.current_track = None

    def _load_sfx(self):
        """Loads sound effects into memory."""
        sfx_files = {
            'click': "hover_click.wav",
            'confirm': "yes_clicked.wav"
            # Add your sound effects here (shot, jump, etc.)
        }

        for name, filename in sfx_files.items():
            path = join(self.sfx_dir, filename)
            try:
                self.sfx[name] = pg.mixer.Sound(path)
                self.sfx[name].set_volume(0.4)
            except FileNotFoundError:
                print(f"Warning: SFX not found -> {path}")

    def play_music(self, track_key):
        """
        Starts playing a music track.
        If the requested track is already playing, does nothing (smooth transition).
        """
        if track_key not in self.music_tracks:
            print(f"Error: Unknown music track '{track_key}'")
            return

        # If the same track is already playing (e.g. intro -> menu), let it continue.
        if track_key == self.current_track and pg.mixer.music.get_busy():
            return

        filename = self.music_tracks[track_key]
        full_path = join(self.audio_dir, filename)

        try:
            pg.mixer.music.load(full_path)
            pg.mixer.music.play(-1)
            pg.mixer.music.set_volume(0.5)
            self.current_track = track_key
        except pg.error as e:
            print(f"Error loading music ({full_path}): {e}")

    def stop_music(self):
        pg.mixer.music.stop()

    def play_sfx(self, name):
        if name in self.sfx:
            self.sfx[name].play()