import os
import sys
import subprocess
import venv
import time
import base64
from io import BytesIO

# --- 1. THE BOOTSTRAPPER ---
def bootstrap():
    venv_dir = os.path.join(os.getcwd(), "ai_venv")
    if sys.prefix == sys.base_prefix:
        if not os.path.exists(venv_dir):
            print(f"[!] Creating isolated sandbox in {venv_dir}...")
            venv.create(venv_dir, with_pip=True)
        python_bin = os.path.join(venv_dir, "bin", "python")
        subprocess.check_call([python_bin, *sys.argv])
        sys.exit()

    packages = {
        "rich": "rich", "psutil": "psutil", "duckduckgo-search": "duckduckgo_search", 
        "llama-cpp-python": "llama_cpp", "Pillow": "PIL", "huggingface-hub": "huggingface_hub"
    }
    
    to_install = [pkg for pkg, imp in packages.items() if not __import_check__(imp)]
    if to_install:
        print(f"[!] Updating sandbox: {to_install}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *to_install])
        os.execv(sys.executable, ['python'] + sys.argv)

def __import_check__(name):
    try:
        __import__(name)
        return True
    except ImportError: return False

bootstrap()

# --- 2. CORE AI ENGINE ---
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.live import Live
from rich.table import Table
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from llama_cpp.llama_chat_format import MoondreamChatHandler
from PIL import Image
import psutil

console = Console()

def get_stats():
    """Generates a real-time hardware status table."""
    mem = psutil.virtual_memory()
    table = Table(show_header=False, box=None)
    
    # Try to get VRAM via nvidia-smi if available
    vram_str = "VRAM: N/A"
    try:
        res = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
        if res.returncode == 0:
            used, total = res.stdout.strip().split(',')
            vram_str = f"VRAM: {used.strip()}/{total.strip()} MB"
    except: pass

    table.add_row(f"[bold cyan]RAM:[/] {mem.percent}%", f"[bold magenta]{vram_str}[/]")
    return table

MODELS = MODELS = [
    {"name": "Llama 3.2 1B (Text)", "repo": "unsloth/Llama-3.2-1B-Instruct-GGUF", "file": "Llama-3.2-1B-Instruct-Q4_K_M.gguf"},
    {"name": "Llama 3.2 3B", "repo": "bartowski/Llama-3.2-3B-Instruct-GGUF", "file": "Llama-3.2-3B-Instruct-Q4_K_M.gguf"},
    {"name": "Gemma 2 2B (Google - The 2B King)", "repo": "bartowski/gemma-2-2b-it-GGUF", "file": "gemma-2-2b-it-Q4_K_M.gguf"},
    {"name": "Qwen 2.5 1.5B (Logic/Code)", "repo": "Qwen/Qwen2.5-1.5B-Instruct-GGUF", "file": "qwen2.5-1.5b-instruct-q4_k_m.gguf"},
    {"name": "Phi-3.5 Mini (Microsoft)", "repo": "bartowski/Phi-3.5-mini-instruct-GGUF", "file": "Phi-3.5-mini-instruct-Q4_K_M.gguf"},
    {"name": "SmolLM2 1.7B (Fast & Clean)", "repo": "bartowski/SmolLM2-1.7B-Instruct-GGUF", "file": "SmolLM2-1.7B-Instruct-Q4_K_M.gguf"},
    {
        "name": "Moondream2 (Vision Engine - Fast)", 
        "repo": "yonigozlan/moondream2-gguf", 
        "file": "moondream2-text-model.gguf", 
        "proj": "moondream2-mmproj.gguf"
    }
]
def main():
    console.print(Panel("SYSTEM MONITOR ACTIVE", title="[bold green]AI HUB[/]"))
    console.print(get_stats())
    
    for i, m in enumerate(MODELS):
        console.print(f" {i+1}. {m['name']}")
    
    choice = IntPrompt.ask("\nSelect Engine", choices=[str(i+1) for i in range(len(MODELS))]) - 1
    selected = MODELS[choice]

    with console.status("[yellow]Downloading/Loading Model..."):
        path = hf_hub_download(selected['repo'], selected['file'])
        proj = hf_hub_download(selected['repo'], selected['proj']) if "proj" in selected else None
        handler = MoondreamChatHandler(clip_model_path=proj) if proj else None
        
        # Load with GPU Layers set to -1 (attempts GPU offload)
        llm = Llama(model_path=path, chat_handler=handler, n_gpu_layers=-1, n_ctx=2048, verbose=False)

    console.print("[green]✓ Ready. Prefix '?' to search or enter an image path.[/]")

    while True:
        console.print(get_stats())
        query = Prompt.ask("\n[bold cyan]>>>[/]").strip()
        if query.lower() in ["exit", "quit"]: break
        
        img_b64 = None
        if any(query.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
            fpath = query.strip("'").strip('"')
            if os.path.exists(fpath):
                img = Image.open(fpath)
                buf = BytesIO()
                img.save(buf, format="JPEG")
                img_b64 = f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"
                query = "Describe this image."

        with console.status("[magenta]AI is processing..."):
            # FIXED LOGIC: Send simple text for Llama 1B, only use complex Dict for Vision
            if not img_b64:
                # Use simple completion for small models to avoid structure confusion
                output = llm(f"User: {query}\nAssistant:", max_tokens=512, stop=["User:"])
                res = output["choices"][0]["text"].strip()
            else:
                messages = [{"role": "user", "content": [{"type": "text", "text": query}, {"type": "image_url", "image_url": {"url": img_b64}}]}]
                res = llm.create_chat_completion(messages=messages)["choices"][0]["message"]["content"]
        
        console.print(Panel(res, title="Response", border_style="blue", subtitle=f"Using {selected['name']}"))

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\nBye!")
