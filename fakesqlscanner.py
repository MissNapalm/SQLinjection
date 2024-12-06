import time
import random
import sys

# Simulated endpoints for testing SQL Injection
ENDPOINTS = [
    {"url": "/search?query=", "method": "GET", "parameter": "query"},
    {"url": "/login", "method": "POST", "parameter": "username"},
    {"url": "/login", "method": "POST", "parameter": "password"},
    {"url": "/admin/update_title", "method": "POST", "parameter": "site_title"},
]

# Simulated payloads
PAYLOADS = [
    "' OR '1'='1",  # Boolean-based SQLi
    "' UNION SELECT NULL--",  # UNION-based SQLi
    "' UNION SELECT username, hash FROM users--",  # Data extraction
    "'; DROP TABLE users;--",  # Malicious intent
    "' AND 1=1--",  # Logical payload
    "UPDATE site_title SET title='Hacked by SQLi';--",  # Defacement payload
]

# Simulated vulnerable endpoints
VULNERABLE_ENDPOINTS = {
    "/search?query=": ["' OR '1'='1", "' UNION SELECT username, hash FROM users--"],
    "/login": ["' OR '1'='1", "' UNION SELECT NULL--"],
    "/admin/update_title": ["UPDATE site_title SET title='Hacked by SQLi';--"],
}

def print_banner():
    """Prints the banner for the fake SQL vulnerability scanner."""
    print("\033[92m")  # Green text
    print("=" * 80)
    print("SQLi Vulnerability Scanner v1.1")
    print("Simulating SQL Injection scanning for educational purposes.")
    print("=" * 80)
    print("\033[0m")  # Reset text color

def scan_endpoint(endpoint):
    """Simulates scanning an endpoint for SQL injection vulnerabilities."""
    print(f"\n[INFO] Scanning endpoint: {endpoint['url']} (Method: {endpoint['method']})")
    time.sleep(1.5)

    for payload in PAYLOADS:
        sys.stdout.write(f"    Testing payload: {payload}... ")
        sys.stdout.flush()
        time.sleep(random.uniform(0.5, 1.5))

        if endpoint["url"] in VULNERABLE_ENDPOINTS and payload in VULNERABLE_ENDPOINTS[endpoint["url"]]:
            print("\033[91mVULNERABLE\033[0m")  # Red text
            print(f"        → Vulnerable to payload: {payload}")
        else:
            print("Not vulnerable")

def progress_bar(task, duration=5):
    """Simulates a progress bar for tasks."""
    print(f"\n[*] {task}")
    for i in range(101):
        time.sleep(duration / 100)
        sys.stdout.write(f"\r    Progress: [{'=' * (i // 2)}{' ' * (50 - (i // 2))}] {i}%")
        sys.stdout.flush()
    print("\n[+] Completed.")

def run_scanner():
    """Main function to simulate the scanner."""
    print_banner()
    time.sleep(2)

    print("[INFO] Initiating SQL Injection vulnerability scan...")
    time.sleep(1)
    progress_bar("Loading payloads", duration=3)

    for endpoint in ENDPOINTS:
        scan_endpoint(endpoint)

    print("\n[INFO] Scan completed.")
    print("[+] Vulnerabilities found on the following endpoints:")
    for endpoint, payloads in VULNERABLE_ENDPOINTS.items():
        print(f"    - {endpoint}")
        for payload in payloads:
            print(f"        → Payload: {payload}")
    print("\n[INFO] Use the extracted data responsibly.")

if __name__ == "__main__":
    run_scanner()
