import time
import random
import sys

ENDPOINTS = [
    {"url": "/login", "method": "POST", "parameter": "username"},
    {"url": "/search?query=", "method": "GET", "parameter": "query"},
    {"url": "/admin/update_title", "method": "POST", "parameter": "site_title"},
]

PAYLOADS = [
    "' OR '1'='1",
    "' UNION SELECT NULL--",
    "' UNION SELECT username, hash FROM users--",
    "'; DROP TABLE users;--",
    "' AND 1=1--",
    "UPDATE site_title SET title='Hacked by SQLi';--", 
    "admin' --",
]

VULNERABLE_ENDPOINTS = {
    "/search?query=": ["' UNION SELECT username, hash FROM users--"],
    "/admin/update_title": ["UPDATE site_title SET title='Hacked by SQLi';--"]
}

def print_banner():
    print("\033[92m")
    print("=" * 80)
    print("Advanced SQLi Vulnerability Scanner v2.0")
    print("Simulating SQL Injection detection for presentation purposes.")
    print("=" * 80)
    print("\033[0m")

def simulate_task(task_name, duration=3):
    print(f"\n[*] {task_name}")
    for i in range(101):
        sys.stdout.write(f"\r Progress: [{'=' * (i // 2)}{' ' * (50 - (i // 2))}] {i}%")
        sys.stdout.flush()
        time.sleep(duration / 100)
    print()

def scan_endpoint(endpoint):
    print(f"\n[INFO] Scanning endpoint: {endpoint['url']} ({endpoint['method']})")
    print(" [*] Testing endpoint availability...")
    time.sleep(random.uniform(1.5, 2.5))  # Add delay for tension

    found_vulns = set()

    for i, payload in enumerate(PAYLOADS):
        print(f" Testing payload: {payload}...")
        time.sleep(random.uniform(1.0, 2.0))

        # Simulate retries for certain payloads
        if random.random() < 0.15:
            print(" [!] Connection timeout, retrying...")
            time.sleep(random.uniform(1.5, 2.5))

        # Simulate detecting vulnerabilities
        is_vulnerable = (
            endpoint["url"] in VULNERABLE_ENDPOINTS and 
            payload in VULNERABLE_ENDPOINTS[endpoint["url"]]
        )

        if is_vulnerable:
            if payload == "' UNION SELECT username, hash FROM users--":
                print("\033[93m[!] SUSPICIOUS: SQL error-based injection detected.\033[0m")
                found_vulns.add(payload)
            elif payload == "UPDATE site_title SET title='Hacked by SQLi';--":
                print("\033[91m[!] VULNERABLE: SQL blind injection confirmed.\033[0m")
                found_vulns.add(payload)
        else:
            print("Not vulnerable")

        if random.random() < 0.3:
            print(" [*] Performing deeper analysis...")
            time.sleep(random.uniform(2.0, 3.0))

    return found_vulns

def run_scanner():
    print_banner()
    time.sleep(1)
    print("[INFO] Starting SQL injection scan...")

    simulate_task("Loading attack patterns", duration=5)
    simulate_task("Compiling detection rules", duration=4)

    print("[*] Initiating WAF (Web Application Firewall) detection")
    time.sleep(random.uniform(1.5, 3.0))
    print("[INFO] No WAF detected. Proceeding with payload testing.")

    confirmed_vulns = {}

    for endpoint in ENDPOINTS:
        vulnerabilities = scan_endpoint(endpoint)
        if vulnerabilities:
            confirmed_vulns[endpoint["url"]] = vulnerabilities

    print("\n[INFO] Scan completed.")

    if confirmed_vulns:
        print("\n[!] Confirmed vulnerabilities:")
        for url, payloads in confirmed_vulns.items():
            print(f"\n Endpoint: {url}")
            for payload in payloads:
                print(f" → Payload: {payload}")
    else:
        print("\n[!] No high-confidence vulnerabilities found")

if __name__ == "__main__":
    try:
        run_scanner()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted")
        print("[!] Results incomplete")
        sys.exit(1)
