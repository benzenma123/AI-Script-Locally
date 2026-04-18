# Do not use this file, its decripricated
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

    if sys.prefix == sys.base_prefix:
        if not os.path.exists(venv_dir):
            print("Creating virtual environment...")
            venv.create(venv_dir, with_pip=True)
        subprocess.run([python_bin, __file__] + sys.argv[1:], env=os.environ)
        sys.exit()

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

    still_failing = [imp for pkg, imp in packages.items() if not __import_check__(imp)]
    if still_failing:
        print("\n" + "="*60)
        print("ERROR: The following packages installed but cannot be imported:")
        for imp in still_failing:
            print(f"  - {imp}")
        print(f"\nYou are running Python {sys.version}")
        print("Fix: use Python 3.12 instead:")
        print("  python3.12 ben_ai.py")
        print("="*60)
        sys.exit(1)

# ── Mode selection ────────────────────────────────────────────────────────────
def ask_mode():
    print()
    print("╔══════════════════════════════╗")
    print("║       BEN AI - Launcher      ║")
    print("╠══════════════════════════════╣")
    print("║  [1] GUI  - Graphical mode   ║")
    print("║  [2] TUI  - Terminal mode    ║")
    print("╚══════════════════════════════╝")
    print()
    while True:
        choice = input("Select mode (1/2): ").strip()
        if choice == "1":
            return "gui"
        elif choice == "2":
            return "tui"
        else:
            print("Invalid choice, enter 1 or 2.")

# ── Shared model list ─────────────────────────────────────────────────────────
MODELS = {
    "1": {"name": "Llama 3.2 1B (Text)",      "repo": "unsloth/Llama-3.2-1B-Instruct-GGUF",          "file": "Llama-3.2-1B-Instruct-Q4_K_M.gguf"},
    "2": {"name": "Llama 3.2 3B",             "repo": "bartowski/Llama-3.2-3B-Instruct-GGUF",         "file": "Llama-3.2-3B-Instruct-Q4_K_M.gguf"},
    "3": {"name": "Gemma 2 2B (Google)",       "repo": "bartowski/gemma-2-2b-it-GGUF",                 "file": "gemma-2-2b-it-Q4_K_M.gguf"},
    "4": {"name": "Qwen 2.5 1.5B (Code)",      "repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF",             "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf"},
    "5": {"name": "Phi-3.5 Mini (Microsoft)",  "repo": "bartowski/Phi-3.5-mini-instruct-GGUF",         "file": "Phi-3.5-mini-instruct-Q4_K_M.gguf"},
    "6": {"name": "SmolLM2 1.7B",              "repo": "bartowski/SmolLM2-1.7B-Instruct-GGUF",         "file": "SmolLM2-1.7B-Instruct-Q4_K_M.gguf"},
    "7": {"name": "DeepSeek R1 1.5B",          "repo": "bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF", "file": "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf"},
    "8": {"name": "DeepSeek R1 8B",            "repo": "bartowski/DeepSeek-R1-Distill-Llama-8B-GGUF",  "file": "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf"},
    "9":  {"name": "Moondream2 (Vision)",        "repo": "yonigozlan/moondream2-gguf",                          "file": "moondream2-text-model.gguf"},
    "10": {"name": "Qwen 2.5 Coder 1.5B",        "repo": "Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF",              "file": "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"},
    "11": {"name": "Mistral 7B",                  "repo": "bartowski/Mistral-7B-Instruct-v0.3-GGUF",             "file": "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"},
    "12": {"name": "TinyLlama 1.1B",              "repo": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",             "file": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"},
}

