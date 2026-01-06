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
Here are some thing that u should install before run the script base on what os is your host computer, this include gpu driver for AMD and Intel
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
- You can run this script (after run this script the first time for installation) without internet, just need the system had python already and plug in the power since it using cpu only mode and might comsum a lot of energy and cpu cores/threads

# AI Model
| Avalible model | Desscription | RAM Consuming |
|----------------|--------------|---------------|
|  Llama 3.2 1B  | Light AI Model for system under 8gb of RAM| 0.81Gb~ |
|MoonDream2| Not work yet as it url had some problem| 2Gb+ |
|Llama 3.2 3B| Pretty heavy AI model but needs more cpu cores/threads and RAM| 4Gb+
|Gemma 2 2B| Pretty good AI model| 1.71Gb~ 
|Qwen 2.5 1.5B| Good AI model for coding | 1.12Gb~
|SmolLM2 1.7B| Fast/Clean| 1.06Gb~
|Phi 3.5 mini| Microsoft's AI| 2.39Gb~

# GPU Driver Not Found Solution
If the script cant find GPU then try these (linux only):
- sudo usermod -aG render,video $USER
- GGML_VULKAN_DEVICE=0
- python ai_agent.py
### Note:
Log out after running these command to take effect

# Decleration
For AMD-Based system, downloads driver for AMD by yourself because im tired and dont have time for this. Sorry AMD Users

# ⚖️ License & Disclaimer
This project is for educational purposes. All models are subject to their respective creators' licenses (Meta, Google, Microsoft, Alibaba, etc.). Use responsibly. And If you do anything and getting sued, I don't care :)
