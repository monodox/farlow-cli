# Farlow

**Farlow** is an open-source, CLI-first conversational AI platform designed to run Hugging Face and other open-weight models with zero vendor lock-in. It provides a lightweight developer experience where users can register, pull, and run models locally or on GPU servers through pluggable runtimes like Transformers, llama.cpp, TGI, and vLLM.

The core vision is to make LLM operations simple, transparent, and modular — starting with a powerful command-line interface and later expanding into plugins, orchestration, and scalable model serving. Farlow aims to be the universal toolkit for developers who want full control over their models, their infrastructure, and their AI workflows.

## Features

- **CLI-First**: Manage your AI workflow entirely from the terminal.
- **Vendor Agnostic**: No lock-in. Run models from Hugging Face, local storage, or other sources.
- **Pluggable Runtimes**: Support for multiple backends (`mock`, `llama.cpp`, `transformers`).
- **Local & Remote**: Run models locally for development or connect to remote GPU servers.

## Installation

### Prerequisites

- Python 3.8+
- [Optional] C++ Compiler (for `llama.cpp` build)

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/farlow.git
cd farlow

# Install dependencies (CPU-only for torch by default)
pip install -e .

# Install PyTorch with CUDA support (Optional, for GPU)
# See https://pytorch.org/get-started/locally/ for your specific command
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Install llama-cpp-python (Optional, for GGUF models)
# Windows users might need Visual Studio Build Tools
pip install llama-cpp-python
```

## Platform Support

Farlow is designed to run on **Windows**, **Linux**, and **macOS**.

### Windows
- **CLI**: Runs in PowerShell, Command Prompt, or Git Bash.
- **Paths**: Configuration stored in `%USERPROFILE%\.farlow`.
- **GPU**: Requires CUDA toolkit for NVIDIA GPU support.

### Linux
- **CLI**: Runs in Bash, Zsh, etc.
- **Paths**: Configuration stored in `~/.farlow`.
- **GPU**: Native CUDA support usually works out of the box with PyTorch.

### macOS
- **CLI**: Runs in Terminal, iTerm2.
- **Paths**: Configuration stored in `~/.farlow`.
- **Silicon (M1/M2/M3)**: Supported via `MPS` (Metal Performance Shaders) in PyTorch (ensure you install the correct torch version).

## Building Standalone Executables

You can build a standalone executable for your current platform (no Python installation required for the end user).

1. Install dependencies:
   ```bash
   pip install .
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

3. Find your executable in `dist/<os>/farlow`.

## Installation via Snap (Linux)

Once published, you can install Farlow via Snap:

```bash
sudo snap install farlow
```

To build the snap locally:

```bash
# Install snapcraft
sudo snap install snapcraft --classic

# Build
snapcraft
```

## Usage

### 1. Pull a Model

Download and register a model.

```bash
farlow pull <model_name>
```

### 2. List Models

See what models you have available.

```bash
farlow list
```

### 3. Run a Model

Run inference on a model.

```bash
farlow run <model_name> "Your prompt here"
```

### 4. Serve Models

Start an OpenAI-compatible API server.

```bash
farlow serve --host 127.0.0.1 --port 8000
```

### 5. Plugins

Farlow supports plugins. Place your python scripts in `~/.farlow/plugins/`.
Example plugin `hello.py`:

```python
from farlow.cli import app, console

@app.command()
def hello():
    console.print("Hello from plugin!")
```

## Configuration

Farlow stores configuration and models in `~/.farlow`. You can customize settings in `~/.farlow/config.json`.

## Status

- [x] Core CLI Structure
- [x] Basic Model Management (Pull/List)
- [x] `llama.cpp` Runtime Integration
- [x] `transformers` Runtime Integration
- [x] Model Serving API
- [x] Plugin System

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
