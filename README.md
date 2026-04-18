# AI-Script-Locally
<p align="center">
    <img src="https://count.getloli.com/@benzenma123?theme=rule34" alt="Moe Counter" height="60" style="margin-center:15px;" />
</p>

# Note:
- Install the latest script from the Release section only

# Tested OS
![Linux](https://img.shields.io/badge/Arch_Linux-Main-1793D1?style=flat-square&logo=Arch-Linux&logoColor=white)
![Windows 11](https://img.shields.io/badge/Windows_11-Secondary-0078D6?style=flat-square&logo=Windows&logoColor=white)

> ⚠️ **macOS is not supported.** Due to a bug in customtkinter/darkdetect that causes a hard abort on macOS 15 (build 1506), the script is Windows and Linux only for now.

# Image
<img width="945" height="1022" alt="260411_16h40m31s_screenshot" src="https://github.com/user-attachments/assets/caaadaad-b10b-4ac0-af8d-28a00e91b14c" />
- this image is decrepricated, no pic will update

# Tutorial

Here are the dependencies you should install before running the script, based on your OS.

#### Windows:
- Python 3.12 (recommended): https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
- GPU Drivers: https://www.intel.com/content/www/us/en/support/detect.html

> ⚠️ **Use Python 3.12.** Python 3.14 is not supported by customtkinter yet and will cause the script to fail.

#### Linux (depends on distro):

##### Arch / Arch-Based

    sudo pacman -S cmake python python3 tk
    sudo pacman -S vulkan-headers vulkan-icd-loader

    # Pick your GPU driver:
    sudo pacman -S vulkan-radeon      # AMD
    sudo pacman -S vulkan-intel       # Intel
    sudo pacman -S nvidia-utils       # NVIDIA

> ⚠️ **`tk` is required.** Without it, customtkinter will fail to import even if installed.

##### Debian / Ubuntu

    sudo apt install cmake python3 python3-tk mesa-vulkan-drivers vulkan-tools libvulkan-dev
    # Intel only:
    sudo apt install intel-opencl-icd intel-level-zero-gpu

##### Fedora Linux

    sudo dnf install cmake python3 python3-tkinter mesa-vulkan-drivers vulkan-tools

##### Gentoo Linux

    sudo emerge --ask python3
    # Add "vulkan" to USE flags, then:
    emerge --ask media-libs/mesa dev-util/vulkan-tools

# Tools to Install (Windows Only)
These are **required** on Windows before running the script:
- Vulkan SDK: https://sdk.lunarg.com/sdk/download/1.4.341.1/windows/vulkansdk-windows-X64-1.4.341.1.exe
- CMake: https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-windows-x86_64.msi
- W64Devkit (place in the same folder as the script): https://github.com/skeeto/w64devkit/releases

> **Note:** W64Devkit must be in the same folder as the script — it's auto-detected. CMake and Vulkan SDK can be installed to their default locations.

# How to Run

Show menu:
```bash
python3 ai_script.py
```

Direct launch:
```bash
python3 ai_script.py -g       # GUI mode
python3 ai_script.py -u       # TUI mode
```

The script will automatically create a virtual environment and install all required Python packages on first run.

On startup without arguments, it shows:
```
***************************************
      ♡ AI Launcher ♡
***************************************
  Usage: python3 ai_script.py [options]

  Options:
   -g  --gui      GUI mode
   -u  --tui      TUI mode


  Examples:
   python3 ai_script.py -g      # GUI mode
   python3 ai_script.py -u      # TUI mode
***************************************
```

# AI Models

### Text & Reasoning
| Model | Description | RAM |
|-------|-------------|-----|
| Llama 3.2 1B | Light model for systems under 8GB RAM | ~0.81 GB |
| Llama 3.2 3B | Heavier model, needs more CPU cores/RAM | ~2.0 GB |
| Gemma 2 2B | Good general model | ~1.71 GB |
| Qwen 2.5 1.5B | Good for coding | ~1.12 GB |
| Phi-3.5 Mini | Microsoft's model | ~2.39 GB |
| DeepSeek R1 1.5B | Reasoning model | ~2.0 GB |
| DeepSeek R1 8B | Smart reasoning | ~6.5-7.2 GB |

### Coding
| Model | Description | RAM |
|-------|-------------|-----|
| Qwen 2.5 Coder 1.5B | Best for coding tasks | ~1.1 GB |
| CodeLlama 7B | Code generation | ~4.0 GB |
| CodeLlama 13B | More powerful code | ~7.3 GB |

### Chat
| Model | Description | RAM |
|-------|-------------|-----|
| Mistral 7B | Best quality at 7B | ~4.5 GB |
| Mistral Nemo 12B | Larger chat model | ~7.0 GB |
| Neural Chat 7B | Intel's chat model | ~4.0 GB |
| TinyLlama 1.1B | Ultra lightweight fallback | ~0.7 GB |

### Roleplay (NEW!)
| Model | Description | RAM |
|-------|-------------|-----|
| Peach 9B Roleplay | Popular RP model | ~5.5 GB |
| Soliloquy 8B | Narrative style | ~4.9 GB |
| RP Llama 3 8B | Character roleplay | ~4.9 GB |
| Violet Lotus 12B | Highly recommended RP | ~7.0 GB |
| Violet Twilight | Great for storytelling | ~7.0 GB |
| Wayfarer 12B | Character depth | ~7.0 GB |
| And more... | | |

# Features (NEW!)

### 16 Themes/Personas
- Felix Argyle (Re:Zero cat boy)
- Rem (Re:Zero maid)
- Emilia (Re:Zero half-elf)
- Natsuki Subaru (Re:Zero)
- Astolfo (Fate)
- Remu Osamu
- Zero Tou
- Kamen Rider Zio
- Kamen Rider Build
- Kamen Rider Ex-Aid
- Kamen Rider Kuuga
- Kamen Rider Agito
- Kamen Rider Wizard
- HyDE (Hyprland)
- Linux Tux
- Default (Professional Assistant)

### GPU Detection
- **NVIDIA** via nvidia-smi
- **AMD/APU** via Vulkan
- **Intel** via Vulkan
- Auto-detects best backend

### Content Filter (NEW!)
The script includes an automatic content filter that enforces legal and ethical boundaries. It blocks inappropriate content involving minors. This is ALWAYS ON in the published version and cannot be bypassed.

Violations:
1. Warning + message blurred
2. 1-day ban
3. 5-day ban
4. Permanent ban

### Settings Menu
- Context size (n_ctx): 2048-16384
- Temperature: 0.1-2.0
- Max tokens: 256-4096
- GPU layers: 0-35
- System prompt editor

### UI Features
- Custom dark theme per persona
- Dynamic background (Unsplash)
- Chat history sidebar
- Model dropdown selector
- Real-time stats (RAM, CPU, GPU, Tokens)
- Stop generation button

### TUI Commands
- Type your message and press Enter to send
- Type `new` to start a fresh session
- Type `exit` to quit
- Search models with keywords: "llama", "code", "char", "7b"

# Common Errors & Fixes

### tkinter not found (Linux)
If you see an import error related to tkinter or customtkinter fails:

    # Arch:
    sudo pacman -S tk

    # Debian/Ubuntu:
    sudo apt install python3-tk

    # Fedora:
    sudo dnf install python3-tkinter

### Vulkan / GPU not found (Linux)
If the script can't find your GPU:

    sudo pacman -S vulkan-headers vulkan-icd-loader   # Arch
    sudo usermod -aG render,video $USER
    # Log out and back in, then:
    GGML_VULKAN_DEVICE=0 python3.12 ai_script.py

### Script loops forever on install
This happens when Python 3.14 is used. Use Python 3.12 instead:

    sudo pacman -S python312   # Arch
    rm -rf ai_venv
    python3.12 ai_script.py

### customtkinter crashes on macOS
macOS is not supported. A bug in darkdetect causes a hard abort on macOS 15 build 1506 and there is no fix yet without a system update.

# For NVIDIA & AMD Users
If you already have GPU drivers installed, you only need the tools listed in the "Tools to Install" section (Windows) or the Vulkan packages for your distro (Linux).

# Hints
- After the first run, the script works **offline** — no internet needed
- Models are cached in `~/.cache/huggingface` and won't re-download
- Keep your device plugged in — GPU mode draws more power
- Use **Python 3.12** for best compatibility
- TUI mode works great over SSH or on headless machines

# ⚖️ License & Disclaimer
- This project is for educational purposes. All models are subject to their respective creators' licenses (Meta, Google, Microsoft, Alibaba, etc.). Use responsibly. If you get sued, that's on you :)

# Supporters
- benzenma123 (me)
- *(contact me if you want to contribute)*

# Update Log

#### 04/01/2025 20:30
- First release
- 2 AI models (Llama & Moondream)

#### 05/01/2025 16:30
- Added more models (Moondream, Llama 3B, Qwen, Gemma)
- Added `/clear` to clear AI memory

#### 06/01/2025 15:39
- Added DeepSeek R1 (1.5B and 8B)
- Fixed error when using Gemma

#### 02/14/2026 08:58
- Fixed the script
- GPU acceleration working (iGPU of all brands, x86_64 only)
- Still not working on other architectures

#### 04/10/2026
- Made script cross-platform (Windows + Linux)
- Auto-detects GPU backend (Vulkan on both platforms)
- w64devkit auto-detection on Windows
- macOS dropped due to customtkinter/darkdetect compatibility issue

#### 04/11/2026
- Fixed infinite install loop caused by Python 3.14 incompatibility
- Added tkinter system check with helpful error messages per distro
- Added vulkan-headers and vulkan-icd-loader to Arch install steps (fixes llama-cpp-python build failure)
- Added tk to Arch install steps (fixes customtkinter import failure)
- Script now exits cleanly with instructions instead of looping on import errors
- Confirmed working on Arch Linux with Python 3.12

#### 04/13/2026
- Added TUI (terminal) mode — run the AI without a GUI, great for SSH and headless setups
- Launcher now asks GUI or TUI at startup
- Multi-session chat — each history entry now has its own isolated chat window
- Streaming text output in both GUI and TUI mode
- Added 3 new models: Qwen 2.5 Coder 1.5B, Mistral 7B, TinyLlama 1.1B

#### 04/17/2026 (MAJOR UPDATE)
- **Added 16 Themes/Personas**: Felix Argyle, Rem, Emilia, Subaru, Astolfo, Kamen Rider series, HyDE, Linux Tux, Default
- **Added 46+ Models**: Including roleplay models (Violet Lotus, Wayfarer, etc.)
- **Added Content Filter**: Automatic blocking of inappropriate content involving minors
- **Added Settings Menu**: Context size, temperature, max tokens, GPU layers, system prompt editor
- **Added Token Counter**: Tracks total tokens per session
- **Added CLI Arguments**: -g (GUI), -u (TUI), -t (test mode)
- **Added Startup Menu**: Shows usage instructions when run without arguments
- **Improved GPU Detection**: Now detects NVIDIA, AMD, Intel automatically
- **Added Chat History**: Auto-saves to JSON files
- **Added Stop Button**: Cancel generation mid-response
