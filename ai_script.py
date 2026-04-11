import os, sys, subprocess, venv, json, threading, platform
from datetime import datetime

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

# ── Platform detection ────────────────────────────────────────────────────────
SYSTEM   = platform.system()
IS_WIN   = SYSTEM == "Windows"
IS_LINUX = SYSTEM == "Linux"

if not IS_WIN and not IS_LINUX:
    print(f"Unsupported OS: {SYSTEM}. This script only supports Windows and Linux.")
    sys.exit(1)

# ── tkinter check (must be installed at system level) ────────────────────────
try:
    import tkinter
except ImportError:
    print("ERROR: tkinter is not installed. Install it with:")
    if IS_LINUX:
        print("  Arch/Arch-based:  sudo pacman -S tk")
        print("  Debian/Ubuntu:    sudo apt install python3-tk")
        print("  Fedora:           sudo dnf install python3-tkinter")
    elif IS_WIN:
        print("  Re-run the Python installer and enable the tcl/tk option.")
    sys.exit(1)

# ── w64devkit (Windows-only, optional) ───────────────────────────────────────
def check_requirements():
    if not IS_WIN:
        return
    root = os.getcwd()
    possible_dirs = [d for d in os.listdir(root) if os.path.isdir(d) and "w64devkit" in d.lower()]
    if possible_dirs:
        devkit_bin = os.path.abspath(os.path.join(root, possible_dirs[0], "bin"))
        if os.path.exists(devkit_bin) and devkit_bin not in os.environ["PATH"]:
            os.environ["PATH"] = devkit_bin + os.pathsep + os.environ["PATH"]
            os.environ["CC"]   = os.path.join(devkit_bin, "gcc.exe")
            os.environ["CXX"]  = os.path.join(devkit_bin, "g++.exe")

# ── venv bootstrap ────────────────────────────────────────────────────────────
def get_python_bin(venv_dir):
    if IS_WIN:
        return os.path.join(venv_dir, "Scripts", "python.exe")
    return os.path.join(venv_dir, "bin", "python")

def __import_check__(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False

def bootstrap():
    check_requirements()
    venv_dir   = os.path.join(os.getcwd(), "ai_venv")
    python_bin = get_python_bin(venv_dir)

    # Step 1: If not in venv, create it and re-launch inside it
    if sys.prefix == sys.base_prefix:
        if not os.path.exists(venv_dir):
            print("Creating virtual environment...")
            venv.create(venv_dir, with_pip=True)
        subprocess.run([python_bin, __file__] + sys.argv[1:], env=os.environ)
        sys.exit()

    # Step 2: We are inside the venv — install missing packages ONCE
    packages = {
        "rich":             "rich",
        "psutil":           "psutil",
        "llama-cpp-python": "llama_cpp",
        "huggingface-hub":  "huggingface_hub",
        "hf_transfer":      "hf_transfer",
        "Pillow":           "PIL",
        "customtkinter":    "customtkinter",
    }

    to_install = [pkg for pkg, imp in packages.items() if not __import_check__(imp)]

    if to_install:
        env_vars = os.environ.copy()
        env_vars["CMAKE_ARGS"]                = "-DGGML_VULKAN=on"
        env_vars["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
        for pkg in to_install:
            print(f"--- Installing {pkg} ---")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], env=env_vars)

    # Step 3: After install, verify — do NOT re-exec if still failing
    still_failing = [imp for pkg, imp in packages.items() if not __import_check__(imp)]
    if still_failing:
        print("\n" + "="*60)
        print("ERROR: The following packages installed but cannot be imported:")
        for imp in still_failing:
            print(f"  - {imp}")
        print(f"\nYou are running Python {sys.version}")
        print("customtkinter does not support Python 3.14 yet.")
        print("Fix: install Python 3.11 or 3.12 and run with that instead:")
        print("  python3.12 ben_ai.py")
        print("="*60)
        sys.exit(1)

