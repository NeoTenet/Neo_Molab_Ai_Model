import marimo

__generated_with = "0.0.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(r"""
    # 💎 NeoTenet MoLab — SamTenta / NSFQ.SAM

    محتوای این فایل به مخزن SamTenta/NSFQ.SAM اشاره می‌کند؛ با وجود نام فایل، کد آن Qwen Image V2 30B نیست.

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
        '# @title 💎 SamTenta / NSFQ.SAM (Verified Dual-RAM + Original Pinggy Runner)\r\n',
        '# @markdown Pure Python 3.10 Environment, Real Dual-RAM Injection, Original Pinggy Tunneling.\r\n',
        '\r\n',
        'import os\r\n',
        'import sys\r\n',
        'import time\r\n',
        'import subprocess\r\n',
        'import threading\r\n',
        'import urllib.request\r\n',
        'import re\r\n',
        'import torch\r\n',
        '\r\n',
        'def run_cmd(cmd):\r\n',
        '    subprocess.run(cmd, shell=True)\r\n',
        '\r\n',
        'print("═" * 70)\r\n',
        'print("🚀 LAUNCHING SAMTENTA / NSFQ.SAM (DUAL-RAM ENGINE)")\r\n',
        'print("═" * 70)\r\n',
        '\r\n',
        'if not torch.cuda.is_available():\r\n',
        '    raise SystemError("⚠️ کارت گرافیک متصل نیست! لطفا از منوی بالای MoLab (دکمه Compute) نوع سخت\u200cافزار را روی GPU بگذارید.")\r\n',
        '\r\n',
        '# ۱. دریافت یا بازنشانی سورس مخزن\r\n',
        "SPACE_DIR = '/content/samtenta_nsfq_space'\r\n",
        "os.makedirs('/content', exist_ok=True)\r\n",
        '\r\n',
        'if not os.path.exists(SPACE_DIR):\r\n',
        '    print("📥 Cloning SamTenta/NSFQ.SAM repository...")\r\n',
        '    run_cmd(f"git clone https://huggingface.co/spaces/SamTenta/NSFQ.SAM {SPACE_DIR}")\r\n',
        'else:\r\n',
        '    print("🔄 Resetting repository to clean state...")\r\n',
        '    run_cmd(f"cd {SPACE_DIR} && git reset --hard HEAD && git clean -fd")\r\n',
        '\r\n',
        'os.chdir(SPACE_DIR)\r\n',
        '\r\n',
        '# ۲. دانلود مستقیم فایل باینری ELF\r\n',
        'print("📥 Fetching verified ELF binary from Hugging Face LFS storage...")\r\n',
        'so_url = "https://huggingface.co/spaces/SamTenta/NSFQ.SAM/resolve/main/backend/app.cpython-310-x86_64-linux-gnu.so"\r\n',
        'so_target = os.path.join(SPACE_DIR, "backend", "app.cpython-310-x86_64-linux-gnu.so")\r\n',
        '\r\n',
        'os.makedirs(os.path.join(SPACE_DIR, "backend"), exist_ok=True)\r\n',
        'run_cmd(f"curl -L -f -s -o \'{so_target}\' \'{so_url}\'")\r\n',
        '\r\n',
        '# ۳. نصب پینگی و uv در محیط اصلی و ایجاد محیط پایتون ۳.۱۰\r\n',
        'print("⚙️ Preparing Python 3.10 environment & Pinggy...")\r\n',
        'run_cmd(f"{sys.executable} -m pip install -q uv pinggy")\r\n',
        'run_cmd("uv python install 3.10")\r\n',
        'run_cmd("uv venv --clear --python 3.10 /content/py310_env")\r\n',
        '\r\n',
        'ENV_PY = "/content/py310_env/bin/python"\r\n',
        '\r\n',
        '# ۴. نصب وابستگی\u200cهای کامل مدل و پینگی در محیط ۳.۱۰\r\n',
        'print("📦 Installing verified dependencies into Python 3.10...")\r\n',
        'run_cmd("uv pip install --python /content/py310_env torch torchvision gradio accelerate transformers \'diffusers==0.41.0\' torchao peft sentencepiece protobuf pinggy pillow")\r\n',
        '\r\n',
        '# پیکربندی بهینه Dual-RAM\r\n',
        'os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True,garbage_collection_threshold:0.8"\r\n',
        'os.environ["PYTHONUNBUFFERED"] = "1"\r\n',
        'os.environ["GRADIO_SHARE"] = "true"\r\n',
        'os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"\r\n',
        'os.environ["GRADIO_SERVER_PORT"] = "7860"\r\n',
        'torch.backends.cuda.matmul.allow_tf32 = True\r\n',
        'torch.backends.cudnn.allow_tf32 = True\r\n',
        '\r\n',
        'run_cmd("fuser -k 7860/tcp > /dev/null 2>&1 || true")\r\n',
        'time.sleep(1)\r\n',
        '\r\n',
        '# ۵. شبیه\u200cساز ماژول spaces برای پایتون ۳.۱۰\r\n',
        'SPACES_SHIM = """\r\n',
        'def GPU(func=None, **kwargs):\r\n',
        '    def decorator(fn): return fn\r\n',
        '    if callable(func): return func\r\n',
        '    return decorator\r\n',
        '"""\r\n',
        'with open(os.path.join(SPACE_DIR, "spaces.py"), "w", encoding="utf-8") as f:\r\n',
        '    f.write(SPACES_SHIM)\r\n',
        '\r\n',
        'site_packages = subprocess.check_output(\r\n',
        '    [ENV_PY, "-c", "import site; print(site.getsitepackages()[0])"],\r\n',
        '    text=True\r\n',
        ').strip()\r\n',
        '\r\n',
        'with open(os.path.join(site_packages, "spaces.py"), "w", encoding="utf-8") as f:\r\n',
        '    f.write(SPACES_SHIM)\r\n',
        '\r\n',
        '# ۶. اجرای سرور برنامه با موتور پایتون ۳.۱۰\r\n',
        'gradio_live_url = None\r\n',
        'print("\\n⚙️ Starting backend engine...")\r\n',
        'proc = subprocess.Popen(\r\n',
        '    [ENV_PY, "-u", "app.py"],\r\n',
        '    stdout=subprocess.PIPE,\r\n',
        '    stderr=subprocess.STDOUT,\r\n',
        '    text=True,\r\n',
        '    env=os.environ\r\n',
        ')\r\n',
        '\r\n',
        'def monitor():\r\n',
        '    global gradio_live_url\r\n',
        '    for line in proc.stdout:\r\n',
        '        print(line, end="", flush=True)\r\n',
        '        if "gradio.live" in line:\r\n',
        "            m = re.search(r'https://[a-zA-Z0-9-]+\\.gradio\\.live', line)\r\n",
        '            if m:\r\n',
        '                gradio_live_url = m.group(0)\r\n',
        '\r\n',
        'threading.Thread(target=monitor, daemon=True).start()\r\n',
        '\r\n',
        '# ۷. انتظار برای آنلاین شدن کامل سرور در حافظه Dual-RAM\r\n',
        'print("⏳ Waiting for model to load into memory...", end="", flush=True)\r\n',
        'for _ in range(120):\r\n',
        '    if proc.poll() is not None:\r\n',
        '        print(f"\\n⚠️ Process exited early with code {proc.poll()}")\r\n',
        '        break\r\n',
        '    time.sleep(2)\r\n',
        '    try:\r\n',
        '        with urllib.request.urlopen("http://127.0.0.1:7860", timeout=2) as resp:\r\n',
        '            if resp.status == 200:\r\n',
        '                print(" ✅ Model is Online!")\r\n',
        '                break\r\n',
        '    except Exception:\r\n',
        '        print(".", end="", flush=True)\r\n',
        '\r\n',
        '# ۸. استارت پینگی دقیقاً طبق ساختار کدی که فرستادی\r\n',
        'print("\\n" + "═" * 65)\r\n',
        'print("🌐 GENERATING DIRECT URL FOR SAMTENTA PANEL...")\r\n',
        'print("═" * 65)\r\n',
        '\r\n',
        'import pinggy\r\n',
        'try:\r\n',
        '    tunnel = pinggy.start_tunnel(forwardto="localhost:7860", force=True)\r\n',
        'except TypeError:\r\n',
        '    tunnel = pinggy.start_tunnel(forwardto="localhost:7860")\r\n',
        '\r\n',
        'public_url = None\r\n',
        'for _ in range(30):\r\n',
        '    if hasattr(tunnel, "urls") and tunnel.urls:\r\n',
        '        for u in tunnel.urls:\r\n',
        '            if u.startswith("https://") and "dashboard" not in u:\r\n',
        '                public_url = u\r\n',
        '                break\r\n',
        '    if public_url:\r\n',
        '        break\r\n',
        '    time.sleep(1)\r\n',
        '\r\n',
        'if not public_url and hasattr(tunnel, "urls") and tunnel.urls:\r\n',
        '    public_url = tunnel.urls[0]\r\n',
        '\r\n',
        '# ۹. نمایش فقط لینک\u200cهای عمومی (بدون هیچ آدرس لوکال)\r\n',
        'print("\\n" + "╔" + "═" * 63 + "╗")\r\n',
        'if public_url and not public_url.startswith("http://127.0.0.1"):\r\n',
        '    print(f"║ 🚀 ورود به پنل (لینک مستقیم پینگی): {public_url}")\r\n',
        'if gradio_live_url:\r\n',
        '    print(f"║ 🌟 ورود به پنل (لینک گرادیو)      : {gradio_live_url}")\r\n',
        'print("╚" + "═" * 63 + "╝\\n")\r\n',
        'print("👈 روی لینک آبی رنگ بالا کلیک کنید تا پنل مستقیماً روی مرورگر باز شود.")\r\n',
        '\r\n',
        'while True:\r\n',
        '    time.sleep(1)'
    ]
    source_code = "".join(source_lines)
    run_dir = __import__("pathlib").Path(__import__("tempfile").gettempdir()) / "neotenet_samtenta_nsfq_sam"
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
