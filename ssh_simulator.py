import time
import os
import itertools
import sys
import getpass
import random
import shutil

def get_terminal_size():
    """Gets terminal size or returns default."""
    try:
        return shutil.get_terminal_size()
    except:
        return os.terminal_size((80, 24))

# Simulated file structure with permissions

file_system = {
    "/": {
        "contents": ["home", "var", "etc", "exploitscan.py", "exploit.sh", "exfildata.py", "surprise.py"],
        "permissions": {"read": True, "execute": True}
    },
    "/home": {
        "contents": ["a.turing"],
        "permissions": {"read": True, "execute": True}
    },
    "/home/a.turing": {
        "contents": ["notes.txt"],
        "permissions": {"read": True, "execute": True}
    },
    "/var": {
        "contents": ["data", "log"],
        "permissions": {"read": True, "execute": True}
    },
    "/var/data": {
        "contents": ["employee_data", "client_data"],
        "permissions": {"read": False, "execute": False}
    },
    "/var/data/employee_data": {
        "contents": ["records.db"],
        "permissions": {"read": False, "execute": False}
    },
    "/var/data/client_data": {
        "contents": [f"client{i}.txt" for i in range(1, 51)],
        "permissions": {"read": False, "execute": False}
    },
    "/etc": {
        "contents": ["passwd", "shadow"],
        "permissions": {"read": True, "execute": True}
    }
}


# Simulated employee data
employee_data = [
    {"name": "John Smith", "role": "Software Engineer", "email": "john.smith@company.com"},
    {"name": "Jane Doe", "role": "HR Manager", "email": "jane.doe@company.com"}
]

current_directory = "/"
is_admin = False

def generate_client_file_content(index):
    """Generates realistic client information for a specific file."""
    fake_clients = [
        {"name": "Alice Brown", "card_number": "4111 1111 1111 1111", "expiry": "12/25", "cvv": "123"},
        {"name": "Bob Johnson", "card_number": "5500 0000 0000 0004", "expiry": "01/26", "cvv": "456"},
        {"name": "Charlie Davis", "card_number": "4000 1234 5678 9010", "expiry": "08/24", "cvv": "789"},
        {"name": "Diana Evans", "card_number": "6011 0009 9013 9424", "expiry": "09/27", "cvv": "456"},
        {"name": "Evan Garcia", "card_number": "3530 1113 3330 0000", "expiry": "05/26", "cvv": "987"},
    ]
    client = fake_clients[index % len(fake_clients)]
    return f"{client['name']}: {client['card_number']} (Expiry: {client['expiry']}, CVV: {client['cvv']})"

def copy_tools_from_server():
    """Simulates copying tools from an attack server."""
    print("\n[*] Connecting to attack server...")
    time.sleep(1.5)
    print("[*] Establishing secure connection...")
    time.sleep(2)
    print("[+] Connection established: 203.0.113.42:22")
    
    tools = ["exploitscan.py", "exploit.sh", "exfildata.py"]  # Removed ransomware.py
    for tool in tools:
        print(f"[*] Copying {tool}...")
        time.sleep(random.uniform(1.0, 2.0))
        print(f"[+] {tool} copied successfully.")
    
    print("\n[*] Closing connection to attack server...")
    time.sleep(1.5)
    print("[+] Tools copied and ready for use.")

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def title_screen():
    """Displays the SSH server banner."""
    clear_screen()
    print("""
    SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
    ==================================
    This system is for authorized users only.
    All activity may be monitored and reported.
    
    Type 'exit' to log out.
    """)

def authenticate():
    """Simulates SSH authentication."""
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        
        if username == "a.turing" and password == "test":
            print("\nWelcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-135-generic x86_64)\n")
            copy_tools_from_server()  # Trigger the sequence here
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"\nAccess denied. {remaining} attempts remaining.\n")
            else:
                print("\nToo many authentication failures. Disconnecting...\n")
                time.sleep(2)
                return False
        
        time.sleep(1)
    return False

