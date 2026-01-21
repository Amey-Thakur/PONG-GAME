<div align="center">

  <a name="readme-top"></a>
  # Pong Game

  [![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
  ![Status](https://img.shields.io/badge/Status-Completed-success)
  [![Technology](https://img.shields.io/badge/Technology-Python%20%7C%20Pygame-orange)](https://github.com/Amey-Thakur/PONG-GAME)
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

  **Terna Engineering College | Computer Engineering | Batch of 2022**

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

**Pong Game** is a tabula-arcade simulation designed to demonstrate core game engine mechanics including collision physics, vector-based velocity, and AI tracking logic. The application serves as a digital study into early interactive system architecture, brought into a modern context via WebAssembly.

### Python Principles
The development of this interface was guided by core **Python Development** paradigms:
*   **Consistency**: The interface strictly adheres to the original 1972 spatial layout, exploiting the user's existing mental model of arcade physics to ensure intuitive interaction.
*   **Direct Manipulation**: Paddle controls provide instantaneous response to input, creating a seamless loop between user intent and system action, critical for high-latency feedback environments.

> [!TIP]
> **Feedback Loop Dynamics**
>
> The design utilizes high-contrast visual elements and distinct auditory triggers (`sfx_point`, `sfx_swooshing`) to invoke strong **Feedback Loops**. By providing immediate sensory confirmation for ball-paddle impacts and score events, the interface creates a robust **Visibility of System Status**, ensuring the user remains accurately oriented within the game state at all times.

---

<!-- FEATURES -->
<a name="features"></a>
## Features

| Feature | Description |
|---------|-------------|
| **Elastic Physics** | High-precision collision detection using **Rect intersection logic** for authentic deflection. |
| **Reactive AI** | An intelligent opponent paddle engineered with **velocity-tracking heuristics** for a scalable challenge. |
| **Binaural Audio** | Event-driven auditory feedback system synchronized with **real-time physics triggers**. |
| **Wasm Stack** | Efficient **WebAssembly compilation** via Pygbag, enabling native browser execution without plugins. |
| **Binary Scoring** | Integrated score management system with visual persistence and round-start countdowns. |
| **Adaptive Logic** | Asynchronous game loop architecture ensuring **non-blocking browser execution** and stability. |

> [!NOTE]
> ### Interactive Polish: The Velocity Singularity
> We have engineered a **physics-driven state manager** that calibrates ball velocity across three distinct axes to simulate atmospheric drag and momentum transfer. During the initial countdown, the interface provides a **Visual Prep-State**, priming the user's cognitive reaction time before the primary game loop resumes. The visual language focuses on the minimalist "High-Contrast" aesthetic of early computing, ensuring maximum focus on the interactive trajectory. Complementing this experience, the application includes a high-fidelity performance summary, with a codebase digitally signed by **Amey & Mega**.

### Tech Stack
- **Languages**: Python 3.11
- **Logic**: **Pygame Engine** (Asynchronous Loop & Physics Engine)
- **Imaging**: **freesansbold.ttf** (Anti-aliased Raster Typography)
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
- **Browser**: Any modern WebAssembly-compliant browser (Chrome, Firefox, Edge, Safari).
- **Python (Optional)**: Python 3.11+ (for local development).

> [!WARNING]
> **Local Execution**
>
> For local development, ensure that the `pygame` and `asyncio` libraries are correctly installed. Running the project locally may require `pygbag` for the full web-simulation experience.

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
