# 🌀 HYPNOTICA

**Project by Zoléni Kokolo Zassi**

My first video game, built with [`pygame-ce`](https://pyga.me/). This version (`version_v4`) is a complete refactor of the original prototype, currently transitioning from a top-down 2D game to a pseudo-3D raycasting game in the style of Wolfenstein 3D.

## ✨ Features

- **Custom raycasting engine** (`game/raycasting_engine/`): DDA ray-by-ray projection, fisheye correction, and distance-based grayscale shading.
- **Smooth frame-rate independent movement** (WASD/ZQSD + arrows), with wall sliding.
- **World map** (`game/core/levels/world_map.py`): a Super Mario World-style level-select screen, reinterpreted as a hypnotic spiral descent. Only the first depth is unlocked today — the rest preview levels to come.
- **State machine** driving screen transitions (intro, menu, world map, instructions, game, game over, credits).
- **Centralized audio management** (per-screen music, sound effects) via `Sound`.

## 🚀 Installation & Launch

Dependencies are managed with [`uv`](https://docs.astral.sh/uv/) (Python ≥ 3.12).

```bash
uv sync
uv run main.py
```

## 📂 Project Architecture

```text
HYPNOTICA/
├── assets/                    # Images, audio, fonts
├── game/
│   ├── components/            # UI for the menu + game over screens
│   │   ├── button_style.py     # Shared button dimensions/colors
│   │   ├── animation_gif.py    # Animated GIF (main-menu background)
│   │   └── elements/           # Button, TextScroller
│   ├── config/                 # Global settings, audio manager, utilities
│   ├── core/
│   │   ├── screens/             # Intro, MainMenu, Instructions, Credits, GameOver, BaseScreen
│   │   └── levels/              # level_3d.py (Level3D, active), world_map.py (level select)
│   └── raycasting_engine/      # Map, Player, RayCasting (DDA engine)
├── main.py                     # Entry point: Game class (state machine)
└── README.md
```

## 🔄 Screens & Flow

Each screen is a state handled by `main.py`'s state machine (`game/core/screens/`, `Level3D`). Here's what each one does and how you move between them:

| Screen | State key | Description | Goes to |
|---|---|---|---|
| **Intro** | `start` | Fading splash sequence (dev logo, credits image, pygame logo). Auto-advances, or skip with `Space`. | → `menu` |
| **Main Menu** | `menu` | Animated GIF background with 4 buttons: JOUER, INSTRUCTIONS, CREDITS, QUITTER. | → `world_map` / `instructions` / `credits` / quit |
| **World Map** | `world_map` | Level-select spiral. Arrow keys/mouse to pick a depth, `Enter`/click to enter (only if unlocked), `M` back to menu. | → `game` / `menu` |
| **Instructions** | `instructions` | Typewriter-animated rules text. `Space` skips the animation, then returns. | → `menu` |
| **Gameplay (3D)** | `game` | The raycasting level (`Level3D`). 60-second timer; reaching zero ends the run. | → `game_over` |
| **Game Over** | `game_over` | Scrolling text over a game-over background. `R` restarts, `A` jumps to credits, `Q` quits. | → `menu` / `credits` / quit |
| **Credits** | `credits` | Auto-scrolling credits list. `M` returns to the menu, `Q` quits. | → `menu` / quit |

`Esc` quits the whole game immediately from any screen (`BaseScreen.check_events()` handles it globally, before a screen's own `Esc` logic — if any — would run).

## 📜 License

This project is distributed under the [MIT](LICENSE) license.