# ── TUI mode ──────────────────────────────────────────────────────────────────
def run_tui():
    import psutil
    from huggingface_hub import hf_hub_download
    from llama_cpp import Llama

    # Token check
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                os.environ["HF_TOKEN"] = json.load(f).get("token", "")
        except Exception:
            pass

    if not os.environ.get("HF_TOKEN"):
        token = input("Paste your Hugging Face 'Read' Token: ").strip()
        if token:
            with open(config_file, "w") as f:
                json.dump({"token": token}, f)
            os.environ["HF_TOKEN"] = token

    # Model selection
    print()
    print("Available models:")
    for k, v in MODELS.items():
        print(f"  [{k}] {v['name']}")
    print()
    while True:
        choice = input("Select model (1-12): ").strip()
        if choice in MODELS:
            break
        print("Invalid choice.")

    model = MODELS[choice]
    print(f"\nDownloading {model['name']}...")
    path = hf_hub_download(
        repo_id=model["repo"],
        filename=model["file"],
        token=os.environ.get("HF_TOKEN"),
    )
    print(f"{model['name']} is online.\n")

    llm = Llama(model_path=path, n_gpu_layers=35, n_ctx=8192, verbose=False)

    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    session_id   = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("Type your message and press Enter. Type 'exit' to quit, 'new' for a new chat.\n")
    print("─" * 60)

    while True:
        try:
            user_input = input("YOU: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if user_input.lower() == "new":
            chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
            session_id   = datetime.now().strftime("%Y%m%d_%H%M%S")
            print("\n[New session started]\n" + "─" * 60)
            continue
        if not user_input:
            continue

        chat_history.append({"role": "user", "content": user_input})

        print("AI: ", end="", flush=True)
        full_response = ""
        for chunk in llm.create_chat_completion(messages=chat_history, stream=True):
            token = chunk["choices"][0]["delta"].get("content", "")
            if token:
                print(token, end="", flush=True)
                full_response += token
        print("\n" + "─" * 60)

        chat_history.append({"role": "assistant", "content": full_response})
        with open(f"chat_{session_id}.json", "w") as f:
            json.dump(chat_history, f)

# ── GUI mode ──────────────────────────────────────────────────────────────────
def run_gui():
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

            self.GUI_MODELS = {v["name"]: {"repo": v["repo"], "file": v["file"]} for v in MODELS.values()}

            # chat_boxes: dict of session_id -> CTkTextbox
            # chat_histories: dict of session_id -> list of messages
            self.chat_boxes     = {}
            self.chat_histories = {}
            self.active_box     = None

            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
            self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

            self.logo = ctk.CTkLabel(self.sidebar, text="BEN AI", font=("Segoe UI", 24, "bold"))
            self.logo.pack(pady=20)

            self.new_chat_btn = ctk.CTkButton(self.sidebar, text="+ New Chat", fg_color="transparent", border_width=1, command=self.new_chat)
            self.new_chat_btn.pack(pady=10, padx=20, fill="x")

            self.model_menu = ctk.CTkOptionMenu(self.sidebar, values=list(self.GUI_MODELS.keys()), command=self.change_model)
            self.model_menu.pack(pady=10, padx=20, fill="x")

            self.history_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
            self.history_frame.pack(fill="both", expand=True, padx=5, pady=5)

            self.ram_label = ctk.CTkLabel(self.sidebar, text="RAM: 0%", font=("Segoe UI", 12))
            self.ram_label.pack(pady=20)

            # chat area — boxes are placed here and swapped on session switch
            self.chat_area = ctk.CTkFrame(self, fg_color="transparent")
            self.chat_area.grid(row=0, column=1, padx=40, pady=(40, 10), sticky="nsew")
            self.chat_area.grid_rowconfigure(0, weight=1)
            self.chat_area.grid_columnconfigure(0, weight=1)

            self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
            self.input_frame.grid(row=1, column=1, padx=40, pady=(0, 30), sticky="ew")

            self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Message BEN AI...", height=50)
            self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
            self.entry.bind("<Return>", lambda e: self.send_click())

            self.btn = ctk.CTkButton(self.input_frame, text="Send", width=100, height=50, command=self.send_click)
            self.btn.pack(side="right")

            self.check_token()
            self.new_chat()
            self.refresh_history_list()
            self.update_stats()

            if os.environ.get("HF_TOKEN"):
                self.change_model(list(self.GUI_MODELS.keys())[0])

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

        def _make_box(self):
            box = ctk.CTkTextbox(self.chat_area, font=("Segoe UI", 15), state="disabled", wrap="word")
            box.grid(row=0, column=0, sticky="nsew")
            return box

        def _switch_to(self, session_id):
            if self.active_box is not None:
                self.active_box.grid_remove()
            self.current_session_id = session_id
            self.chat_history       = self.chat_histories[session_id]
            self.active_box         = self.chat_boxes[session_id]
            self.active_box.grid()

        def refresh_history_list(self):
            for widget in self.history_frame.winfo_children():
                widget.destroy()
            files = sorted([f for f in os.listdir() if f.startswith("chat_") and f.endswith(".json")], reverse=True)
            for f in files:
                btn = ctk.CTkButton(self.history_frame, text=f[5:-5], fg_color="transparent", anchor="w",
                                    command=lambda file=f: self.load_history_file(file))
                btn.pack(fill="x", pady=1)

        def new_chat(self):
            sid     = datetime.now().strftime("%Y%m%d_%H%M%S")
            history = [{"role": "system", "content": "You are a helpful assistant."}]
            box     = self._make_box()
            self.chat_boxes[sid]     = box
            self.chat_histories[sid] = history
            self._switch_to(sid)
            self.add_message("SYSTEM", "New session started.")
            self.refresh_history_list()

        def load_history_file(self, filename):
            sid = filename[5:-5]
            try:
                if sid in self.chat_boxes:
                    self._switch_to(sid)
                    return
                with open(filename, "r") as f:
                    history = json.load(f)
                box = self._make_box()
                self.chat_boxes[sid]     = box
                self.chat_histories[sid] = history
                self._switch_to(sid)
                box.configure(state="normal")
                for msg in history:
                    if msg["role"] != "system":
                        box.insert("end", f"{'YOU' if msg['role'] == 'user' else 'AI'}: {msg['content']}\n\n")
                box.configure(state="disabled")
                box.see("end")
            except Exception as e:
                self.add_message("SYSTEM", f"Error: {e}")

        def change_model(self, model_name):
            threading.Thread(target=self._load_model_task, args=(model_name,), daemon=True).start()

        def _load_model_task(self, model_name):
            self.add_message("SYSTEM", f"Downloading {model_name}...")
            m_data = self.GUI_MODELS[model_name]
            try:
                path = hf_hub_download(
                    repo_id=m_data["repo"],
                    filename=m_data["file"],
                    token=os.environ.get("HF_TOKEN"),
                )
                self.llm = Llama(model_path=path, n_gpu_layers=35, n_ctx=8192, verbose=False)
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
            box = self.active_box
            box.configure(state="normal")
            box.insert("end", "AI: ")
            box.configure(state="disabled")
            box.see("end")

            full_response = ""
            for chunk in self.llm.create_chat_completion(messages=self.chat_history, stream=True):
                token = chunk["choices"][0]["delta"].get("content", "")
                if token:
                    full_response += token
                    box.configure(state="normal")
                    box.insert("end", token)
                    box.configure(state="disabled")
                    box.see("end")

            box.configure(state="normal")
            box.insert("end", "\n\n")
            box.configure(state="disabled")

            self.chat_history.append({"role": "assistant", "content": full_response})
            with open(f"chat_{self.current_session_id}.json", "w") as f:
                json.dump(self.chat_history, f)
            self.refresh_history_list()

        def add_message(self, sender, text):
            box = self.active_box
            if box is None:
                return
            box.configure(state="normal")
            box.insert("end", f"{sender}: {text}\n\n")
            box.configure(state="disabled")
            box.see("end")

    app = ZangggAI()
    app.mainloop()

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    bootstrap()
    mode = ask_mode()
    if mode == "tui":
        run_tui()
    else:
        run_gui()


