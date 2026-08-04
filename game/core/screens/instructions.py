import pygame as pg
from game.config import *
from .base_screen import BaseScreen

# Contenu des instructions
INSTRUCTIONS_CONTENT = [
    {'type': 'text', 'value': "Welcome to HYPNOTICA", 'font-size': 50, 'color': COLORS['white']},
    {'type': 'spacer', 'height': 50},
    {'type': 'text', 'value': "Objective : Keep the player satiated", 'font-size': 35, 'color': COLORS['white']},
    {'type': 'text', 'value': "by collecting phones.", 'font-size': 35, 'color': COLORS['white']},
    {'type': 'spacer', 'height': 50},
    {'type': 'text', 'value': "Use the LEFT and RIGHT", 'font-size': 35, 'color': COLORS['white']},
    {'type': 'text', 'value': "to", 'font-size': 35, 'color': COLORS['white']},
    {'type': 'text', 'value': "move the player", 'font-size': 35},
    {'type': 'spacer', 'height': 50},
    {'type': 'text', 'value': "Press SPACE to return to the main menu.", 'font-size': 25, 'color': COLORS['white']},
]

class Instructions(BaseScreen):
    def __init__(self, game):
        super().__init__(game)        
        self.instruction_data = INSTRUCTIONS_CONTENT
        
        # Variables animation
        self.current_char_index = 0
        self.last_char_time = 0
        self.typing_speed = 30 
        self.total_chars = 0
        
        self.prepared_items = []
        self._prepare_content()
        
        # Reset pour l'animation au démarrage
        self.last_char_time = pg.time.get_ticks()

    def _prepare_content(self):
        # (Même logique que votre code original, adaptée légèrement)
        current_y = HEIGHT // 6
        self.total_chars = 0

        for item in self.instruction_data:
            if item['type'] == 'text':
                size = item.get('font-size', 30)
                font = get_font(DEFAULT_FONT_NAME, size)

                self.prepared_items.append({
                    'type': 'text',
                    'full_text': item['value'],
                    'font': font,
                    'color': item.get('color', COLORS['white']),
                    'y': current_y,
                    'start_index': self.total_chars,
                    'length': len(item['value'])
                })
                self.total_chars += len(item['value'])
                current_y += font.get_height() + 10 
            elif item['type'] == 'spacer':
                current_y += item.get('height', 20)

    def on_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                # Si l'animation n'est pas finie, on l'accélère
                if self.current_char_index < self.total_chars:
                    self.current_char_index = self.total_chars
                else:
                    return "menu"
            elif event.key == pg.K_ESCAPE:
                return "menu"
        return None

    def update(self):
        current_time = pg.time.get_ticks()
        if self.current_char_index < self.total_chars:
            if current_time - self.last_char_time > self.typing_speed:
                self.current_char_index += 1
                self.last_char_time = current_time

    def draw(self):
        self.screen.fill(COLORS['black'])
        for item in self.prepared_items:
            if item['type'] == 'text':
                # On n'affiche que si l'index global a dépassé le start_index de la ligne
                if self.current_char_index > item['start_index']:
                    # Combien de caractères de cette ligne afficher ?
                    char_limit = min(self.current_char_index - item['start_index'], item['length'])
                    text_to_render = item['full_text'][:char_limit]
                    
                    surf = item['font'].render(text_to_render, True, item['color'])
                    rect = surf.get_rect(center=(WIDTH // 2, item['y']))
                    self.screen.blit(surf, rect)
    
    