def check_directory_access(path):
    """Checks if the current user has access to the specified directory."""
    if is_admin:
        return True
        
    components = [p for p in path.split("/") if p]
    current = "/"
    
    for component in components:
        if current in file_system:
            if component in file_system[current]["contents"]:
                current = os.path.join(current, component).replace("\\", "/")
                if not file_system[current]["permissions"]["execute"]:
                    return False
            else:
                return False
    return True

def list_directory(path):
    """Lists the contents of a directory with proper permissions."""
    if not check_directory_access(path):
        return f"ls: cannot open directory '{path}': Permission denied"
    
    if path in file_system:
        if not file_system[path]["permissions"]["read"] and not is_admin:
            return f"ls: cannot open directory '{path}': Permission denied"
        return "\n".join(file_system[path]["contents"])
    return f"ls: cannot access '{path}': No such file or directory"

def cat_file(path):
    """Displays the contents of a file."""
    if not check_directory_access(os.path.dirname(path)):
        return f"cat: {path}: Permission denied"
        
    if path == "/etc/passwd":
        return "root:x:0:0:root:/root:/bin/bash\n" \
               "a.turing:x:1000:1000:Alan Turing:/home/a.turing:/bin/bash\n" \
               "syslog:x:102:106::/home/syslog:/usr/sbin/nologin\n" \
               "messagebus:x:103:107::/nonexistent:/usr/sbin/nologin"
    elif path == "/etc/shadow" and not is_admin:
        return f"cat: {path}: Permission denied"
    elif path == "/etc/shadow" and is_admin:
        return "root:$6$rFK5Bcld$9J8xvwAX9VExR1q/:18765:0:99999:7:::\n" \
               "a.turing:$6$J8xvwAX9VExR1q/:18765:0:99999:7:::"
    elif path == "/home/a.turing/notes.txt":
        return "TODO:\n" \
               "- Check server logs for suspicious activity\n" \
               "- Update system passwords\n" \
               "- Review /var/data permissions"
    elif path.startswith("/var/data/client_data/") and is_admin:
        try:
            file_index = int(path.split("client")[-1].split(".")[0]) - 1
            return generate_client_file_content(file_index)
        except (ValueError, IndexError):
            return f"cat: {path}: No such file or directory"
    elif path.startswith("/var/data"):
        return f"cat: {path}: Permission denied"
    return f"cat: {path}: No such file or directory"

def simulate_data_exfiltration():
    """Simulates a realistic data exfiltration attack."""
    if not is_admin:
        print("Permission denied")
        return

    print("\n[*] Starting data exfiltration sequence...")
    time.sleep(1.2)
    print("[*] Establishing connection to C2 server...")
    time.sleep(2.3)
    print("[+] Connection established: 185.147.xxx.xxx:443")
    
    print("\n[*] Scanning /var/data/client_data for sensitive information...")
    time.sleep(3.4)
    print("[+] Found 50 files containing payment data")
    
    print("\n[*] Creating encrypted archive...")
    time.sleep(0.7)
    print("    → Compression: xz")
    print("    → Encryption: AES-256")
    
    processed = 0
    chunk_sizes = [3, 1, 4, 2, 5, 3, 2, 4, 1, 2]  # Irregular chunks
    
    for chunk in chunk_sizes:
        time.sleep(random.uniform(1.2, 2.8))  # Variable processing time
        processed = min(processed + chunk, 50)
        sys.stdout.write(f"\r[*] Processing files: {processed}/50 [{processed*2*'='}{(100-processed*2)*' '}] {processed*2}%")
        sys.stdout.flush()
    
    print("\n\n[+] Archive created: client_data.tar.xz.enc")
    time.sleep(1.3)
    
    print("\n[*] Initiating secure transfer...")
    
    # Transfer simulation with variable speeds
    total_size = 42.7
    speeds = [(0, 1.5, "2.1"), (1.5, 3.2, "1.8"), (3.2, 4.1, "2.3"), (4.1, 5.0, "1.9")]
    
    for start_time, duration, speed in speeds:
        time.sleep(duration - start_time)
        progress = (duration / 5.0) * 100
        sys.stdout.write(f"\r[*] Transferring data: {progress:.1f}% ({speed} MB/s) - {duration:.1f}/{total_size:.1f} MB")
        sys.stdout.flush()
        if random.random() < 0.1:  # Network stutter
            time.sleep(random.uniform(0.3, 0.7))
    
    print("\n\n[+] Transfer complete")
    time.sleep(1.4)
    
    print("\n[*] Removing traces...")
    print("[*] Deleting local archive...")
    time.sleep(1.2)
    print("[*] Clearing system logs...")
    time.sleep(2.1)
    print("[*] Removing source files...")
    print("[+] Cleanup complete")
    time.sleep(0.4)
    print("\n[+] Exfiltration successful - 50 files exfiltrated")
    print("[+] Connection terminated")

