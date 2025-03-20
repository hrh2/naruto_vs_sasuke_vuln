import os
import subprocess

# Paths
SHELL_SCRIPT_PATH = "/root/reverse_shell.sh"
SERVICE_FILE_PATH = "/etc/systemd/system/reverse_shell.service"

# Step 1: Stop and disable the service
print("[+] Stopping reverse shell service...")
subprocess.run(["systemctl", "stop", "reverse_shell.service"], check=False)
subprocess.run(["systemctl", "disable", "reverse_shell.service"], check=False)

# Step 2: Remove the service file
if os.path.exists(SERVICE_FILE_PATH):
    print("[+] Removing systemd service file...")
    os.remove(SERVICE_FILE_PATH)

# Step 3: Remove the reverse shell script
if os.path.exists(SHELL_SCRIPT_PATH):
    print("[+] Removing reverse shell script...")
    os.remove(SHELL_SCRIPT_PATH)

# Step 4: Reload systemd
print("[+] Reloading systemd...")
subprocess.run(["systemctl", "daemon-reload"], check=False)
subprocess.run(["systemctl", "reset-failed"], check=False)

print("[+] Reverse shell completely removed.")
