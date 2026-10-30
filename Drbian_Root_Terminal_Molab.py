# @title NeoTenet Web Terminal Workspace (Pinggy Auto-Clean & Fallback Fixed)
# @markdown Automatically kills stale Pinggy sessions and adds SSH fallback to guarantee link generation on repeated runs.

import os
import re
import time
import subprocess
from pathlib import Path

class NeoTenetEnvironment:
    def __init__(self):
        self.port = 7681
        self.home_dir = Path(os.path.expanduser("~"))
        self.bashrc_path = self.home_dir / ".bashrc"

    def configure_shell_prompt(self):
        prompt_config = r"""
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
export PS1="\[\e[1;32m\]NeoTenet\[\e[0m\]@\[\e[1;34m\]molab\[\e[0m\]:\[\e[1;33m\]~\[\e[0m\]# "
clear
echo -e "\e[1;35m  =======================================================\e[0m"
echo -e "\e[1;36m   🚀  NEOTENET TERMINAL WORKSPACE | ROOT ACCESS ACTIVE  \e[0m"
echo -e "\e[1;35m  =======================================================\e[0m"
echo -e "\e[1;32m   📢 Telegram Channel : @NeoTenet\e[0m"
echo -e "\e[1;33m   ⚡ Engine           : ttyd Web Console + Pinggy Tunnel\e[0m"
echo -e "\e[1;35m  =======================================================\e[0m"
echo ""
"""
        try:
            self.bashrc_path.write_text(prompt_config)
        except Exception:
            pass

    def prepare_dependencies(self):
        print("⚡ [Phase 1] Optimizing repositories & fetching packages...")

        subprocess.run(
            "sed -i '/stat.illinois.edu/d' /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null || true",
            shell=True
        )

        packages = ["htop", "curl", "wget", "git", "python3-pip"]
        subprocess.run(
            f"apt-get update -qq && apt-get install -y {' '.join(packages)} -qq",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # نصب پینگی برای پایتون
        subprocess.run(
            f"{os.sys.executable} -m pip install -q --upgrade pinggy",
            shell=True
        )

        # دانلود ttyd
        ttyd_dest = "/usr/local/bin/ttyd"
        if not os.path.exists(ttyd_dest):
            subprocess.run(
                f"wget -q -nc https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -O {ttyd_dest} && chmod +x {ttyd_dest}",
                shell=True
            )

    def terminate_old_processes(self):
        print("🧹 Cleaning old sessions & releasing network ports...")
        # ۱. آزاد کردن پورت 7681
        subprocess.run(f"fuser -k {self.port}/tcp > /dev/null 2>&1 || true", shell=True)
        subprocess.run(["pkill", "-9", "-f", "ttyd"], stderr=subprocess.DEVNULL)
        
        # ۲. بستن کامل نشست‌های قبلی پینگی در حافظه (علت اصلی خطای دفعه دوم)
        subprocess.run("pkill -9 -f pinggy > /dev/null 2>&1 || true", shell=True)
        subprocess.run("pkill -9 -f a.pinggy.io > /dev/null 2>&1 || true", shell=True)
        subprocess.run("rm -rf /tmp/pinggy* /tmp/.pinggy* > /dev/null 2>&1 || true", shell=True)
        
        # ۳. مهلت به سرورهای پینگی برای قطع کامل ارتباط قبلی
        time.sleep(3)

    def initialize_services(self):
        print("🌐 [Phase 2] Deploying ttyd web console...")

        ttyd_args = [
            "ttyd", "-W", "-p", str(self.port),
            "-t", "fontSize=16",
            "-t", "theme={'background': '#000000', 'foreground': '#ffffff'}",
            "bash", "--rcfile", str(self.bashrc_path)
        ]

        subprocess.Popen(ttyd_args)
        time.sleep(2)

    def start_pinggy_tunnel(self):
        print("💎 [Phase 3] Generating secure Pinggy tunnel...")
        import pinggy
        
        # تلاش اول با کتابخانه رسمی پایتون
        tunnel = None
        try:
            tunnel = pinggy.start_tunnel(forwardto=f"localhost:{self.port}", force=True)
        except Exception:
            try:
                tunnel = pinggy.start_tunnel(forwardto=f"localhost:{self.port}")
            except Exception:
                pass

        endpoint = None
        if tunnel:
            for _ in range(25):
                if hasattr(tunnel, "urls") and tunnel.urls:
                    for u in tunnel.urls:
                        if isinstance(u, str) and u.startswith("https://") and "dashboard" not in u:
                            endpoint = u
                            break
                if endpoint:
                    break
                time.sleep(1)

            if not endpoint and hasattr(tunnel, "urls") and tunnel.urls:
                endpoint = tunnel.urls[0]

        # تلاش دوم (پشتیبان اضطراری SSH): اگر روش اول لینک نداد، با SSH فوراً لینک می‌گیرد
        if not endpoint:
            print("⏳ Switching to Pinggy Direct Link protocol...")
            ssh_log = Path("/tmp/pinggy_ssh.log")
            if ssh_log.exists():
                ssh_log.unlink()
            
            subprocess.Popen(
                f"ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=10 -p 443 -R0:localhost:{self.port} free@a.pinggy.io > /tmp/pinggy_ssh.log 2>&1",
                shell=True
            )
            
            for _ in range(15):
                time.sleep(1)
                if ssh_log.exists():
                    text = ssh_log.read_text()
                    found = re.findall(r'https://[a-zA-Z0-9-]+\.free\.pinggy\.link|https://[a-zA-Z0-9-]+\.free\.pinggy\.net', text)
                    if found:
                        endpoint = found[0]
                        break

        return endpoint

    def start(self):
        self.terminate_old_processes()
        self.prepare_dependencies()
        self.configure_shell_prompt()
        self.initialize_services()

        url = self.start_pinggy_tunnel()

        print("\n" + "═" * 55)
        print("  💎 NEOTENET WEB TERMINAL IS ACTIVE")
        print("═" * 55)
        print(f"  🚀 ACCESS LINK : {url if url else 'Failed to generate Pinggy link'}")
        print("═" * 55 + "\n")
        print("👈 روی لینک بالا کلیک کنید تا محیط خط فرمان ترمینال در مرورگر باز شود.")

        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nShutting down NeoTenet Environment...")

if __name__ == "__main__":
    app = NeoTenetEnvironment()
    app.start()