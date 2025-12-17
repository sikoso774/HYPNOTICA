import pygame as pg
import random
from ...config.settings import *
from ...constants.gameplay_const import *
from .hypnose_gif import Animation_GIF, HYPNOSE_FOLDER_NAME

class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        
class Background(pg.sprite.Sprite):
    """
    Classe de gestion de l'arrière-plan animé comme un Sprite.
    """
    
    def __init__(self, groups, screen): 
        # 2. On initialise le parent (Sprite) et on s'ajoute aux groupes
        super().__init__(groups)
        self.screen = screen
        self._layer = 0 # IMPORTANT : On définit la couche (0 = fond, 1 = joueur)
        
        gif_folder_path = get_resource_path(join(IMAGES_DIR, HYPNOSE_FOLDER_NAME))
        self.gif_animator = Animation_GIF(gif_folder_path, screen)
        
        # 3. Initialisation des attributs OBLIGATOIRES pour un Sprite
        # On prend la première frame comme image de départ
        if self.gif_animator.frames:
            self.image = self.gif_animator.frames[0]
        else:
            self.image = pg.Surface((screen.get_width(), screen.get_height()))
            self.image.fill(COLORS['black'])
            
        self.rect = self.image.get_frect(topleft=(0, 0))
        
    def update(self, dt): # Accepte dt pour être compatible avec l'appel de groupe
        """
        Met à jour l'image du sprite avec la prochaine frame du GIF.
        """
        self.gif_animator.animate()
        
        # 4. On met à jour self.image pour que le draw() du groupe affiche la bonne frame
        current_frame_index = self.gif_animator.animation_frame
        if self.gif_animator.frames:
            self.image = self.gif_animator.frames[current_frame_index]
       
class Player(Sprite):
    def __init__(self, groups):
        # Nous devons fournir pos et surf, même si Player les met à jour juste après.
        # Utilisez des valeurs temporaires ou des constantes ici.
        TEMP_SURF = pg.Surface((PLAYER_SIZE, PLAYER_SIZE))
        TEMP_POS = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20)
        
        # Passer les arguments au constructeur de Sprite
        super().__init__(TEMP_POS, TEMP_SURF, groups) 
        self._layer = 1
        
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        
        # Le code suivant va écraser TEMP_SURF et TEMP_POS, ce qui est acceptable.
        self.image = self.paceholder(self.size) 
        self.rect  = self.image.get_frect(
            centerx=WINDOW_WIDTH / 2,
            bottom = WINDOW_HEIGHT - 20
        )
        self.direction = pygame.math.Vector2()

    # Si il n'y a pas de sprites...
    def paceholder(self, player_size):
        """
        Charge et redimensionne le sprite du joueur.
        Utilise un carré placeholder si PLAYER_SPRITE_PATH n'est pas défini.
        """
        if PLAYER_SPRITE_PATH:
            try:
                sprite = pg.image.load(PLAYER_SPRITE_PATH).convert_alpha()
                return pg.transform.scale(sprite, (player_size, player_size))
            except pg.error as e:
                print(f"Erreur de chargement du sprite joueur ({PLAYER_SPRITE_PATH}): {e}. Utilisation du placeholder.")
        # Placeholder: un carré bleu clair
        placeholder = pg.Surface((player_size, player_size), pg.SRCALPHA)
        placeholder.fill((50, 50, 200)) # Bleu un peu plus clair
        return placeholder
    
    def input(self, dt):
        keys = pg.key.get_pressed()
        self.direction.x = int(keys[pg.K_RIGHT]) - int(keys[pg.K_LEFT])  # <---- bcp plus simple
        self.direction.y = int(keys[pg.K_DOWN]) - int(keys[pg.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
    
    def update(self, dt):
        self.input(dt)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Phone(Sprite):
    def __init__(self, groups): # Prend le groupe comme Player
        
        # 1. Préparation des arguments pour le parent (Sprite)
        # On utilise des valeurs temporaires car Phone calcule sa vraie position plus tard
        temp_size = PHONE_SIZE
        temp_surf = self.load_phone_sprite(temp_size) # On utilise une méthode locale pour charger l'image
        temp_pos = (random.randint(0, WINDOW_WIDTH - temp_size), 0)

        # 2. Appel au constructeur de la classe parente (Sprite)
        super().__init__(temp_pos, temp_surf, groups)
        
        self._layer = 1
        self.size = temp_size
        self.speed = 200
        self.image = temp_surf
        # self.rect est déjà initialisé par Sprite.__init__
        
        # 3. Finalisation de la position initiale (écraser le temp_pos)
        self.reset_position()

    # NOTE : La méthode load_phone_sprite doit être dans la classe (méthode statique ou dans l'instance)
    # Puisque vous l'aviez dans un autre fichier, nous l'intégrons ici (ou dans un SpriteManager si vous changez d'avis)
    def load_phone_sprite(self, phone_size):
        """
        Charge et redimensionne le sprite du téléphone.
        Utilise un cercle placeholder si PHONE_SPRITE_PATH n'est pas défini.
        """
        if PHONE_SPRITE_PATH:
            try:
                sprite = pg.image.load(PHONE_SPRITE_PATH).convert_alpha()
                return pg.transform.scale(sprite, (phone_size, phone_size))
            except pg.error as e:
                print(f"Erreur de chargement du sprite téléphone ({PHONE_SPRITE_PATH}): {e}. Utilisation du placeholder.")
        # Placeholder: un cercle vert
        placeholder = pg.Surface((phone_size, phone_size), pg.SRCALPHA)
        pg.draw.circle(placeholder, (0, 200, 0), (phone_size // 2, phone_size // 2), phone_size // 2)
        return placeholder

    def reset_position(self):
        """
        Réinitialise la position du téléphone en haut de l'écran à une position X aléatoire.
        """
        # Utilisation de self.rect qui vient du parent
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.size)
        self.rect.y = 0  # Commence en haut de l'écran

    def update(self, dt): # Prend dt pour être cohérent avec Player, même si non utilisé ici
        """
        Met à jour la position du téléphone (le fait tomber).
        """
        self.rect.y += self.speed * dt

        # Si le téléphone sort de l'écran, le réinitialise
        if self.rect.top > WINDOW_HEIGHT:
            self.reset_position()
        
    def draw(self, surface):
        """
        Dessine le téléphone sur la surface donnée.
        """
        surface.blit(self.image, self.rect)

