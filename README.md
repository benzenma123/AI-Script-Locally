# AI-Script-Locally
<p align="center">
    <img src="https://count.getloli.com/@benzenma123?theme=rule34" alt="Moe Counter" height="60" style="margin-center:15px;" />
</p>

# Note:
- u should only Install the latest script in the Release section

# Tested OS
![Linux](https://img.shields.io/badge/Arch_Linux-Main-1793D1?style=flat-square&logo=Arch-Linux&logoColor=white)
![Windows 11](https://img.shields.io/badge/Windows_11-Secondary-0078D6?style=flat-square&logo=Windows&logoColor=white)
> ⚠️ **macOS is not supported.** Due to a bug in customtkinter/darkdetect that causes a hard abort on macOS 15 (build 1506), the script is Windows and Linux only for now.

# Image
<img width="945" height="1022" alt="260411_16h40m31s_screenshot" src="https://github.com/user-attachments/assets/caaadaad-b10b-4ac0-af8d-28a00e91b14c" />



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

    
    wget https://github.com/benzenma123/AI-Script-Locally/releases/download/v0.0.4-official/ai_script.py
## For Windows user:
- https://github.com/benzenma123/AI-Script-Locally/releases/download/v0.0.4-official/ai_script.py
The script will automatically create a virtual environment and install all required Python packages on first run.

# AI Models

| Model | Description | RAM Usage | Storage |
|-------|-------------|-----------|---------|
| Llama 3.2 1B | Light model for systems under 8GB RAM | ~0.81 GB | ~750 MB |
| Llama 3.2 3B | Heavier model, needs more CPU cores/RAM | 4 GB+ | ~2.0 GB |
| Gemma 2 2B | Good general model | ~1.71 GB | ~1.6 GB |
| Qwen 2.5 1.5B | Good for coding | ~1.12 GB | ~1.1 GB |
| SmolLM2 1.7B | Fast and clean | ~1.06 GB | ~1.0 GB |
| Phi-3.5 Mini | Microsoft's model | ~2.39 GB | ~2.2 GB |
| DeepSeek R1 1.5B | Reasoning model | ~2.0 GB | ~1.1 GB |
| DeepSeek R1 8B | Smart reasoning | ~6.5–7.2 GB | ~4.92 GB |
| Moondream2 | Vision model (WIP) | 2 GB+ | ~850 MB |

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
