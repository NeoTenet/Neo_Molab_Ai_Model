import marimo

__generated_with = "0.0.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(r"""
    # 💎 NeoTenet MoLab — Wan 2.2 14B I2V

    اسکریپت اصلی راه‌اندازی Wan 2.2 تصویر به ویدئو با رابط Gradio و تونل عمومی.

    **سازنده: NeoTenet · [T.me/NeoTenet](https://t.me/NeoTenet)**

    کد منبع اصلی در این فایل جاسازی شده و هنگام اجرا عیناً به فایل موقت پایتون نوشته می‌شود؛ سپس در پردازش جداگانه اجرا می‌شود تا محیط marimo قفل نشود. محتوای اسکریپت اصلی بازنویسی نشده است.

    > برای اجرای مدل، محیط باید GPU سازگار، اینترنت و امکان نصب وابستگی‌ها داشته باشد. اجرای اسکریپت می‌تواند حجم زیادی از بسته‌ها و وزن‌های مدل را دریافت کند.
    """)
    start_button = mo.ui.run_button(label="▶️ اجرای مدل")
    stop_button = mo.ui.run_button(label="⏹ توقف مدل")
    refresh_button = mo.ui.run_button(label="🔄 تازه‌سازی لاگ")
    mo.hstack([start_button, stop_button, refresh_button], justify="start")
    return mo, start_button, stop_button, refresh_button


@app.cell
def _(start_button):
    # Original source code as exact logical lines; joined text is byte-identical after UTF-8 encoding.
    source_lines = [
        '# @title Wan 2.2 14B I2V Studio (ftfy & Video Modules Fixed)\r\n',
        '# @markdown Adds ftfy, imageio, and ffmpeg dependencies to allow smooth video rendering and export.\r\n',
        '\r\n',
        'import os\r\n',
        'import sys\r\n',
        'import time\r\n',
        'import urllib.request\r\n',
        'import subprocess\r\n',
        'import threading\r\n',
        'import site\r\n',
        'import torch\r\n',
        '\r\n',
        'def run_cmd(cmd):\r\n',
        '    subprocess.run(cmd, shell=True)\r\n',
        '\r\n',
        'print("═" * 65)\r\n',
        'print("🎬 LAUNCHING WAN 2.2 14B (Rchoks/wan555) - DUAL-RAM ENGINE")\r\n',
        'print("═" * 65)\r\n',
        '\r\n',
        'if not torch.cuda.is_available():\r\n',
        '    raise SystemError("⚠️ GPU acceleration required! Ensure GPU runtime is active.")\r\n',
        '\r\n',
        '# ۱. پیکربندی حافظه و محیط اجرایی\r\n',
        'os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True,garbage_collection_threshold:0.8"\r\n',
        'os.environ["PYTHONUNBUFFERED"] = "1"\r\n',
        'os.environ["TOKENIZERS_PARALLELISM"] = "true"\r\n',
        'torch.backends.cuda.matmul.allow_tf32 = True\r\n',
        'torch.backends.cudnn.allow_tf32 = True\r\n',
        '\r\n',
        'vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)\r\n',
        'print(f"• Dedicated VRAM : {vram_gb:.2f} GB")\r\n',
        'print("• Memory Mode    : Dual-RAM Hybrid (CPU RAM + GPU VRAM Offload)")\r\n',
        '\r\n',
        '# آزادسازی پورت\u200cها\r\n',
        'run_cmd("fuser -k 7860/tcp > /dev/null 2>&1 || true")\r\n',
        'time.sleep(1)\r\n',
        '\r\n',
        '# ۲. کلون مخزن رسمی Rchoks/wan555\r\n',
        "WAN_DIR = '/content/wan555_app'\r\n",
        "os.makedirs('/content', exist_ok=True)\r\n",
        '\r\n',
        'if not os.path.exists(WAN_DIR):\r\n',
        '    print("\\n📥 در حال دانلود مخزن رسمی Rchoks/wan555 از هاگینگ\u200cفیس...")\r\n',
        '    run_cmd(f"git clone https://huggingface.co/spaces/Rchoks/wan555 {WAN_DIR}")\r\n',
        '\r\n',
        'os.chdir(WAN_DIR)\r\n',
        '\r\n',
        '# ۳. نصب تمام پیش\u200cنیازها به همراه ftfy و ماژول\u200cهای ویدیویی (حل خطای ftfy)\r\n',
        'print("\\n📦 در حال نصب و آپدیت پیش\u200cنیازها (ftfy, imageio, diffusers)...")\r\n',
        'run_cmd(\r\n',
        '    f"{sys.executable} -m pip install -q --upgrade "\r\n',
        '    f"ftfy imageio imageio-ffmpeg av "\r\n',
        '    f"git+https://github.com/huggingface/diffusers.git "\r\n',
        '    f"transformers accelerate torchvision pillow gradio pinggy torchao sentencepiece protobuf"\r\n',
        ')\r\n',
        '\r\n',
        '# ۴. رفع قطعی خطای spaces و ساخت پکیج spaces.zero\r\n',
        'SPACES_SHIM = """\r\n',
        'class _ZeroAOTI:\r\n',
        '    class ZeroGPUCompiledModel:\r\n',
        '        pass\r\n',
        '\r\n',
        'class _ZeroTorch:\r\n',
        '    aoti = _ZeroAOTI()\r\n',
        '\r\n',
        'class _Zero:\r\n',
        '    torch = _ZeroTorch()\r\n',
        '\r\n',
        'zero = _Zero()\r\n',
        '\r\n',
        'def GPU(func=None, **kwargs):\r\n',
        '    def decorator(fn):\r\n',
        '        return fn\r\n',
        '    if callable(func):\r\n',
        '        return func\r\n',
        '    return decorator\r\n',
        '\r\n',
        'def aoti_load(model=None, *args, **kwargs):\r\n',
        '    return model\r\n',
        '\r\n',
        'def aoti_blocks_load(*args, **kwargs):\r\n',
        '    pass\r\n',
        '\r\n',
        'def __getattr__(name):\r\n',
        '    def _fallback(first=None, *args, **kwargs):\r\n',
        '        return first\r\n',
        '    return _fallback\r\n',
        '"""\r\n',
        '\r\n',
        'spaces_dir = os.path.join(WAN_DIR, "spaces")\r\n',
        'os.makedirs(spaces_dir, exist_ok=True)\r\n',
        'with open(os.path.join(spaces_dir, "__init__.py"), "w", encoding="utf-8") as f:\r\n',
        '    f.write(SPACES_SHIM)\r\n',
        '\r\n',
        'with open(os.path.join(WAN_DIR, "spaces.py"), "w", encoding="utf-8") as f:\r\n',
        '    f.write(SPACES_SHIM)\r\n',
        '\r\n',
        'for sp in site.getsitepackages():\r\n',
        '    try:\r\n',
        '        sp_pkg = os.path.join(sp, "spaces")\r\n',
        '        os.makedirs(sp_pkg, exist_ok=True)\r\n',
        '        with open(os.path.join(sp_pkg, "__init__.py"), "w", encoding="utf-8") as f:\r\n',
        '            f.write(SPACES_SHIM)\r\n',
        '        with open(os.path.join(sp_pkg, "spaces.py"), "w", encoding="utf-8") as f:\r\n',
        '            f.write(SPACES_SHIM)\r\n',
        '    except Exception:\r\n',
        '        pass\r\n',
        '\r\n',
        '# ۵. خنثی\u200cسازی کامل aoti.py\r\n',
        'aoti_dummy = """\r\n',
        'class ZeroGPUCompiledModel:\r\n',
        '    pass\r\n',
        '\r\n',
        'def aoti_blocks_load(*args, **kwargs):\r\n',
        '    pass\r\n',
        '\r\n',
        'def aoti_load(model=None, *args, **kwargs):\r\n',
        '    return model\r\n',
        '\r\n',
        'def __getattr__(name):\r\n',
        '    def _fallback(first=None, *args, **kwargs):\r\n',
        '        return first\r\n',
        '    return _fallback\r\n',
        '"""\r\n',
        'with open(os.path.join(WAN_DIR, "aoti.py"), "w", encoding="utf-8") as f:\r\n',
        '    f.write(aoti_dummy)\r\n',
        '\r\n',
        '# ۶. باینری frpc برای لینک گرادیو\r\n',
        'try:\r\n',
        '    import gradio\r\n',
        '    g_dir = os.path.dirname(gradio.__file__)\r\n',
        '    frpc_file = os.path.join(g_dir, "frpc_linux_amd64_v0.3")\r\n',
        '    if not os.path.exists(frpc_file):\r\n',
        '        run_cmd(f"curl -fsSL https://cdn-media.huggingface.co/frpc-subdomain/assets/frpc_linux_amd64 -o {frpc_file} && chmod +x {frpc_file}")\r\n',
        'except Exception:\r\n',
        '    pass\r\n',
        '\r\n',
        '# ۷. پیکربندی Dual-RAM و حذف سانسور\r\n',
        'print("\\n⚙️ Configuring Dual-RAM memory split and uncensored generation...")\r\n',
        "app_file = os.path.join(WAN_DIR, 'app.py')\r\n",
        '\r\n',
        "with open(app_file, 'r', encoding='utf-8') as f:\r\n",
        '    code = f.read()\r\n',
        '\r\n',
        'code = code.replace(".to(\'cuda\')", "")\r\n',
        'code = code.replace(\'.to("cuda")\', "")\r\n',
        '\r\n',
        'if "pipe.enable_model_cpu_offload()" not in code:\r\n',
        '    injection = """\r\n',
        'pipe.enable_model_cpu_offload()\r\n',
        "if hasattr(pipe, 'vae') and hasattr(pipe.vae, 'enable_tiling'):\r\n",
        '    pipe.vae.enable_tiling()\r\n',
        "if hasattr(pipe, 'safety_checker'):\r\n",
        '    pipe.safety_checker = None\r\n',
        '"""\r\n',
        '    if "original_scheduler =" in code:\r\n',
        '        code = code.replace("original_scheduler =", injection + "\\noriginal_scheduler =")\r\n',
        '\r\n',
        'if "demo.queue().launch(" in code:\r\n',
        '    code = code.replace("demo.queue().launch(", "demo.queue().launch(share=True, server_name=\'0.0.0.0\', server_port=7860, inbrowser=False, ")\r\n',
        'elif "demo.launch(" in code:\r\n',
        '    code = code.replace("demo.launch(", "demo.launch(share=True, server_name=\'0.0.0.0\', server_port=7860, inbrowser=False, ")\r\n',
        '\r\n',
        "with open(app_file, 'w', encoding='utf-8') as f:\r\n",
        '    f.write(code)\r\n',
        '\r\n',
        'print("✅ ftfy ready, Dual-RAM configured!")\r\n',
        '\r\n',
        '# ۸. اجرای سرور گرادیو\r\n',
        'print("\\n" + "═" * 65)\r\n',
        'print("🚀 STARTING WAN 2.2 ENGINE & GRADIO SERVER...")\r\n',
        'print("═" * 65 + "\\n")\r\n',
        '\r\n',
        'proc = subprocess.Popen(\r\n',
        '    [sys.executable, "-u", "app.py"],\r\n',
        '    stdout=subprocess.PIPE,\r\n',
        '    stderr=subprocess.STDOUT,\r\n',
        '    text=True,\r\n',
        '    env=os.environ\r\n',
        ')\r\n',
        '\r\n',
        'def log_stream():\r\n',
        '    for line in proc.stdout:\r\n',
        '        print(line, end="", flush=True)\r\n',
        '\r\n',
        'threading.Thread(target=log_stream, daemon=True).start()\r\n',
        '\r\n',
        '# ۹. تست سلامت پورت ۷۸۶۰ و ساخت لینک پینگی\r\n',
        'server_ready = False\r\n',
        'for _ in range(150):\r\n',
        '    time.sleep(2)\r\n',
        '    try:\r\n',
        '        with urllib.request.urlopen("http://127.0.0.1:7860", timeout=2) as resp:\r\n',
        '            if resp.status == 200:\r\n',
        '                server_ready = True\r\n',
        '                print("\\n✅ سرور با موفقیت فعال شد!")\r\n',
        '                break\r\n',
        '    except Exception:\r\n',
        '        pass\r\n',
        '\r\n',
        'import pinggy\r\n',
        'try:\r\n',
        '    tunnel = pinggy.start_tunnel(forwardto="localhost:7860", force=True)\r\n',
        'except Exception:\r\n',
        '    tunnel = pinggy.start_tunnel(forwardto="localhost:7860")\r\n',
        '\r\n',
        'pinggy_url = None\r\n',
        'for _ in range(25):\r\n',
        '    if hasattr(tunnel, "urls") and tunnel.urls:\r\n',
        '        for u in tunnel.urls:\r\n',
        '            if u.startswith("https://") and "dashboard" not in u:\r\n',
        '                pinggy_url = u\r\n',
        '                break\r\n',
        '    if pinggy_url:\r\n',
        '        break\r\n',
        '    time.sleep(1)\r\n',
        '\r\n',
        'if not pinggy_url and hasattr(tunnel, "urls") and tunnel.urls:\r\n',
        '    pinggy_url = tunnel.urls[0]\r\n',
        '\r\n',
        'print("\\n" + "╔" + "═" * 63 + "╗")\r\n',
        'print(f"║ 🔗 لینک ورود پینگی : {pinggy_url}")\r\n',
        'print("╚" + "═" * 63 + "╝")\r\n',
        'print("📌 لینک رسمی گرادیو (Running on public URL) نیز در لاگ\u200cهای بالا چاپ می\u200cشود.\\n")\r\n',
        '\r\n',
        'while True:\r\n',
        '    time.sleep(1)'
    ]
    source_code = "".join(source_lines)
    run_dir = __import__("pathlib").Path(__import__("tempfile").gettempdir()) / "neotenet_wan22_i2v_lightning"
    run_dir.mkdir(parents=True, exist_ok=True)
    source_path = run_dir / "original_script.py"
    log_path = run_dir / "runner.log"
    pid_path = run_dir / "runner.pid"
    source_path.write_text(source_code, encoding="utf-8")

    status = "برای شروع، دکمه «اجرای مدل» را بزنید."
    if start_button.value:
        import os, subprocess, sys, time
        old_pid = None
        try:
            old_pid = int(pid_path.read_text(encoding="utf-8").strip())
        except Exception:
            pass
        running = False
        if old_pid:
            try:
                os.kill(old_pid, 0)
                running = True
            except OSError:
                running = False
        if running:
            status = f"فرایند از قبل در حال اجراست (PID: {old_pid})."
        else:
            log_path.write_text("", encoding="utf-8")
            env = os.environ.copy()
            with log_path.open("ab") as log_stream:
                proc = subprocess.Popen(
                    [sys.executable, "-u", str(source_path)],
                    cwd=str(run_dir),
                    stdout=log_stream,
                    stderr=subprocess.STDOUT,
                    env=env,
                    start_new_session=True,
                )
            pid_path.write_text(str(proc.pid), encoding="utf-8")
            status = f"فرایند اجرا شد. PID: {proc.pid} — برای دیدن خروجی «تازه‌سازی لاگ» را بزنید."
    status
    return log_path, pid_path, run_dir, source_path, status


