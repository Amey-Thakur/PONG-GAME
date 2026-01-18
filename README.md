<div align="center">

  <a name="readme-top"></a>
  # Pong Game

  [![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
  [![Status](https://img.shields.io/badge/Status-Completed-success)](https://github.com/Amey-Thakur/PONG-GAME)
  [![Play Now](https://img.shields.io/badge/Play-NOW-blue?style=for-the-badge&logo=github)](https://amey-thakur.github.io/PONG-GAME/)

  Start the Game: **[PONG GAME LIVE](https://amey-thakur.github.io/PONG-GAME/)**

  A classic arcade implementation of Pong, engineered with **Pygame** and optimized for web execution via **Pygbag**.

  **[Source Code](Source%20Code/)** &nbsp;·&nbsp; **[Play Online](https://amey-thakur.github.io/PONG-GAME/)** &nbsp;·&nbsp; **[Report Bug](https://github.com/Amey-Thakur/PONG-GAME/issues)**

</div>

---

<div align="center">

  [Overview](#overview) &nbsp;·&nbsp; [Controls](#controls) &nbsp;·&nbsp; [Tech Stack](#tech-stack) &nbsp;·&nbsp; [Code Structure](#code-structure) &nbsp;·&nbsp; [License](#license)

</div>

---

<!-- OVERVIEW -->
<a name="overview"></a>
## Overview

**Pong Game** is a high-fidelity recreation of the 1972 tabular arcade game. This project serves as a study in game loop mechanics, collision detection physics, and state management using Python.

### Key Features
*   **Physics Engine**: Precise ball deflection and velocity adjustment based on paddle impact branding.
*   **AI Opponent**: A reactive computer-controlled paddle that tracks ball positioning.
*   **Procedural Audio**: Retro sound effects triggered by collision events.
*   **WebAssembly**: Compiled to run natively in modern web browsers using **Pygbag**.

---

<!-- CONTROLS -->
<a name="controls"></a>
## Controls

| Action | Player Input |
| :--- | :--- |
| **Move Up** | <kbd>⬆️ Up Arrow</kbd> |
| **Move Down** | <kbd>⬇️ Down Arrow</kbd> |
| **Start/Reset** | Automatic (Round Based) |

---

<!-- TECH STACK -->
<a name="tech-stack"></a>
### Tech Stack
- **Languages**: Python 3.11
- **Engine**: **Pygame** (Rendering & Physics)
- **Functions**: `ball_animation()`, `player_animation()`, `opponent_animation()`
- **Deployment**: **Pygbag** (WebAssembly Compilation)
- **Hosting**: GitHub Pages

---

<!-- STRUCTURE -->
<a name="code-structure"></a>
## Code Structure

```python
PONG-GAME/
│
├── .github/
│   └── workflows/
│       └── main.yml        # CI/CD Pipeline (Pygbag Build)
│
├── Source Code/
│   ├── sound/              # Audio Assets (WAV)
│   └── main.py             # Core Game Logic (Entry Point)
│
└── README.md               # Documentation
```

---

<!-- LICENSE -->
<a name="license"></a>
## License

This repository is available under the **MIT License**.

Copyright © 2022 **Amey Thakur**

<div align="center">
  <br>
  👉🏻 <a href="https://github.com/Amey-Thakur"><strong>Back to Engineering</strong></a> 👈🏻
</div>