# ── Main app ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bootstrap()

    import customtkinter as ctk
    import psutil
    from huggingface_hub import hf_hub_download
    from llama_cpp import Llama

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    class ZangggAI(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("BEN AI - Local Intelligence")
            self.geometry("1200x800")

            self.llm                = None
            self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.chat_history       = [{"role": "system", "content": "You are a helpful assistant."}]

            self.MODELS = {
                "Llama 3.2 1B (Text)":      {"repo": "unsloth/Llama-3.2-1B-Instruct-GGUF",           "file": "Llama-3.2-1B-Instruct-Q4_K_M.gguf"},
                "Llama 3.2 3B":             {"repo": "bartowski/Llama-3.2-3B-Instruct-GGUF",          "file": "Llama-3.2-3B-Instruct-Q4_K_M.gguf"},
                "Gemma 2 2B (Google)":      {"repo": "bartowski/gemma-2-2b-it-GGUF",                  "file": "gemma-2-2b-it-Q4_K_M.gguf"},
                "Qwen 2.5 1.5B (Code)":     {"repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",              "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf"},
                "Phi-3.5 Mini (Microsoft)": {"repo": "bartowski/Phi-3.5-mini-instruct-GGUF",          "file": "Phi-3.5-mini-instruct-Q4_K_M.gguf"},
                "SmolLM2 1.7B":             {"repo": "bartowski/SmolLM2-1.7B-Instruct-GGUF",          "file": "SmolLM2-1.7B-Instruct-Q4_K_M.gguf"},
                "DeepSeek R1 1.5B":         {"repo": "bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF",  "file": "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"},
                "DeepSeek R1 8B":           {"repo": "bartowski/DeepSeek-R1-Distill-Llama-8B-GGUF",   "file": "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf"},
                "Moondream2 (Vision)":      {"repo": "yonigozlan/moondream2-gguf",                    "file": "moondream2-text-model.gguf"},
            }

            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

            self.logo = ctk.CTkLabel(self.sidebar, text="BEN AI", font=("Segoe UI", 24, "bold"))
            self.logo.pack(pady=20)

            self.new_chat_btn = ctk.CTkButton(self.sidebar, text="+ New Chat", fg_color="transparent", border_width=1, command=self.new_chat)
            self.new_chat_btn.pack(pady=10, padx=20, fill="x")

            self.model_menu = ctk.CTkOptionMenu(self.sidebar, values=list(self.MODELS.keys()), command=self.change_model)
            self.model_menu.pack(pady=10, padx=20, fill="x")

            self.history_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
            self.history_frame.pack(fill="both", expand=True, padx=5, pady=5)

            self.ram_label = ctk.CTkLabel(self.sidebar, text="RAM: 0%", font=("Segoe UI", 12))
            self.ram_label.pack(pady=20)

            self.chat_box = ctk.CTkTextbox(self, font=("Segoe UI", 15), state="disabled", wrap="word")
            self.chat_box.grid(row=0, column=1, padx=40, pady=(40, 10), sticky="nsew")

            self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.input_frame.grid(row=1, column=1, padx=40, pady=(0, 30), sticky="ew")

            self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Message BEN AI...", height=50)
            self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
            self.entry.bind("<Return>", lambda e: self.send_click())

            self.btn = ctk.CTkButton(self.input_frame, text="Send", width=100, height=50, command=self.send_click)
            self.btn.pack(side="right")

            self.check_token()
            self.refresh_history_list()
            self.update_stats()

            if os.environ.get("HF_TOKEN"):
                self.change_model(list(self.MODELS.keys())[0])

        def check_token(self):
            config_file = "config.json"
            if os.path.exists(config_file):
                try:
                    with open(config_file, "r") as f:
                        config = json.load(f)
                        os.environ["HF_TOKEN"] = config.get("token", "")
                except Exception:
                    pass

            if not os.environ.get("HF_TOKEN"):
                dialog = ctk.CTkInputDialog(text="Paste your Hugging Face 'Read' Token:", title="HF Authentication")
                token = dialog.get_input()
                if token:
                    with open(config_file, "w") as f:
                        json.dump({"token": token}, f)
                    os.environ["HF_TOKEN"] = token

        def refresh_history_list(self):
            for widget in self.history_frame.winfo_children():
                widget.destroy()
            files = sorted([f for f in os.listdir() if f.startswith("chat_") and f.endswith(".json")], reverse=True)
            for f in files:
                btn = ctk.CTkButton(self.history_frame, text=f[5:-5], fg_color="transparent", anchor="w",
                                    command=lambda file=f: self.load_history_file(file))
                btn.pack(fill="x", pady=1)

        def new_chat(self):
            self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
            self.chat_box.configure(state="normal")
            self.chat_box.delete("1.0", "end")
            self.chat_box.configure(state="disabled")
            self.add_message("SYSTEM", "New session started.")

        def load_history_file(self, filename):
            try:
                with open(filename, "r") as f:
                    self.chat_history = json.load(f)
                self.chat_box.configure(state="normal")
                self.chat_box.delete("1.0", "end")
                for msg in self.chat_history:
                    if msg["role"] != "system":
                        self.chat_box.insert("end", f"{'YOU' if msg['role'] == 'user' else 'AI'}: {msg['content']}\n\n")
                self.chat_box.configure(state="disabled")
                self.current_session_id = filename[5:-5]
            except Exception as e:
                self.add_message("SYSTEM", f"Error: {e}")

        def change_model(self, model_name):
            threading.Thread(target=self._load_model_task, args=(model_name,), daemon=True).start()

        def _load_model_task(self, model_name):
            self.add_message("SYSTEM", f"Downloading {model_name}...")
            m_data = self.MODELS[model_name]
            try:
                path = hf_hub_download(
                    repo_id=m_data["repo"],
                    filename=m_data["file"],
                    token=os.environ.get("HF_TOKEN"),
                )
                self.llm = Llama(
                    model_path=path,
                    n_gpu_layers=35,
                    n_ctx=8192,
                    verbose=False,
                )
                self.add_message("SYSTEM", f"{model_name} is online.")
            except Exception as e:
                self.add_message("SYSTEM", f"Error loading model: {e}")

        def update_stats(self):
            self.ram_label.configure(text=f"RAM: {psutil.virtual_memory().percent}%")
            self.after(2000, self.update_stats)

        def send_click(self):
            if not self.llm:
                return
            msg = self.entry.get().strip()
            if msg:
                self.add_message("YOU", msg)
                self.entry.delete(0, "end")
                self.chat_history.append({"role": "user", "content": msg})
                threading.Thread(target=self.generate_ai, daemon=True).start()

        def generate_ai(self):
            self.add_message("AI", "...")
            response = self.llm.create_chat_completion(messages=self.chat_history)
            ans = response["choices"][0]["message"]["content"]
            self.chat_box.configure(state="normal")
            self.chat_box.delete("end-2l", "end-1l")
            self.chat_box.configure(state="disabled")
            self.add_message("AI", ans)
            self.chat_history.append({"role": "assistant", "content": ans})
            with open(f"chat_{self.current_session_id}.json", "w") as f:
                json.dump(self.chat_history, f)
            self.refresh_history_list()

        def add_message(self, sender, text):
            self.chat_box.configure(state="normal")
            self.chat_box.insert("end", f"{sender}: {text}\n\n")
            self.chat_box.configure(state="disabled")
            self.chat_box.see("end")

    app = ZangggAI()
    app.mainloop()
