# @title NeoTenet Web Terminal Workspace (Pinggy 100% Fixed + SSH Fallback + No Drive)
# @markdown Installs openssh-client, fixes Pinggy regex & API parsing, removes Drive backup.

import os
import re
import time
import subprocess
import urllib.request
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

        # اضافه شدن openssh-client جهت تضمین کارکرد تونل SSH پینگی
        packages = ["openssh-client", "htop", "curl", "wget", "git", "python3-pip"]
        subprocess.run(
            f"apt-get update -qq && apt-get install -y {' '.join(packages)} -qq",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # نصب کتابخانه پایتون پینگی
        subprocess.run(
            f"{os.sys.executable} -m pip install -q --upgrade pinggy",
            shell=True
        )

        # دانلود باینری ttyd
        ttyd_dest = "/usr/local/bin/ttyd"
        if not os.path.exists(ttyd_dest):
            subprocess.run(
                f"wget -q -nc https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -O {ttyd_dest} && chmod +x {ttyd_dest}",
                shell=True
            )

    def terminate_old_processes(self):
        print("🧹 Cleaning old sessions & releasing network ports...")
        subprocess.run(f"fuser -k {self.port}/tcp > /dev/null 2>&1 || true", shell=True)
        subprocess.run(f"fuser -k 4300/tcp > /dev/null 2>&1 || true", shell=True)
        subprocess.run(["pkill", "-9", "-f", "ttyd"], stderr=subprocess.DEVNULL)
        subprocess.run("pkill -9 -f pinggy > /dev/null 2>&1 || true", shell=True)
        subprocess.run("pkill -9 -f a.pinggy.io > /dev/null 2>&1 || true", shell=True)
        subprocess.run("rm -rf /tmp/pinggy* /tmp/.pinggy* > /dev/null 2>&1 || true", shell=True)
        time.sleep(2)

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
        endpoint = None

        # تلاش ۱: استفاده از SDK پایتون پینگی
        try:
            import pinggy
            tunnel = pinggy.start_tunnel(forwardto=f"localhost:{self.port}")
            for _ in range(12):
                if hasattr(tunnel, "urls") and tunnel.urls:
                    for u in tunnel.urls:
                        if isinstance(u, str) and u.startswith("https://") and "dashboard" not in u:
                            endpoint = u
                            break
                if endpoint:
                    break
                time.sleep(1)
        except Exception:
            pass

        # تلاش ۲ (تضمینی): پروتکل SSH با وب‌دیباگر و ریجکس هوشمند
        if not endpoint:
            print("⏳ Connecting via Pinggy Native SSH Protocol...")
            ssh_log = Path("/tmp/pinggy_ssh.log")
            if ssh_log.exists():
                ssh_log.unlink()

            # اجرای تونل معکوس SSH با فوروارد پورت دیباگر 4300 جهت دریافت قطعی لینک
            subprocess.Popen(
                f"ssh -p 443 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=10 "
                f"-R0:localhost:{self.port} -L4300:localhost:4300 free@a.pinggy.io > /tmp/pinggy_ssh.log 2>&1",
                shell=True
            )

            for _ in range(20):
                time.sleep(1)
                # بررسی API پینگی روی پورت 4300
                try:
                    with urllib.request.urlopen("http://localhost:4300/urls", timeout=1) as resp:
                        import json
                        data = json.loads(resp.read().decode())
                        for u in data.get("urls", []):
                            if u.startswith("https://"):
                                endpoint = u
                                break
                except Exception:
                    pass

                if endpoint:
                    break

                # بررسی مستقیم فایل لاگ با ریجکس جامع
                if ssh_log.exists():
                    text = ssh_log.read_text()
                    found = re.findall(r'https://[^\s<>"\']+(?:pinggy\.link|pinggy\.net|pinggy\.io|pinggy-free\.link)', text)
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
        print(f"  🚀 ACCESS LINK : {url if url else 'خطا در تولید لینک، مجدد Run کنید'}")
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