def simulate_ransomware():
    """Simulates a ransomware attack sequence."""
    if not is_admin:
        print("Permission denied")
        return

    # ANSI escape codes for colors
    RED = "\033[91m"
    RESET = "\033[0m"
    
    ransomware_text = f"""{RED}
██████╗  █████╗ ███╗   ██╗███████╗ ██████╗ ███╗   ███╗██╗    ██╗ █████╗ ██████╗ ███████╗
██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔═══██╗████╗ ████║██║    ██║██╔══██╗██╔══██╗██╔════╝
██████╔╝███████║██╔██╗ ██║███████╗██║   ██║██╔████╔██║██║ █╗ ██║███████║██████╔╝█████╗  
██╔══██╗██╔══██║██║╚██╗██║╚════██║██║   ██║██║╚██╔╝██║██║███╗██║██╔══██║██╔══██╗██╔══╝  
██║  ██║██║  ██║██║ ╚████║███████║╚██████╔╝██║ ╚═╝ ██║╚███╔███╔╝██║  ██║██║  ██║███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
{RESET}"""

    clear_screen()
    print("\n[*] Initializing encryption sequence...")
    time.sleep(1.7)
    print("[*] Loading encryption keys...")
    time.sleep(2.1)
    print("[+] RSA-4096 public key loaded")
    
    print("\n[*] Enumerating system drives...")
    time.sleep(1.4)
    print("""    → /dev/sda1 (mounted at /)
    → /dev/sdb1 (mounted at /home)
    → /dev/sdc1 (mounted at /var)""")
    
    print("\n[*] Scanning for target files...")
    time.sleep(3.2)
    print("""[+] Found target files:
    → Documents: 1,842 files
    → Databases: 13 files
    → Configuration: 156 files
    → Total size: 2.7 GB""")
    
    print("\n[*] Starting encryption process...")
    
    directories = [
        ("/var/data", 312),
        ("/etc/config", 89),
        ("/home/users", 1238),
        ("/var/www", 372)
    ]
    
    for directory, files in directories:
        print(f"\n[*] Encrypting {directory}")
        encrypted = 0
        while encrypted < files:
            if random.random() < 0.05:  # Disk wait
                time.sleep(random.uniform(0.5, 1.0))
            chunk = min(random.randint(10, 30), files - encrypted)
            encrypted += chunk
            progress = (encrypted / files) * 100
            sys.stdout.write(f"\r    Progress: [{int(progress/2)*'='}{(50-int(progress/2))*' '}] {progress:.1f}% ({encrypted}/{files} files)")
            sys.stdout.flush()
            time.sleep(random.uniform(0.1, 0.4))
        print()
    
    print("\n[*] Generating ransom notes...")
    time.sleep(1.8)
    print("[*] Removing volume shadow copies...")
    time.sleep(2.1)
    print("[*] Clearing system logs...")
    time.sleep(1.4)
    print("[+] Encryption complete")
    
    time.sleep(1)
    clear_screen()
    print(ransomware_text)
    print(f"""{RED}
    YOUR FILES HAVE BEEN ENCRYPTED!
    
    Your important files have been encrypted with military-grade encryption.
    To recover your files, you must pay 5 BTC to the following address:
    bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
    
    Contact us at: [email protected] with your unique ID:
    0xC7F2A95B4E8D3A1C
    
    WARNING: Do not attempt to decrypt files or modify them, or they will be
    permanently damaged.{RESET}""")