@app.cell
def _(mo, stop_button, pid_path):
    import os, signal
    stop_status = ""
    if stop_button.value:
        try:
            pid = int(pid_path.read_text(encoding="utf-8").strip())
            os.killpg(pid, signal.SIGTERM)
            stop_status = f"درخواست توقف برای فرایند {pid} ارسال شد."
        except Exception as exc:
            stop_status = f"توقف انجام نشد یا فرایند قبلاً بسته شده است: {exc}"
    if stop_status:
        mo.md("### وضعیت توقف\n" + stop_status)
    return


@app.cell
def _(mo, log_path, refresh_button, status):
    from pathlib import Path
    mo.md("### وضعیت اجرا")
    mo.md(status)
    if refresh_button.value:
        try:
            log_text = Path(log_path).read_text(encoding="utf-8", errors="replace")
            if len(log_text) > 14000:
                log_text = "[… ابتدای لاگ کوتاه شده است …]\n" + log_text[-14000:]
        except Exception as exc:
            log_text = f"خواندن لاگ ممکن نشد: {exc}"
        print(log_text if log_text else "هنوز لاگی ثبت نشده است.")
    else:
        mo.md("برای مشاهده خروجی تازه، دکمه «تازه‌سازی لاگ» را بزنید.")
    return


if __name__ == "__main__":
    app.run()
