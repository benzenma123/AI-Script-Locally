import os, sys, subprocess, venv, time, json

def check_requirements():
    """Automatically finds w64devkit and sets the PATH for this session."""
    root = os.getcwd()
    possible_dirs = [d for d in os.listdir(root) if os.path.isdir(d) and "w64devkit" in d.lower()]
    
    if possible_dirs:
        devkit_bin = os.path.abspath(os.path.join(root, possible_dirs[0], "bin"))
        if os.path.exists(devkit_bin):
            if devkit_bin not in os.environ["PATH"]:
                os.environ["PATH"] = devkit_bin + os.pathsep + os.environ["PATH"]
                os.environ["CC"] = os.path.join(devkit_bin, "gcc.exe")
                os.environ["CXX"] = os.path.join(devkit_bin, "g++.exe")
                print(f"[✓] Toolchain linked: {devkit_bin}")

    gcc_check = subprocess.run(["where", "gcc"], capture_output=True, text=True)
    if gcc_check.returncode != 0:
        print("\n[!] COMPILER NOT FOUND. Place 'w64devkit' in this folder.")
        sys.exit(1)
    print(f"[✓] Compiler verified: {gcc_check.stdout.splitlines()[0]}")

def bootstrap():
    check_requirements() 
    venv_dir = os.path.join(os.getcwd(), "ai_venv")
    python_bin = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "python")
    
    if sys.prefix == sys.base_prefix:
        if not os.path.exists(venv_dir):
            print(f"[!] Creating virtual environment...")
            venv.create(venv_dir, with_pip=True)
        subprocess.run([python_bin, __file__] + sys.argv[1:], env=os.environ)
        sys.exit()

    packages = {"rich": "rich", "psutil": "psutil", "llama-cpp-python": "llama_cpp", "huggingface-hub": "huggingface_hub", "Pillow": "PIL"}
    to_install = [pkg for pkg, imp in packages.items() if not __import_check__(imp)]
    
    if to_install:
        print(f"[!] Installing dependencies (Vulkan-ready): {to_install}")
        env_vars = os.environ.copy()
        env_vars["CMAKE_GENERATOR"] = "MinGW Makefiles" 
        env_vars["CMAKE_ARGS"] = "-DGGML_VULKAN=on"
        env_vars["FORCE_CMAKE"] = "1"
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        for pkg in to_install:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg], env=env_vars)
        os.execv(sys.executable, ['python', __file__] + sys.argv[1:])

def __import_check__(name):
    try: __import__(name); return True
    except ImportError: return False

if __name__ == "__main__":
    bootstrap()
    
    # Modern terminal fix for Windows
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)

    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from huggingface_hub import hf_hub_download
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import MoondreamChatHandler
    from PIL import Image
    import psutil

    console = Console()
    MODELS = [
    {"name": "Llama 3.2 1B (Text)", "repo": "unsloth/Llama-3.2-1B-Instruct-GGUF", "file": "Llama-3.2-1B-Instruct-Q4_K_M.gguf", "vram": "Light"},
    {"name": "Llama 3.2 3B", "repo": "bartowski/Llama-3.2-3B-Instruct-GGUF", "file": "Llama-3.2-3B-Instruct-Q4_K_M.gguf", "vram": "Medium"},
    {"name": "Gemma 2 2B (Google - The 2B King)", "repo": "bartowski/gemma-2-2b-it-GGUF", "file": "gemma-2-2b-it-Q4_K_M.gguf", "vram": "Medium"},
    {"name": "Qwen 2.5 1.5B (Logic/Code)", "repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF", "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf", "vram": "Light"},
    {"name": "Phi-3.5 Mini (Microsoft)", "repo": "bartowski/Phi-3.5-mini-instruct-GGUF", "file": "Phi-3.5-mini-instruct-Q4_K_M.gguf", "vram": "Medium"},
    {"name": "SmolLM2 1.7B (Fast & Clean)", "repo": "bartowski/SmolLM2-1.7B-Instruct-GGUF", "file": "SmolLM2-1.7B-Instruct-Q4_K_M.gguf", "vram": "Light"},
    {"name": "DeepSeek R1 1.5B (Reasoning)", "repo": "bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF", "file": "DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf", "vram": "Light"},
    {"name": "DeepSeek R1 8B (Smart Reasoning)", "repo": "bartowski/DeepSeek-R1-Distill-Llama-8B-GGUF", "file": "DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf", "vram": "Heavy"},
    {
        "name": "Moondream2 (Vision Engine - Fast)", 
        "repo": "yonigozlan/moondream2-gguf", 
        "file": "moondream2-text-model.gguf", 
        "proj": "moondream2-mmproj.gguf",
        "vram": "Medium"
    }
]

    def get_stats():
        mem = psutil.virtual_memory()
        table = Table(show_header=False, box=None)
        backend = "CPU (Slow)"
        try:
            from llama_cpp import llama_cpp as lc
            info = lc.llama_print_system_info().decode()
            if "VULKAN" in info: backend = "Vulkan (iGPU Active)"
        except: pass
        table.add_row(f"[bold cyan]RAM:[/] {mem.percent}%", f"[bold magenta]Engine:[/] {backend}")
        return table

    def main_logic():
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel.fit("AI SELECTION MENU", title="[bold green]BEN AIIIIIII[/]"))
        console.print(get_stats())
        
        # --- MEMORY LOADING ---
        memory_file = "chat_history.json"
        if os.path.exists(memory_file):
            with open(memory_file, "r") as f:
                chat_history = json.load(f)
            console.print(f"[dim]Loaded {len(chat_history)} messages from memory.json[/]")
        else:
            chat_history = [{"role": "system", "content": "You are a helpful assistant."}]

        for i, m in enumerate(MODELS):
            console.print(f" [bold green]{i+1}.[/] {m['name']} [dim]({m['vram']})[/]")
        
        choice_idx = IntPrompt.ask("\nSelect Engine", choices=[str(i+1) for i in range(len(MODELS))]) - 1
        selected = MODELS[choice_idx]

        with console.status(f"[yellow]Launching {selected['name']}..."):
            path = hf_hub_download(selected['repo'], selected['file'])
            proj = hf_hub_download(selected['repo'], selected['proj']) if "proj" in selected else None
            handler = MoondreamChatHandler(clip_model_path=proj) if proj else None
            # Set higher n_ctx (4096) for longer memory
            llm = Llama(model_path=path, chat_handler=handler, n_gpu_layers=35, n_ctx=4096, verbose=False)

        console.print(f"[green]✓ System Online. Type 'clear' to reset memory.[/]")

        while True:
            query = Prompt.ask("\n[bold cyan]YOU[/]").strip()
            if query.lower() in ["exit", "quit"]: break
            if query.lower() == "clear":
                chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
                if os.path.exists(memory_file): os.remove(memory_file)
                console.print("[yellow]Memory wiped![/]")
                continue
            
            chat_history.append({"role": "user", "content": query})
            
            with console.status("[magenta]Thinking..."):
                response = llm.create_chat_completion(messages=chat_history, max_tokens=512)
                ans = response["choices"][0]["message"]["content"]
            
            chat_history.append({"role": "assistant", "content": ans})
            
            # --- AUTO-SAVE ---
            with open(memory_file, "w") as f:
                json.dump(chat_history, f, indent=4)
            
            console.print(Panel(ans, title="AI Response", border_style="green"))

    try:
        main_logic()
    except KeyboardInterrupt:
        print("\nStopped.")
