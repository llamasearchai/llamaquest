# Contributing to LlamaQuest

Thank you for your interest in contributing to LlamaQuest! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to foster an inclusive and respectful community.

## How to Contribute

### Reporting Bugs

If you find a bug in the game, please create an issue on our GitHub repository with the following information:

1. A clear and descriptive title
2. Steps to reproduce the bug
3. Expected behavior
4. Actual behavior
5. Screenshots if applicable
6. System information (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for enhancing LlamaQuest! To suggest an enhancement:

1. Create an issue with a clear title and detailed description
2. Explain why this enhancement would be useful
3. Provide examples of how it would work if possible

### Pull Requests

We actively welcome your pull requests for code contributions, documentation improvements, or new features. Here's how to submit a pull request:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a pull request

### Development Workflow

1. Set up your development environment:
   ```bash
   # Clone your fork
   git clone https://github.com/yourusername/llamaquest.git
   cd llamaquest
   
   # Set up Python environment
   cd python
   pip install -r requirements.txt
   pip install -e .
   
   # Build Rust core (if needed)
   cd ../rust_core
   cargo build
   ```

2. Run tests before submitting your changes:
   ```bash
   # Run Python tests
   cd python
   pytest
   
   # Run Rust tests
   cd ../rust_core
   cargo test
   ```

3. Format your code according to the project style:
   - Python: Use `black` and `isort`
   - Rust: Use `rustfmt`

## Project Structure

Understanding the project structure will help you contribute effectively:

- **python/**: Contains the Python game logic and high-level systems
  - **llamaquest/**: Main Python package
  - **tests/**: Python tests
- **rust_core/**: Contains Rust code for performance-critical parts
  - **src/**: Rust source files
  - **tests/**: Rust tests
- **web/**: Web frontend for browser play
- **tauri/**: Tauri app configuration for desktop
- **docs/**: Documentation
- **assets/**: Game assets including sprites, sounds, and world data

## Documentation

Good documentation is essential. When contributing:

- Document new functions, classes, and modules
- Update existing documentation if you change functionality
- Add examples where appropriate
- Update README if necessary

## Community

Join our community discussions:

- GitHub Discussions: For feature ideas and general questions
- Discord: For real-time chat and collaboration

## Attribution

Contributors will be acknowledged in our CONTRIBUTORS.md file. By contributing, you agree to license your contributions under the same license as this project. 