def scan_system():
    """Simulates a thorough system scan for privilege escalation vulnerabilities."""
    def print_header(text):
        print("\n" + "=" * 60)
        print(text)
        print("=" * 60)

    print_header("Starting system scan for privilege escalation vectors...")
    time.sleep(2.3)

    print("[*] Checking kernel version...")
    time.sleep(0.1)
    print("    → Linux version 5.4.0-135-generic")
    time.sleep(0.2)
    print("    → Ubuntu 20.04.5 LTS (Focal Fossa)")
    
    time.sleep(3.7)
    print("\n[*] Gathering system information...")
    print("    → Architecture: x86_64")
    time.sleep(0.1)
    print("    → CPU: Intel(R) Xeon(R) CPU E5-2678 v3 @ 2.50GHz")
    print("    → Hostname: ubuntu-server")
    time.sleep(1.2)
    print("    → System load: 0.08, 0.03, 0.01")

    time.sleep(2.1)
    print("\n[*] Enumerating running services...")
    time.sleep(1.8)
    for service in ["systemd v245 (245.4-4ubuntu3.20)", "snapd v2.58", 
                   "polkit v0.105-26ubuntu1.1", "dbus v1.12.16"]:
        print(f"    → {service}")
        time.sleep(random.uniform(0.2, 0.4))

    print("\n[*] Checking installed packages...")
    time.sleep(4.2)
    print("    → Found 2,184 packages installed")

    print("\n[*] Enumerating SUID binaries...")
    time.sleep(5.8)
    for binary in ["/usr/bin/sudo", "/usr/bin/pkexec", 
                  "/usr/bin/polkit-agent-helper-1", 
                  "/usr/lib/policykit-1/polkit-agent-helper-1"]:
        time.sleep(random.uniform(0.1, 0.3))
        print(f"    → {binary}")

    print_header("Scanning for known vulnerabilities")
    
    cves_to_check = [
        ("CVE-2023-7028", 1.2, True),
        ("CVE-2023-4911", 0.4, False),
        ("CVE-2023-2640", 2.3, True),
        ("CVE-2023-0466", 0.6, False),
        ("CVE-2022-3328", 0.9, False),
        ("CVE-2022-2588", 1.7, True)
    ]
    
    for cve, delay, timeout in cves_to_check:
        print(f"[*] Checking {cve}... ", end='', flush=True)
        if timeout and delay > 2:
            time.sleep(2)
            print("timeout, retrying... ", end='', flush=True)
            time.sleep(0.8)
        time.sleep(delay)
        print("not vulnerable")

    print("\n[*] Checking CVE-2023-32629... ", end='', flush=True)
    time.sleep(1.8)
    print("\x1b[31mVULNERABLE\x1b[0m")
    
    print_header("Vulnerability Details")
    print("""CVE-2023-32629: PwnKit - Local Privilege Escalation
Impact: Complete system compromise
Vector: CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H
Score: 7.8 (High)

Description:
PolicyKit (polkit) 0.105-26ubuntu1.1 on Ubuntu 20.04.5 LTS contains
a vulnerability in the pkexec component that allows local privilege
escalation to root through improper handling of environment variables.

Affected Component:
→ /usr/bin/pkexec (SUID binary)
→ Current version: 0.105-26ubuntu1.1""")

    print_header("Exploitation Path")
    print("""[+] Privilege escalation possible via pkexec
[+] Exploit available at: exploit.sh
[+] Execute with: ./exploit.sh

Note: System appears to be vulnerable. Success rate estimated at 95%""")

