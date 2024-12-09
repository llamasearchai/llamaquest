# 🦙 LlamaQuest

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Rust](https://img.shields.io/badge/Rust-1.70+-orange.svg?logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![Pyxel](https://img.shields.io/badge/Pyxel-1.9.x-red)](https://github.com/kitao/pyxel)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI/CD](https://img.shields.io/badge/CI/CD-passing-brightgreen)](https://llamasearch.ai

<div align="center">
  <img src="docs/images/llamaquest_banner.png" alt="LlamaQuest Banner" width="800">
  <p>A procedurally generated llama farming and adventure game with Rust-powered terrain generation.</p>
</div>

## 🎮 Game Overview

LlamaQuest is a unique blend of farming simulation, adventure gaming, and machine learning. In this game, you'll:

- Build and manage your own llama farm in a procedurally generated world
- Breed unique llamas with genetic traits that affect their stats and appearance
- Trade resources with local villages and other players in multiplayer mode
- Embark on quests to discover rare items and special llama variants
- Navigate dynamic weather systems and seasonal changes that affect gameplay
- Utilize high-performance Rust modules for terrain generation and physics

The game features a retro-inspired pixel art style while leveraging modern game development techniques for an engaging and extensive gameplay experience.

## 📹 Demo & Screenshots

<div align="center">
  <a href="https://youtu.be/llamaquest_gameplay_demo"><img src="docs/images/video_thumbnail.png" alt="Gameplay Video" width="400"></a>
</div>

<div align="center">
  <img src="docs/images/screenshot1.png" alt="Gameplay Screenshot 1" width="400">
  <img src="docs/images/screenshot2.png" alt="Gameplay Screenshot 2" width="400">
</div>

## 🚀 Features

- **Advanced Terrain Generation**: Procedurally generated world with diverse biomes implemented in Rust for high performance
- **Genetic Algorithm**: Realistic llama breeding with inherited traits and mutations
- **Dynamic Economy**: Fluctuating market prices based on supply and demand
- **Weather System**: Dynamic weather patterns affecting crop growth and llama happiness
- **AI Behavior**: Intelligent llama and NPC behaviors powered by decision trees and state machines
- **Cross-platform**: Play on Desktop (Windows, macOS, Linux) or in a web browser
- **Multiplayer Support**: Connect with friends in cooperative or competitive farm management

## 🔧 Tech Stack

- **Frontend**: Python with Pyxel for retro-style rendering
- **Core Game Logic**: Python with NumPy for game mechanics
- **Performance-Critical Components**: Rust for terrain generation, physics, and pathfinding
- **Web Interface**: WebAssembly compiled from Rust for browser play
- **Multiplayer Backend**: Python with WebSockets
- **Desktop Packaging**: Tauri for native application distribution

## 🏗️ Architecture

LlamaQuest follows a modern hybrid architecture:

```
LlamaQuest
├── Python Game Engine
│   ├── Game Loop
│   ├── Rendering
│   ├── User Interface
│   └── Game Logic
├── Rust Core Engine
│   ├── Terrain Generation
│   ├── Physics Simulation
│   ├── Pathfinding
│   └── Resource Management
└── Web/Desktop Integration
    ├── WebAssembly Bindings
    ├── Tauri Desktop App
    └── Multiplayer Services
```

For more details on the architecture, see [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🚦 Getting Started

### Prerequisites

- Python 3.8+
- Rust (latest stable)
- Node.js 16+ (for web deployment)
- Pyxel (Python game library)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://llamasearch.ai
   cd llamaquest
   ```

2. **Install Python dependencies**
   ```bash
   cd python
   pip install -r requirements.txt
   ```

3. **Build the Rust components**
   ```bash
   cd ../rust_core
   ./build.sh
   ```

### Running the Game

#### Desktop Version
```bash
./run_desktop.sh
```

#### Web Version
```bash
./run_web.sh
```

For detailed instructions, including multiplayer setup, see [INSTALLATION.md](docs/INSTALLATION.md).

## 🧪 Development

### Project Structure

```
llamaquest/
├── python/                  # Python game implementation
│   ├── llamaquest/          # Main game modules
│   │   ├── ai.py            # AI behavior for llamas and NPCs
│   │   ├── economy.py       # Trade and economic systems
│   │   ├── genetics.py      # Llama breeding and traits
│   │   ├── terrain.py       # Python terrain utilities
│   │   └── weather.py       # Weather and season simulation
│   └── requirements.txt     # Python dependencies
├── rust_core/               # Rust implementation
│   ├── src/                 # Rust source code
│   │   ├── terrain.rs       # Terrain generation algorithms
│   │   ├── pathfinding.rs   # Pathfinding for NPCs
│   │   └── lib.rs           # Library entry point
│   └── Cargo.toml           # Rust dependencies
├── web/                     # Web interface
│   ├── index.html           # Main web page
│   └── js/                  # JavaScript bindings
├── tauri/                   # Desktop application packaging
├── tests/                   # Automated tests
└── docs/                    # Documentation
```

### Building from Source

See [BUILDING.md](docs/BUILDING.md) for complete build instructions.

### Contributing

We welcome contributions! Please check our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest enhancements.

## 📚 Documentation

- [User Guide](docs/USER_GUIDE.md) - How to play the game
- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Extending and modifying the game
- [API Reference](docs/API_REFERENCE.md) - Python and Rust API documentation

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Pyxel](https://github.com/kitao/pyxel) - Retro game engine for Python
- [Perlin Noise](https://en.wikipedia.org/wiki/Perlin_noise) - Algorithm used for terrain generation
- [WebAssembly](https://webassembly.org/) - Enabling high-performance web gaming
- [Tauri](https://tauri.app/) - Framework for building lightweight desktop applications
- All contributors who have helped shape LlamaQuest 
# Updated in commit 1 - 2025-04-04 17:01:08
