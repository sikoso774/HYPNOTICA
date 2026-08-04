# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

HYPNOTICA (a.k.a. "Deep Hypnotica") is Zoléni Kokolo Zassi's first video game, built with `pygame-ce`. This is `version_v4`, a refactor of an earlier prototype, currently mid-transition from a 2D top-down game to a raycasting-based pseudo-3D game (Wolfenstein-style).

## Commands

Dependencies are managed with `uv` (see `pyproject.toml` / `uv.lock`, Python >=3.12).

```bash
uv sync              # install dependencies
uv run main.py        # run the game
```

There is no test suite, linter, or build/packaging step configured. `test.py` at the repo root is a scratch file for language experiments (e.g. `hasattr`/`setattr`), not a real test — ignore it unless asked to work on it.

## Architecture

### Entry point and state machine

`main.py` defines the `Game` class, which owns the `pg.display` surface, the shared `Sound` manager, and `delta_time`. `Game.run()` is a simple state-machine loop keyed by `self.current_state` (`'start'`, `'menu'`, `'instructions'`, `'credits'`, `'game'`, `'game_over'`), each mapped to a screen object built in `Game.setup()`. Screens return either `None` (stay), an action string (transition to that state), or `'quit'`. Note: entering `'game'` recreates `self.level = Level_3D(self)` every time to reset the run.

### Screens (`game/core/screens/`)

All screens subclass `BaseScreen` (`game/core/screens/base_screen.py`), which implements the shared per-screen loop: `check_events()` → `update()` → `draw()` → `pg.display.flip()`. Subclasses override `on_event(event)`, `update()`, and `draw()`; `update()`/`on_event()` can return an action string to trigger a state transition. If a screen sets `self.music_name`, `BaseScreen.run()` auto-plays that track via `Sound.play_music()` on entry.

### Raycasting engine (`game/raycasting_engine/`)

This is the active gameplay path, wired up as `Level_3D` (`game/core/levels/level_3d.py`, exported from `game/core/__init__.py`). `levels/` is kept as its own directory even with a single file today, since a future overworld/level-select map (Super Mario World-style) will add more files there. It composes three pieces each frame:
- `Map` (`map.py`) — a hardcoded `mini_map` grid converted into a `world_map` dict of `(x, y) -> wall_id` for O(1) collision/wall lookups.
- `Player` (`player.py`) — position/angle in map (tile) coordinates, WASD/ZQSD + arrow-key movement scaled by `game.dt`, with axis-separated wall sliding via `check_wall_collision`.
- `RayCasting` (`engine.py`) — DDA-style raycaster (horizontal/vertical grid intersections compared per ray) that fisheye-corrects depth and draws vertical wall slices directly with `pg.draw.rect` (no textures yet — shading is distance-based grayscale).

All raycasting math constants (`FOV`, `NUM_RAYS`, `MAX_DEPTH`, `SCREEN_DIST`, `TILE_SIZE`, etc.) live in `game/config/settings.py` and are derived from `WIDTH`/`HEIGHT` at import time — changing `WIDTH`/`HEIGHT` requires these derived constants to stay consistent, so edit them in settings.py rather than overriding downstream.

### Config (`game/config/`)

`game/config/__init__.py` re-exports `settings.py` (constants, colors, paths), `utils.py` (`get_resource_path` for PyInstaller-compatible asset paths, `get_font` with a module-level font cache, `display_text_center`), and `sound.py` (`Sound`, keyed music/SFX dictionaries, resolves files under `assets/audio/`). Most other modules do `from game.config import *` or `from game.config.settings import *`, so new constants should go in `settings.py` to stay consistent with existing imports.

### Components (`game/components/`)

Used by `MainMenu` and `GameOver`: `button_style.py` (shared button dimensions/colors), `elements/` (`Button`, `TextScroller`), and `animation_gif.py` (`Animation_GIF`, used for the main-menu GIF background). Screen-specific content (`INSTRUCTIONS_CONTENT`, `CREDITS_CONTENT`, `BUTTONS_MENU`) lives directly in its screen file (`game/core/screens/instructions.py`, `credits.py`, `mainmenu.py`) rather than in a separate constants module, since each is only ever used by one screen.

### Assets

`assets/` holds images, fonts (`MINDCONTROL.ttf`), and audio, referenced via `get_resource_path()` so paths resolve correctly both in dev and in a PyInstaller-frozen build.

## Notes

- `debug.py` (gitignored) is a personal interactive screen-picker script for jumping directly to any screen; it imports `Game` from `main.py` (the top-level entry point, not `game/game.py` which doesn't exist).
- `others/` and `backups/` are gitignored scratch/backup directories, not part of the shipped code. The original 2D top-down prototype (`Level` screen, `game/components/sprites/sprites.py`, `sprites/groups.py` (`AllSprites`), `elements/satiety.py` (`Satiety`)) was moved to `others/legacy_2d_level/` once `Level_3D` (raycasting) became the only playable path — kept on disk for reference, no longer part of the active codebase or import graph.
