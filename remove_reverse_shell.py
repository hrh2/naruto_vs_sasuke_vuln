import os
import subprocess
import sys

# Linux Paths
SHELL_SCRIPT_PATH_LINUX = "/root/reverse_shell.sh"
SERVICE_FILE_PATH_LINUX = "/etc/systemd/system/reverse_shell.service"

# Windows Paths
SHELL_SCRIPT_PATH_WIN = os.path.expandvars(r"%APPDATA%\reverse_shell.ps1")
TASK_NAME = "ReverseShellGame"

# Detect OS
os_name = os.uname().sysname if hasattr(os, "uname") else sys.platform

if os_name == "Linux":
    try:
        print("[+] Stopping reverse shell service...")
        subprocess.run(["systemctl", "stop", "reverse_shell.service"], check=False)
        subprocess.run(["systemctl", "disable", "reverse_shell.service"], check=False)

        if os.path.exists(SERVICE_FILE_PATH_LINUX):
            print("[+] Removing systemd service file...")
            os.remove(SERVICE_FILE_PATH_LINUX)

        if os.path.exists(SHELL_SCRIPT_PATH_LINUX):
            print("[+] Removing reverse shell script...")
            os.remove(SHELL_SCRIPT_PATH_LINUX)

        print("[+] Reloading systemd...")
        subprocess.run(["systemctl", "daemon-reload"], check=False)
        subprocess.run(["systemctl", "reset-failed"], check=False)

        print("[✓] Reverse shell completely removed (Linux).")

    except Exception as e:
        print(f"[ERROR] Failed to remove reverse shell (Linux): {e}")
        sys.exit(1)

elif os_name.startswith("Win"):
    try:
        print("[+] Stopping scheduled task (if exists)...")
        subprocess.run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"], check=False)

        if os.path.exists(SHELL_SCRIPT_PATH_WIN):
            print("[+] Removing PowerShell reverse shell script...")
            os.remove(SHELL_SCRIPT_PATH_WIN)

        print("[✓] Reverse shell completely removed (Windows).")

    except Exception as e:
        print(f"[ERROR] Failed to remove reverse shell (Windows): {e}")
        sys.exit(1)

else:
    print(f"[ERROR] Unknown system: {os_name}")
    sys.exit(1)