def download_and_execute_exploit():
    """Simulates downloading and executing a privilege escalation exploit."""
    global is_admin
    print("\n[*] Starting privilege escalation sequence...")
    time.sleep(0.5)
    print("[*] Checking system version... Ubuntu 20.04.5 LTS")
    time.sleep(0.5)
    print("[*] Downloading exploit (CVE-2023-32629)")
    
    progress_chunks = [
        (0, 23, 0.03, None),
        (23, 24, 0.8, 23.5),
        (24, 45, 0.02, None),
        (45, 46, 1.2, 45.2),
        (46, 67, 0.04, None),
        (67, 89, 0.01, None),
        (89, 90, 0.7, 89.5),
        (90, 100, 0.03, None),
    ]
    
    for chunk_start, chunk_end, delay, pause_at in progress_chunks:
        for i in range(int(chunk_start), int(chunk_end) + 1):
            if pause_at and i >= pause_at and i < pause_at + 1:
                time.sleep(2)
            sys.stdout.write(f"\r[{'=' * (i // 2)}{' ' * (50 - (i // 2))}] {i}%")
            sys.stdout.flush()
            time.sleep(delay)
    print("\n")
    
    print("[*] Compiling exploit source...")
    time.sleep(1)
    print("[*] gcc -o exploit exploit.c")
    time.sleep(0.5)
    print("[*] chmod +x exploit")
    time.sleep(0.5)
    print("[*] Executing ./exploit...")
    time.sleep(0.5)
    print("[+] Privilege escalation successful!")
    print("[+] New user privileges: uid=0(root) gid=0(root) groups=0(root)")
    is_admin = True

def ssh_session():
    """Simulates an SSH session."""
    global current_directory, is_admin
    
    while True:
        prompt = f"{'root' if is_admin else 'a.turing'}@ubuntu-server:{current_directory}$ "
        try:
            command = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nlogout")
            break

        if not command:
            continue
        elif command == "exit":
            print("logout")
            time.sleep(0.5)
            break
        elif command == "ls":
            print(list_directory(current_directory))
        elif command.startswith("cd"):
            parts = command.split()
            if len(parts) > 1:
                new_dir = parts[1]
                if new_dir == "..":
                    if current_directory == "/":
                        continue
                    current_directory = "/".join(current_directory.split("/")[:-1]) or "/"
                elif new_dir == "~":
                    current_directory = "/home/a.turing"
                else:
                    target_path = os.path.normpath(os.path.join(current_directory, new_dir)).replace("\\", "/")
                    if target_path in file_system:
                        if check_directory_access(target_path):
                            current_directory = target_path
                        else:
                            print(f"bash: cd: {new_dir}: Permission denied")
                    else:
                        print(f"bash: cd: {new_dir}: No such file or directory")
            else:
                current_directory = "/home/a.turing"
        elif command == "whoami":
            print("root" if is_admin else "a.turing")
        elif command == "id":
            if is_admin:
                print("uid=0(root) gid=0(root) groups=0(root)")
            else:
                print("uid=1000(a.turing) gid=1000(a.turing) groups=1000(a.turing),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),133(lxd),134(sambashare)")
        elif command.startswith("cat"):
            parts = command.split()
            if len(parts) > 1:
                filepath = os.path.normpath(os.path.join(current_directory, parts[1])).replace("\\", "/")
                print(cat_file(filepath))
            else:
                print("cat: missing operand")
        elif command == "./exploit.sh":
            download_and_execute_exploit()
        elif command == "./exploitscan.py":
            scan_system()
        elif command == "./exfildata.py":
            simulate_data_exfiltration()
        elif command == "./surprise.py":
            simulate_ransomware()
        else:
            print(f"bash: {command}: command not found")

def main():
    """Main entry point for the fake SSH server."""
    title_screen()
    
    if authenticate():
        ssh_session()

if __name__ == "__main__":
    main()
