import marimo

__generated_with = "0.0.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(r"""
    # 💎 NeoTenet MoLab — Qwen-Image-2.1-Turbo

    اسکریپت اصلی Qwen-Image-2.1-Turbo با رابط Gradio، تنظیمات حافظه و لینک عمومی.

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
        '# @title 💎 Qwen-Image-2.1-Turbo (Official Dual-RAM + Fixed Pinggy & Gradio Live)\r\n',
        '# @markdown Pure Default Gradio, Dual-RAM CPU Offloading, 100% Uncensored, Verified Public Links.\r\n',
        '\r\n',
        'import os\r\n',
        'import sys\r\n',
        'import time\r\n',
        'import subprocess\r\n',
        'import threading\r\n',
        'import site\r\n',
        'import urllib.request\r\n',
        'import re\r\n',
        'import torch\r\n',
        '\r\n',
        'def run_cmd(cmd):\r\n',
        '    subprocess.run(cmd, shell=True)\r\n',
        '\r\n',
        'print("═" * 70)\r\n',
        'print("🚀 LAUNCHING OFFICIAL QWEN-IMAGE-2.1-TURBO (DUAL-RAM + UNCENSORED)")\r\n',
        'print("═" * 70)\r\n',
        '\r\n',
        'if not torch.cuda.is_available():\r\n',
        '    raise SystemError("⚠️ کارت گرافیک متصل نیست! لطفا از منوی بالای MoLab (دکمه Compute) نوع سخت\u200cافزار را روی GPU بگذارید.")\r\n',
        '\r\n',
        '# ۱. دریافت یا بازنشانی کامل سورس مخزن رسمی توربو\r\n',
        "SPACE_DIR = '/content/qwen_turbo_space'\r\n",
        "os.makedirs('/content', exist_ok=True)\r\n",
        '\r\n',
        'if not os.path.exists(SPACE_DIR):\r\n',
        '    print("📥 Cloning official Qwen-Image-2.1-Turbo repository...")\r\n',
        '    run_cmd(f"git clone https://huggingface.co/spaces/hugging-apps/qwen-qwen-image-2-1-turbo {SPACE_DIR}")\r\n',
        'else:\r\n',
        '    print("🔄 Resetting repository to clean state...")\r\n',
        '    run_cmd(f"cd {SPACE_DIR} && git reset --hard HEAD && git clean -fd")\r\n',
        '\r\n',
        'os.chdir(SPACE_DIR)\r\n',
        '\r\n',
        '# ۲. نصب وابستگی\u200cهای پایتون (شامل پینگی، شتاب\u200cدهنده و گرادیو)\r\n',
        'print("📦 Installing verified dependencies...")\r\n',
        'run_cmd(f"{sys.executable} -m pip install -q gradio pinggy accelerate torchvision pillow")\r\n',
        'if os.path.exists(os.path.join(SPACE_DIR, "requirements.txt")):\r\n',
        '    run_cmd(f"{sys.executable} -m pip install -q -r {os.path.join(SPACE_DIR, \'requirements.txt\')}")\r\n',
        '\r\n',
        '# پیکربندی حافظه و Dual-RAM\r\n',
        'os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True,garbage_collection_threshold:0.8"\r\n',
        'os.environ["PYTHONUNBUFFERED"] = "1"\r\n',
        'os.environ["QWEN21_AOTI"] = "0"\r\n',
        'os.environ["GRADIO_SHARE"] = "true"\r\n',
        'os.environ["GRADIO_SERVER_NAME"] = "0.0.0.0"\r\n',
        'os.environ["GRADIO_SERVER_PORT"] = "7860"\r\n',
        'torch.backends.cuda.matmul.allow_tf32 = True\r\n',
        'torch.backends.cudnn.allow_tf32 = True\r\n',
        '\r\n',
        'run_cmd("fuser -k 7860/tcp > /dev/null 2>&1 || true")\r\n',
        'time.sleep(1)\r\n',
        '\r\n',
        '# ۳. شبیه\u200cساز ماژول spaces\r\n',
        'SPACES_SHIM = """\r\n',
        'def GPU(func=None, **kwargs):\r\n',
        '    def decorator(fn): return fn\r\n',
        '    if callable(func): return func\r\n',
        '    return decorator\r\n',
        '"""\r\n',
        'with open(os.path.join(SPACE_DIR, "spaces.py"), "w", encoding="utf-8") as f:\r\n',
        '    f.write(SPACES_SHIM)\r\n',
        '\r\n',
        'for sp in site.getsitepackages():\r\n',
        '    try:\r\n',
        '        with open(os.path.join(sp, "spaces.py"), "w", encoding="utf-8") as f:\r\n',
        '            f.write(SPACES_SHIM)\r\n',
        '    except Exception:\r\n',
        '        pass\r\n',
        '\r\n',
        '# ۴. غیرفعال\u200cسازی ۱۰۰٪ ماژول سانسور و تعریف متغیر GUARD_ID برای رفع خطای خط ۱۰۷\r\n',
        "NCII_DISABLED_SHIM = '''\r\n",
        'GUARD_ID = "Disabled"\r\n',
        'GUARD_REJECTION_MESSAGE = ""\r\n',
        'PORT = 8000\r\n',
        '\r\n',
        'def start():\r\n',
        '    print("[guard] 🛡️ NCII Guard completely disabled -> 100% Uncensored Mode Active")\r\n',
        '\r\n',
        'def score(prompt, timeout=60.0):\r\n',
        '    return 0.0\r\n',
        '\r\n',
        'def classify(prompt):\r\n',
        '    return {"label": "safe", "score": 0.0}\r\n',
        '\r\n',
        'def check_guard(prompt):\r\n',
        '    return None\r\n',
        "'''\r\n",
        'with open(os.path.join(SPACE_DIR, "ncii_guard.py"), "w", encoding="utf-8") as f:\r\n',
        '    f.write(NCII_DISABLED_SHIM)\r\n',
        '\r\n',
        '# ۵. پچ کردن سورس: فعال\u200cسازی معماری Dual-RAM + رفع سانسور\r\n',
        'print("\\n• پیاده\u200cسازی معماری Dual-RAM و پیکربندی سرور...")\r\n',
        "app_file = os.path.join(SPACE_DIR, 'app.py')\r\n",
        '\r\n',
        "with open(app_file, 'r', encoding='utf-8') as f:\r\n",
        '    code = f.read()\r\n',
        '\r\n',
        '# فعال\u200cسازی تقسیم رم: ارسال لایه\u200cها به رم سیستم و فراخوانی نوبتی در VRAM کارت گرافیک\r\n',
        'dual_ram_code = \'\'\'print("[memory] 🚀 Dual-RAM Active: Distributing Qwen-2.1-Turbo across System RAM & GPU VRAM...")\r\n',
        "pipe.enable_model_cpu_offload()'''\r\n",
        "code = re.sub(r'pipe(?:\\s*=\\s*pipe)?\\.to\\([^\\)]+\\)', dual_ram_code, code)\r\n",
        '\r\n',
        '# خنثی\u200cسازی کامل توابع ارور سانسور در فایل اصلی\r\n',
        "code = re.sub(r'def check_prompt\\(.*?\\):', 'def check_prompt(prompt):\\n    return None\\ndef _disabled_prompt(prompt):', code)\r\n",
        "code = re.sub(r'def check_guard\\(.*?\\):', 'def check_guard(prompt):\\n    return None\\ndef _disabled_guard(prompt):', code)\r\n",
        "code = re.sub(r'raise gr\\.Error\\(.*?\\)', 'pass', code)\r\n",
        '\r\n',
        '# فعال\u200cسازی share=True در Gradio بدون دستکاری ظاهر رسمی\r\n',
        'if "server_name=" not in code:\r\n',
        '    code = code.replace("demo.launch(", "demo.launch(share=True, server_name=\'0.0.0.0\', server_port=7860, inbrowser=False, ")\r\n',
        '\r\n',
        "with open(app_file, 'w', encoding='utf-8') as f:\r\n",
        '    f.write(code)\r\n',
        '\r\n',
        'print("✅ مدل Qwen-2.1-Turbo با معماری Dual-RAM آماده شد!")\r\n',
        '\r\n',
        '# ۶. اجرای سرور برنامه\r\n',
        'gradio_live_url = None\r\n',
        'print("\\n⚙️ Starting backend engine...")\r\n',
        'proc = subprocess.Popen(\r\n',
        '    [sys.executable, "-u", "app.py"],\r\n',
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
        '# ۷. انتظار برای بارگذاری کامل مدل در حافظه Dual-RAM\r\n',
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
        '# ۸. استارت پینگی دقیقاً با همان ساختار موفق کد قبلی\r\n',
        'print("\\n" + "═" * 65)\r\n',
        'print("🌐 GENERATING DIRECT URL FOR QWEN TURBO...")\r\n',
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
        '            if u.startswith("https://") and "dashboard" not in u and "127.0.0.1" not in u and "localhost" not in u:\r\n',
        '                public_url = u\r\n',
        '                break\r\n',
        '    if public_url:\r\n',
        '        break\r\n',
        '    time.sleep(1)\r\n',
        '\r\n',
        'if not public_url and hasattr(tunnel, "urls") and tunnel.urls:\r\n',
        '    for u in tunnel.urls:\r\n',
        '        if u.startswith("https://") and "127.0.0.1" not in u:\r\n',
        '            public_url = u\r\n',
        '            break\r\n',
        '\r\n',
        '# ۹. نمایش لینک\u200cهای عمومی (بدون هیچ آدرس لوکال)\r\n',
        'print("\\n" + "╔" + "═" * 65 + "╗")\r\n',
        'if public_url and not public_url.startswith("http://127.0.0.1"):\r\n',
        '    print(f"║ 🚀 ورود به پنل (لینک مستقیم پینگی): {public_url}")\r\n',
        'if gradio_live_url:\r\n',
        '    print(f"║ 🌟 ورود به پنل (لینک گرادیو)      : {gradio_live_url}")\r\n',
        'print("╚" + "═" * 65 + "╝\\n")\r\n',
        'print("👈 روی لینک آبی رنگ بالا کلیک کنید تا پنل ۲.۱ توربو مستقیماً روی مرورگر باز شود.")\r\n',
        '\r\n',
        'while True:\r\n',
        '    time.sleep(1)'
    ]
    source_code = "".join(source_lines)
    run_dir = __import__("pathlib").Path(__import__("tempfile").gettempdir()) / "neotenet_qwen_image_2_1_turbo"
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
