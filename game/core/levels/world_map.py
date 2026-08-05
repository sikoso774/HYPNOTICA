import pygame as pg
import math
from game.config import *
from game.core.screens import BaseScreen

# World map depths (only one level exists for now:
# the following ones are locked, they show what's planned next).
NODES = [
    {'name': "L'Antichambre", 'depth': 'I', 'locked': False, 'action': 'game',
     'flavor': "Le seuil de ta conscience. La premiere porte."},
    {'name': "Le Pendule", 'depth': 'II', 'locked': True, 'action': None,
     'flavor': "Un balancier hypnotique bat quelque part dans le noir."},
    {'name': "La Spirale", 'depth': 'III', 'locked': True, 'action': None,
     'flavor': "Elle tourne. Elle a toujours tourne."},
    {'name': "L'Oeil Ouvert", 'depth': 'IV', 'locked': True, 'action': None,
     'flavor': "Il te regarde revenir, encore et encore."},
    {'name': 'Le Point Zero', 'depth': 'V', 'locked': True, 'action': None,
     'flavor': "Toutes les pensees convergent ici."},
]

CENTER = (WIDTH // 2, 260)
R_MAX = 190
R_MIN = 40
THETA_END = math.pi * 2.5
NODE_RADIUS = 20
LABEL_OFFSET = 28

PATH_COLOR = (60, 52, 76)
LOCKED_COLOR = (74, 63, 92)
UNLOCKED_COLOR = COLORS['purple']
SELECTED_COLOR = COLORS['green']
DIM_TEXT_COLOR = (144, 131, 171)
PANEL_BG = (21, 15, 36)

PULSE_AMPLITUDE = 3
PULSE_SPEED = 0.005
CURSOR_COLOR = COLORS['green']
CURSOR_RADIUS = 6

TRANSITION_DURATION_MS = 700
TRANSITION_ZOOM_MAX = 0.5


class WorldMap(BaseScreen):
    """Super Mario World-style level-select screen: nodes placed along a spiral path."""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = get_font(DEFAULT_FONT_NAME, 34)
        self.font_node = get_font(BODY_FONT_BOLD_NAME, 14)
        self.font_label = get_font(BODY_FONT_NAME, 13)
        self.font_panel_name = get_font(BODY_FONT_BOLD_NAME, 20)
        self.font_panel_text = get_font(BODY_FONT_NAME, 14)
        self._build_path()
        self._place_nodes()
        self.selected = 0
        self.transitioning = False

    def run(self):
        """Always restarts on the first depth when entering the map."""
        self.selected = 0
        self.transitioning = False
        pg.mouse.set_visible(False)
        try:
            return super().run()
        finally:
            pg.mouse.set_visible(True)

    # --- Spiral geometry ---

    def _build_path(self):
        """Samples the spiral and computes its cumulative length, so nodes can then
        be placed at regular intervals along the curve (rather than at regular
        angle intervals, which would bunch them up near the center)."""
        steps = 300
        samples = []
        cumulative_len = 0.0
        prev_point = None
        for step in range(steps + 1):
            t = step / steps
            theta = THETA_END * t
            r = R_MAX - (R_MAX - R_MIN) * t
            x = CENTER[0] + r * math.cos(theta)
            y = CENTER[1] + r * math.sin(theta)
            if prev_point is not None:
                cumulative_len += math.hypot(x - prev_point[0], y - prev_point[1])
            samples.append((x, y, theta, cumulative_len))
            prev_point = (x, y)
        self._samples = samples
        self._total_len = cumulative_len
        self.path_points = [(s[0], s[1]) for s in samples]

    def _point_at_arc_fraction(self, fraction):
        target = fraction * self._total_len
        samples = self._samples
        for i in range(1, len(samples)):
            ax, ay, atheta, alen = samples[i - 1]
            bx, by, btheta, blen = samples[i]
            if blen >= target:
                seg = (target - alen) / (blen - alen) if blen > alen else 0
                x = ax + (bx - ax) * seg
                y = ay + (by - ay) * seg
                theta = atheta + (btheta - atheta) * seg
                return x, y, theta
        last = samples[-1]
        return last[0], last[1], last[2]

    def _place_nodes(self):
        count = len(NODES)
        for i, node in enumerate(NODES):
            x, y, theta = self._point_at_arc_fraction(i / (count - 1))
            node['pos'] = (x, y)
            node['label_pos'] = (x + math.cos(theta) * LABEL_OFFSET, y + math.sin(theta) * LABEL_OFFSET)
            cos_t = math.cos(theta)
            node['label_align'] = 'left' if cos_t > 0.15 else ('right' if cos_t < -0.15 else 'center')

    # --- Inputs ---

    def on_event(self, event):
        if self.transitioning:
            return None
        if event.type == pg.KEYDOWN:
            if event.key in (pg.K_DOWN, pg.K_RIGHT):
                self._move_selection(1)
            elif event.key in (pg.K_UP, pg.K_LEFT):
                self._move_selection(-1)
            elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                return self._confirm()
            elif event.key == pg.K_m:
                self.sound.play_sfx('click')
                return "menu"
        elif event.type == pg.MOUSEMOTION:
            self._handle_hover(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            hovered = self._node_at(event.pos)
            if hovered is not None:
                self.selected = hovered
                return self._confirm()
        return None

    def _move_selection(self, direction):
        self.selected = (self.selected + direction) % len(NODES)
        self.sound.play_sfx('click')

    def _node_at(self, pos):
        for i, node in enumerate(NODES):
            nx, ny = node['pos']
            if (pos[0] - nx) ** 2 + (pos[1] - ny) ** 2 <= NODE_RADIUS ** 2:
                return i
        return None

    def _handle_hover(self, pos):
        hovered = self._node_at(pos)
        if hovered is not None and hovered != self.selected:
            self.selected = hovered
            self.sound.play_sfx('click')

    def _confirm(self):
        node = NODES[self.selected]
        if node['locked']:
            return None
        self.sound.play_sfx('confirm')
        self.transitioning = True
        self.transition_start = pg.time.get_ticks()
        self.transition_action = node['action']
        self.transition_node_pos = node['pos']
        return None

    def update(self):
        """While transitioning, hand the pending action back once the vortex animation ends."""
        if self.transitioning:
            elapsed = pg.time.get_ticks() - self.transition_start
            if elapsed >= TRANSITION_DURATION_MS:
                return self.transition_action
        return None

    # --- Rendering ---

    def draw(self):
        self.screen.fill(COLORS['black'])
        pg.draw.circle(self.screen, (26, 20, 38), CENTER, R_MAX, 1)
        pg.draw.circle(self.screen, (26, 20, 38), CENTER, (R_MAX + R_MIN) // 2, 1)

        if len(self.path_points) > 1:
            pg.draw.lines(self.screen, PATH_COLOR, False, self.path_points, 2)

        for i, node in enumerate(NODES):
            self._draw_node(i, node)

        title_surf = self.font_title.render("CARTE DES PROFONDEURS", True, COLORS['white'])
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 40))
        self.screen.blit(title_surf, title_rect)

        self._draw_panel()
        self._draw_hints()
        self._draw_cursor()

        if self.transitioning:
            self._draw_transition()

    def _draw_node(self, index, node):
        x, y = node['pos']
        pos = (int(x), int(y))
        selected = index == self.selected

        if node['locked']:
            ring_color = COLORS['white'] if selected else LOCKED_COLOR
            fill_color = (18, 14, 28)
        else:
            ring_color = SELECTED_COLOR if selected else UNLOCKED_COLOR
            fill_color = (35, 20, 56)

        pg.draw.circle(self.screen, fill_color, pos, NODE_RADIUS)
        if selected:
            pulse = math.sin(pg.time.get_ticks() * PULSE_SPEED) * PULSE_AMPLITUDE
            pg.draw.circle(self.screen, ring_color, pos, NODE_RADIUS + pulse, 3)
        else:
            pg.draw.circle(self.screen, ring_color, pos, NODE_RADIUS, 2)

        if node['locked']:
            self._draw_lock_icon(x, y)
        else:
            depth_surf = self.font_node.render(node['depth'], True, ring_color)
            depth_rect = depth_surf.get_rect(center=pos)
            self.screen.blit(depth_surf, depth_rect)
            # Progress marker: always on the first depth,
            # the only level that's actually playable today.
            if index == 0:
                pg.draw.circle(self.screen, SELECTED_COLOR, pos, 4)

        label_x, label_y = node['label_pos']
        label_surf = self.font_label.render(f"{node['depth']}. {node['name']}", True,
                                             COLORS['white'] if selected else DIM_TEXT_COLOR)
        label_rect = label_surf.get_rect()
        if node['label_align'] == 'left':
            label_rect.midleft = (label_x, label_y)
        elif node['label_align'] == 'right':
            label_rect.midright = (label_x, label_y)
        else:
            label_rect.center = (label_x, label_y)
        self.screen.blit(label_surf, label_rect)

    def _draw_lock_icon(self, x, y):
        body = pg.Rect(0, 0, 11, 8)
        body.center = (x, y + 2)
        pg.draw.rect(self.screen, LOCKED_COLOR, body, border_radius=1)
        pg.draw.arc(self.screen, LOCKED_COLOR, pg.Rect(x - 4, y - 7, 8, 8), 0, math.pi, 2)

    def _draw_panel(self):
        node = NODES[self.selected]
        panel_rect = pg.Rect(0, 0, 460, 100)
        panel_rect.center = (WIDTH // 2, HEIGHT - 80)

        panel_surf = pg.Surface(panel_rect.size, pg.SRCALPHA)
        panel_surf.fill((*PANEL_BG, 235))
        pg.draw.rect(panel_surf, LOCKED_COLOR, panel_surf.get_rect(), 1)
        self.screen.blit(panel_surf, panel_rect)

        name_surf = self.font_panel_name.render(f"{node['depth']}. {node['name']}", True, COLORS['white'])
        name_rect = name_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 24))
        self.screen.blit(name_surf, name_rect)

        flavor_surf = self.font_panel_text.render(node['flavor'], True, DIM_TEXT_COLOR)
        flavor_rect = flavor_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 50))
        self.screen.blit(flavor_surf, flavor_rect)

        status_text = "Verrouille" if node['locked'] else "Pret a explorer"
        status_color = DIM_TEXT_COLOR if node['locked'] else SELECTED_COLOR
        status_surf = self.font_panel_text.render(status_text, True, status_color)
        status_rect = status_surf.get_rect(center=(panel_rect.centerx, panel_rect.top + 76))
        self.screen.blit(status_surf, status_rect)

    def _draw_hints(self):
        hint_text = "HAUT/BAS: naviguer   ENTREE: explorer   M: retour au menu"
        hint_surf = self.font_panel_text.render(hint_text, True, LOCKED_COLOR)
        hint_rect = hint_surf.get_rect(center=(WIDTH // 2, HEIGHT - 16))
        self.screen.blit(hint_surf, hint_rect)

    def _draw_transition(self):
        """Vortex-style outro: the frame gets pulled/zoomed into the chosen node
        while a black iris closes in on that same point, converging together."""
        elapsed = pg.time.get_ticks() - self.transition_start
        t = min(1.0, elapsed / TRANSITION_DURATION_MS)
        eased = t * t  # ease-in: the pull accelerates towards the end

        nx, ny = self.transition_node_pos
        zoom = 1.0 + TRANSITION_ZOOM_MAX * eased
        w, h = self.screen.get_size()
        scaled = pg.transform.smoothscale(self.screen, (int(w * zoom), int(h * zoom)))
        offset = (nx * (1 - zoom), ny * (1 - zoom))
        self.screen.blit(scaled, offset)

        overlay = pg.Surface((w, h), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 255))
        max_radius = math.hypot(w, h)
        radius = max_radius * (1 - eased)
        if radius > 0:
            pg.draw.circle(overlay, (0, 0, 0, 0), (int(nx), int(ny)), int(radius))
        self.screen.blit(overlay, (0, 0))

    def _draw_cursor(self):
        """Custom crosshair cursor, drawn in place of the OS arrow to fit the theme."""
        x, y = pg.mouse.get_pos()
        pg.draw.circle(self.screen, CURSOR_COLOR, (x, y), CURSOR_RADIUS, 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x - CURSOR_RADIUS - 4, y), (x - 2, y), 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x + 2, y), (x + CURSOR_RADIUS + 4, y), 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x, y - CURSOR_RADIUS - 4), (x, y - 2), 1)
        pg.draw.line(self.screen, CURSOR_COLOR, (x, y + 2), (x, y + CURSOR_RADIUS + 4), 1)
