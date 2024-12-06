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
        "contents": ["home", "var", "etc"],
        "permissions": {"read": True, "execute": True}
    },
    "/home": {
        "contents": ["a.turing"],
        "permissions": {"read": True, "execute": True}
    },
    "/home/a.turing": {
        "contents": ["notes.txt", "exploitscan.py", "exploit.sh", "exfildata.py", "ransomware.py", "exfil"],
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

current_directory = "/"
is_admin = False

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
    print("[*] Establishing connection to C2 server...")
    print("[+] Connection established: 185.147.xxx.xxx:443")
    print("[*] Scanning /var/data/client_data for sensitive information...")
    print("[+] Found 50 files containing payment data")
    print("[*] Creating encrypted archive...")
    print("    → Compression: xz")
    print("    → Encryption: AES-256")
    
    for i in range(51):
        sys.stdout.write(f"\r[*] Processing files: {i}/50 [{i*2*'='}{(100-i*2)*' '}] {i*2}%")
        sys.stdout.flush()
    
    print("\n\n[+] Archive created: client_data.tar.xz.enc")
    print("[*] Initiating secure transfer...")
    
    total_size = 42.7
    for i in range(101):
        progress = i / 100 * total_size
        speed = random.uniform(1.8, 2.3)
        sys.stdout.write(f"\r[*] Transferring data: {i}% ({speed:.1f} MB/s) - {progress:.1f}/{total_size:.1f} MB")
        sys.stdout.flush()
    
    print("\n\n[+] Transfer complete")
    print("[*] Removing traces...")
    print("[*] Deleting local archive...")
    print("[*] Clearing system logs...")
    print("[*] Removing source files...")
    print("[+] Cleanup complete")
    print("\n[+] Exfiltration successful - 50 files exfiltrated")
    print("[+] Connection terminated")

# Main logic follows...
def simulate_ransomware():
    """Simulates a ransomware attack sequence."""
    if not is_admin:
        print("Permission denied")
        return

    print("\n[*] Initializing ransomware...")
    print("[*] Encrypting files...")
    time.sleep(2)
    print("[*] Writing ransom note...")
    time.sleep(1)
    print("[+] Ransomware complete. All files are encrypted.")

def download_and_execute_exploit():
    """Simulates downloading and executing a privilege escalation exploit."""
    global is_admin
    print("\n[*] Starting privilege escalation sequence...")
    time.sleep(1)
    print("[*] Downloading exploit script...")
    for i in range(101):
        sys.stdout.write(f"\r[{'=' * (i // 2)}{' ' * (50 - (i // 2))}] {i}%")
        sys.stdout.flush()
        time.sleep(0.05)
    print("\n[+] Exploit downloaded successfully.")
    time.sleep(1)
    print("[*] Executing exploit...")
    time.sleep(2)
    print("[+] Privilege escalation successful. You are now root.")
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
        elif command.startswith("./"):
            script_name = command[2:]  # Remove ./
            if script_name in ["exploit.sh", "exploitscan.py", "exfildata.py", "ransomware.py", "exfil"]:
                if script_name == "exploit.sh":
                    download_and_execute_exploit()
                elif script_name == "exploitscan.py":
                    simulate_data_exfiltration()
                elif script_name in ["exfildata.py", "exfil"]:
                    simulate_data_exfiltration()
                elif script_name == "ransomware.py":
                    simulate_ransomware()
            else:
                print(f"bash: {command}: No such file or directory")
        else:
            print(f"bash: {command}: command not found")

def main():
    """Main entry point for the fake SSH server."""
    title_screen()

    if authenticate():
        ssh_session()

if __name__ == "__main__":
    main()
