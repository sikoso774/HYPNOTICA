# 🌀 HYPNOTICA

**Project by Zoléni Kokolo Zassi**

My first video game, built with [`pygame-ce`](https://pyga.me/). This version (`version_v4`) is a complete refactor of the original prototype, currently transitioning from a top-down 2D game to a pseudo-3D raycasting game in the style of Wolfenstein 3D.

## ✨ Features

- **Custom raycasting engine** (`game/raycasting_engine/`): DDA ray-by-ray projection, fisheye correction, and distance-based grayscale shading.
- **Smooth frame-rate independent movement** (WASD/ZQSD + arrows), with wall sliding.
- **State machine** driving screen transitions (intro, menu, instructions, game, game over, credits).
- **Centralized audio management** (per-screen music, sound effects) via `Sound`.
- A legacy top-down 2D level (`Level`) remains in the code but is no longer connected to the game — `Level_3D` (raycasting) is the active gameplay.

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
│   ├── components/            # Sprites & UI for the legacy 2D screen + menu
│   │   ├── constants/          # Layout constants per screen
│   │   ├── elements/           # Button, Satiety, TextScroller
│   │   └── sprites/            # Player/Phone/Background/AllSprites, animated GIF
│   ├── config/                 # Global settings, audio manager, utilities
│   ├── core/
│   │   ├── screens/             # Intro, MainMenu, Instructions, Credits, GameOver, BaseScreen
│   │   └── levels/              # Level (legacy 2D) and Level_3D (raycasting, active)
│   └── raycasting_engine/      # Map, Player, RayCasting (DDA engine)
├── main.py                     # Entry point: Game class (state machine)
└── README.md
```

## 🔄 Screens & Flow

Each screen is a state handled by `main.py`'s state machine (`game/core/screens/`, `Level_3D`). Here's what each one does and how you move between them:

| Screen | State key | Description | Goes to |
|---|---|---|---|
| **Intro** | `start` | Fading splash sequence (dev logo, credits image, pygame logo). Auto-advances, or skip with `Space`/`Esc`. | → `menu` |
| **Main Menu** | `menu` | Animated GIF background with 4 buttons: JOUER, INSTRUCTIONS, CREDITS, QUITTER. | → `game` / `instructions` / `credits` / quit |
| **Instructions** | `instructions` | Typewriter-animated rules text. `Space` skips the animation, then returns; `Esc` returns immediately. | → `menu` |
| **Gameplay (3D)** | `game` | The raycasting level (`Level_3D`). 60-second timer; reaching zero ends the run. | → `game_over` |
| **Game Over** | `game_over` | Scrolling text over a game-over background. `R` restarts, `A` jumps to credits, `Q` quits. | → `menu` / `credits` / quit |
| **Credits** | `credits` | Auto-scrolling credits list. `M`/`Esc` returns to the menu, `Q` quits. | → `menu` / quit |

## 📜 License

This project is distributed under the [MIT](LICENSE) license.
