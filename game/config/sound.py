import pygame as pg
from os.path import join
from game.config import get_resource_path

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        
        # Définition des chemins de base
        self.audio_dir = get_resource_path(join("assets", "audio"))
        self.sfx_dir = get_resource_path(join("assets", "audio", "sounds"))

        # Dictionnaire des musiques
        self.music_tracks = {
            'intro': "Max Brhon - AI [NCS Release].mp3",
            'menu': "Max Brhon - AI [NCS Release].mp3",
            'game_over': "More Plastic - Rewind [NCS Release].mp3",
            'credits': "waera - harinezumi [NCS Release].mp3",
            'game': "DEAF KEV - Invincible [NCS Release].mp3"
            # Ajoutez d'autres pistes ici si nécessaire
        }
        
        # Chargement des effets sonores (SFX)
        self.sfx = {}
        self._load_sfx()

        self.current_track = None

    def _load_sfx(self):
        """Charge les effets sonores en mémoire."""
        sfx_files = {
            'click': "hover_click.wav",
            'confirm': "yes_clicked.wav"
            # Ajoutez vos bruitages ici (tir, saut, etc.)
        }
        
        for name, filename in sfx_files.items():
            path = join(self.sfx_dir, filename)
            try:
                self.sfx[name] = pg.mixer.Sound(path)
                self.sfx[name].set_volume(0.4)
            except FileNotFoundError:
                print(f"Attention: SFX introuvable -> {path}")

    def play_music(self, track_key):
        """
        Lance une musique. 
        Si la musique demandée joue déjà, on ne fait rien (transition fluide).
        """
        if track_key not in self.music_tracks:
            print(f"Erreur: Piste musicale inconnue '{track_key}'")
            return

        # Si la même piste est déjà en cours (ex: intro -> menu), on la laisse jouer.
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
            print(f"Erreur chargement musique ({full_path}): {e}")

    def stop_music(self):
        pg.mixer.music.stop()

    def play_sfx(self, name):
        if name in self.sfx:
            self.sfx[name].play()