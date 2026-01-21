<div align="center">

  <a name="readme-top"></a>
  # Pong Game

  [![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
  ![Status](https://img.shields.io/badge/Status-Completed-success)
  [![Technology](https://img.shields.io/badge/Technology-Python%20%7C%20Pygame-blueviolet)](https://github.com/Amey-Thakur/PONG-GAME)
  [![Developed by Amey Thakur and Mega Satish](https://img.shields.io/badge/Developed%20by-Amey%20Thakur%20%26%20Mega%20Satish-blue.svg)](https://github.com/Amey-Thakur/PONG-GAME)

  A modern **Python** + **Pygame** reconstruction of the original 1972 Pong, built with accurate collision physics and performance-focused game loops.

  **[Source Code](Source%20Code/)** &nbsp;·&nbsp; **[Technical Specification](Source%20Code/main.py)** &nbsp;·&nbsp; **[Live Demo](https://amey-thakur.github.io/PONG-GAME/)**

</div>

---

<div align="center">

  [Authors](#authors) &nbsp;·&nbsp; [Overview](#overview) &nbsp;·&nbsp; [Features](#features) &nbsp;·&nbsp; [Structure](#project-structure) &nbsp;·&nbsp; [Quick Start](#quick-start) &nbsp;·&nbsp; [Usage Guidelines](#usage-guidelines) &nbsp;·&nbsp; [License](#license) &nbsp;·&nbsp; [About](#about-this-repository) &nbsp;·&nbsp; [Acknowledgments](#acknowledgments)

</div>

---

<!-- AUTHORS -->
<div align="center">

  <a name="authors"></a>
  ## Authors



| <a href="https://github.com/Amey-Thakur"><img src="https://github.com/Amey-Thakur.png" width="150" height="150" alt="Amey Thakur"></a><br>[**Amey Thakur**](https://github.com/Amey-Thakur)<br><br>[![ORCID](https://img.shields.io/badge/ORCID-0000--0001--5644--1575-green.svg)](https://orcid.org/0000-0001-5644-1575) | <a href="https://github.com/msatmod"><img src="Mega/Mega.png" width="150" height="150" alt="Mega Satish"></a><br>[**Mega Satish**](https://github.com/msatmod)<br><br>[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--1844--9557-green.svg)](https://orcid.org/0000-0002-1844-9557) |
| :---: | :---: |

</div>

> [!IMPORTANT]
> ### 🤝🏻 Special Acknowledgement
> *Special thanks to **[Mega Satish](https://github.com/msatmod)** for her meaningful contributions, guidance, and support that helped shape this work.*

---

<!-- OVERVIEW -->
<a name="overview"></a>
## Overview

**Pong Game** is a precision-engineered simulation of the 1972 arcade foundational, rebuilt using **Python** and **Pygame** with a focus on engine adaptability and web performance. By leveraging **WebAssembly** for ubiquitous deployment, this project bridges the gap between retro systems and modern browser capabilities, offering a responsive, mathematically accurate study of collision dynamics and game loop architecture.

### core mechanics
The simulation is governed by strict **computational design patterns** ensuring fidelity and responsiveness:
*   **Progressive Physics**: The engine utilizes a linear velocity multiplier, incrementally increasing ball speed with every successful rally to create an evolving challenge curve.
*   **Heuristic AI**: Unlike static opponents, the CPU logic integrates a **probabilistic error function** that dynamically refines its accuracy over time, simulating an organic learning curve.
*   **Direct Manipulation**: Input handling supports both continuous key-state and coordinate-based (mouse) control schemes, ensuring **zero-latency** paddle response critical for high-speed gameplay.

> [!TIP]
> **Sensory Feedback Integration**
>
> To maximize state clarity, the engine employs a **multi-modal feedback system**. **Particle emitters** detonate on scoring events, and **dynamic trails** visualize the ball's velocity vector, strictly coupling visual flair with game state changes. This ensures the user's mental model is constantly synchronized with the underlying physics simulation without reliance on intrusive HUD elements.

---

<!-- FEATURES -->
<a name="features"></a>
## Features

| Feature | Description |
|---------|-------------|
| **Physics Engine** | High-precision collision detection using **Rect intersection logic** for authentic deflection. |
| **Adaptive AI** | Opponent logic with **velocity-tracking heuristics** and organic error rates. |
| **Spatial Audio** | Event-driven sound engine using **OGG assets** for broad browser compatibility. |
| **Wasm Architecture** | Efficient **WebAssembly compilation** via Pygbag for native web execution. |
| **Game Loop** | Asynchronous architecture ensuring **60 FPS stability** on web clients. |
| **Visual Feedback** | **Dynamic Particle Systems** that trigger on goal events for sensory reward. |
| **State Feedback** | **Velocity-Based Trails** and screen flash effects for high-impact game feel. |
| **Social Persistence** | **Interactive Footer Integration** bridging the game to the source repository. |

> [!NOTE]
> ### Interactive Polish: The Velocity Singularity
> We have engineered a **Physics-Driven State Manager** that calibrates ball velocity across multiple vectors to simulate momentum transfer. The visual language focuses on the minimalist "High-Contrast" aesthetic of early computing, ensuring maximum focus on the interactive trajectory.

### Tech Stack
- **Languages**: Python 3.11
- **Logic**: **Pygame Engine** (Asynchronous Loop & Physics Engine)
- **Imaging**: **Procedural Graphics** (Custom Particle & Trail Systems)
- **UI System**: Premium Retro Graphics (Custom Python Canvas)
- **Deployment**: GitHub Actions (Pygbag WebAssembly Pipeline)
- **Hosting**: GitHub Pages

---

<!-- STRUCTURE -->
<a name="project-structure"></a>
## Project Structure

```python
PONG-GAME/
│
├── .github/                         # Deployment & Automation Layer
│   └── workflows/
│       └── main.yml                 # CI/CD Pipeline (Pygbag Build & Deploy)
│
├── docs/                            # Technical Documentation
│   └── SPECIFICATION.md             # Architecture & Design Specification
│
├── Mega/                            # Archival Attribution Assets
│   ├── Filly.jpg                    # Companion (Filly)
│   └── Mega.png                     # Author Profile Image (Mega Satish)
│
├── Source Code/                     # Primary Application Layer
│   ├── build/                       # WebAssembly Build Artifacts
│   ├── sound/                       # Audio Assets (WAV/OGG)
│   ├── default.tmpl                 # Pygbag HTML Template
│   ├── favicon.png                  # System Identity Icon
│   ├── icon.png                     # Application Icon
│   └── main.py                      # Core Game Logic (Asynchronous Entry Point)
│
├── .gitattributes                   # Git configuration
├── .gitignore                       # Repository Filters
├── CITATION.cff                     # Scholarly Citation Metadata
├── codemeta.json                    # Machine-Readable Project Metadata
├── favicon.png                      # Root Identity Icon
├── LICENSE                          # MIT License Terms
├── README.md                        # Comprehensive Scholarly Entrance
└── SECURITY.md                      # Security Policy & Protocol
```

---

<!-- QUICK START -->
<a name="quick-start"></a>
## Quick Start

### 1. Prerequisites
- **Python 3.11+**: Required for runtime execution. [Download Python](https://www.python.org/downloads/)
- **Git**: For version control and cloning. [Download Git](https://git-scm.com/downloads)

> [!WARNING]
> **Local Execution**
>
> For local development, ensure that the `pygame` and `asyncio` libraries are correctly installed. Running the project locally may require `pygbag` for the full web-simulation experience.

### 2. Installation
Clone the repository and install the necessary dependencies in one go:

```bash
git clone https://github.com/Amey-Thakur/PONG-GAME.git
cd PONG-GAME
pip install pygame-ce pygbag
```

### 3. Execution Modes
You can launch the application in two distinct environments:

**A. Native Desktop (Recommended)**
Run the game directly as a high-performance desktop application:
```bash
python "Source Code/main.py"
```

**B. Web Simulation (Pygbag)**
Simulate the WebAssembly environment locally to test browser compatibility:
```bash
pygbag "Source Code"
```
> Access the simulation at `http://localhost:8000` once the server starts.

---

<!-- USAGE -->
<a name="usage-guidelines"></a>
## Usage Guidelines

This repository is openly shared to support learning and knowledge exchange across the academic community.

**For Students**  
Use this project as reference material for understanding game engine logic, asynchronous programming in Python, and Python principles.

**For Educators**  
This project may serve as a practical lab example or supplementary teaching resource for Python Programming and Game Development Laboratory courses (`CSC801` & `CSL801`).

---

<!-- LICENSE -->
<a name="license"></a>
## License

This repository and all its creative and technical assets are made available under the **MIT License**. See the [LICENSE](LICENSE) file for complete terms.

Copyright © 2022 Amey Thakur & Mega Satish

---

<!-- ABOUT -->
<a name="about-this-repository"></a>
## About This Repository

**Created & Maintained by**: [Amey Thakur](https://github.com/Amey-Thakur) & [Mega Satish](https://github.com/msatmod)  
**Academic Journey**: Bachelor of Engineering in Computer Engineering (2018-2022)  
**Institution**: [Terna Engineering College](https://ternaengg.ac.in/), Navi Mumbai  

This project features **The Pong Game**, developed as a **Python** project during the **8th Semester Computer Engineering** curriculum.

---

<div align="center">

  [↑ Back to Top](#readme-top)

  [Authors](#authors) &nbsp;·&nbsp; [Overview](#overview) &nbsp;·&nbsp; [Features](#features) &nbsp;·&nbsp; [Structure](#project-structure) &nbsp;·&nbsp; [Quick Start](#quick-start) &nbsp;·&nbsp; [Usage Guidelines](#usage-guidelines) &nbsp;·&nbsp; [License](#license) &nbsp;·&nbsp; [About](#about-this-repository) &nbsp;·&nbsp; [Acknowledgments](#acknowledgments)

  <br>

  🔬 **[Python Programming Laboratory](https://github.com/Amey-Thakur/HUMAN-MACHINE-INTERACTION-AND-HUMAN-MACHINE-INTERACTION-LAB)** &nbsp; · &nbsp; 🏓 **[PONG-GAME](https://amey-thakur.github.io/PONG-GAME)**

  ---

  ### 🎓 [Computer Engineering Repository](https://github.com/Amey-Thakur/COMPUTER-ENGINEERING)

</div>
