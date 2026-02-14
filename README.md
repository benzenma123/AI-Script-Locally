# AI-Script-Locally
<p align="center">
    <img src="https://count.getloli.com/@benzenma123?theme=rule34" alt="Moe Counter" height="60" style="margin-center:15px;" />
  </p>


# Tested OS
![Linux](https://img.shields.io/badge/Arch_Linux-Main-1793D1?style=flat-square&logo=Arch-Linux&logoColor=white)
![macOS Catalina](https://img.shields.io/badge/macOS_Catalina-Hackintosh-000000?style=flat-square&logo=Apple&logoColor=white)
![Windows 11](https://img.shields.io/badge/Windows_11-Secondary-0078D6?style=flat-square&logo=Windows&logoColor=white)
![FreeBSD](https://img.shields.io/badge/FreeBSD-Unix-AB2B28?style=flat-square&logo=FreeBSD&logoColor=white)
# Tutorial
Here are some dependencies that u should install before run the script base on what os is your host computer, this include gpu driver for Intel (AMD & Nvidia will found later on)
  #### Windows:
  - Python: https://www.python.org/ftp/python/3.14.2/python-3.14.2-amd64.exe
  - GPU Drivers: https://www.intel.com/content/www/us/en/support/detect.html
  #### Linux (depends):
##### Gentoo Linux:
- Python: sudo emerge --ask python3
- GPU Drivers: update VIDEO_CARDS and add "vulkan" flags to USE
- GPU Drivers: emerge --ask media-libs/mesa dev-util/vulkan-tools
##### Arch/Arch-Based
- Python: sudo pacman -S python python3
- Python: yay -S python3
- GPU Drivers: sudo pacman -Syu mesa vulkan-intel intel-media-driver clinfo
##### Debian/Ubuntu
- Python: sudo apt install python3 python
- GPU Drivers: sudo apt install mesa-vulkan-drivers vulkan-tools libvulkan1
- GPU Drivers: sudo apt install intel-opencl-icd intel-level-zero-gpu
##### Fedora Linux
- Python: sudo dnf install python3
- GPU Drivers: sudo dnf install mesa-vulkan-drivers vulkan-tools
  #### MacOS:
  - Python: sudo brew install python (its usually built-in)
  - GPU Drivers: Built-in
# Tool need to Install
Here are some tool you HAVE TO install to be able to run this script (Windows only)
- Vulkan SDK: https://sdk.lunarg.com/sdk/download/1.4.341.1/windows/vulkansdk-windows-X64-1.4.341.1.exe
- CMake: https://github.com/Kitware/CMake/releases/download/v4.2.3/cmake-4.2.3-windows-x86_64.msi
- W64Devkit (required): https://github.com/skeeto/w64devkit/releases
## How to run the script
you just need to run:
```
git clone https://github.com/benzenma123/AI-Script-Locally
cd AI-Script-Locally
python3 ai_script.py
```
# Tested Kernel
![Linux Kernel](https://img.shields.io/badge/Linux-6.7.x-FFCC00?style=flat-square&logo=Linux&logoColor=black)
![FreeBSD Kernel](https://img.shields.io/badge/FreeBSD-14.x-AB2B28?style=flat-square&logo=FreeBSD&logoColor=white)
![Darwin Kernel](https://img.shields.io/badge/Darwin-XNU-000000?style=flat-square&logo=Apple&logoColor=white)
## Hints
- You can run this script (after run this script the first time for installation) without internet, just need the system had python already and plug in the power since it using gpu only mode now and it will spike a litle power
- Install the tool (W64Devkit) in the folder or else it will cause a error if install in the other place, CMake and Vulkan SDK can install in it default folder.

# AI Model
| Avalible model | Desscription | RAM Consuming | Storage Space Needed |
|----------------|--------------|---------------|----------------------|
|  Llama 3.2 1B  | Light AI Model for system under 8gb of RAM| 0.81Gb~ | ~750 MB |
|MoonDream2| Not work yet as it url had some problem| 2Gb+ | ~850 MB|
|Llama 3.2 3B| Pretty heavy AI model but needs more cpu cores/threads and RAM| 4Gb+ | ~2.0GB
|Gemma 2 2B| Pretty good AI model| 1.71Gb~ | ~1.6 GB
|Qwen 2.5 1.5B| Good AI model for coding | 1.12Gb~| ~1.1 GB
|SmolLM2 1.7B| Fast/Clean| 1.06Gb~| ~1.0 GB
|Phi 3.5 mini| Microsoft's AI| 2.39Gb~| ~2.2 GB
|Deepseek R1 1.5B (Reasoning)| Not Availible| ~2.0 GB| ~1.1 GB|
|Deepseek R1 8B (Smart Reasoning)| Not Availible| ~6.5 - 7.2 GB| 4.92 GB

# GPU Driver Not Found Solution
If the script cant find GPU then try these (linux only):
- sudo usermod -aG render,video $USER
- GGML_VULKAN_DEVICE=0
- python ai_agent.py
### Note:
Log out after running these command to take effect

# For Nvidia & AMD User
For the Nvidia & AMD fellas, if you already had GPU driver then you just need to install Tool at the other section in here
# ⚖️ License & Disclaimer
This project is for educational purposes. All models are subject to their respective creators' licenses (Meta, Google, Microsoft, Alibaba, etc.). Use responsibly. And If you do anything and getting sued, I don't care :)

# Supporter
- benzenma123 (me)
- (I will add u if u contact me and want to work with me)

# Update Log
#### 04/01/2025 20:30 log
- First time make this repo
- Had total 2 AI Model (Llama & Moondream)
#### 05/01/2025 16:30 log
- Add more AI Model (Moondream, Llama 3B, Gwen and Gemma)
- Add /clear to clear AI memory
#### 06/01/2025 15:39
- Add Deepseek R1 (1B and 8B)
- Fix error when using Gemma 
#### 2/14/2026 8:58 AM
- Fix the script
- Actually work on GPU (include IGPU of all brand x86_64 only)
- Still cannot work on other architechture yet
