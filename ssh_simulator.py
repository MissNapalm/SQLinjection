import time
import random
import sys

ENDPOINTS = [
   {"url": "/search?query=", "method": "GET", "parameter": "query"},
   {"url": "/login", "method": "POST", "parameter": "username"},
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
   "/login": ["admin' --"],
   "/admin/update_title": ["UPDATE site_title SET title='Hacked by SQLi';--"]
}

def print_banner():
   print("\033[92m")
   print("=" * 80)
   print("SQLi Vulnerability Scanner v1.1")
   print("Simulating SQL Injection scanning for educational purposes.")
   print("=" * 80)
   print("\033[0m")

def handle_timeout():
   if random.random() < 0.3:
       print(" [!] Connection timeout, retrying...")
       time.sleep(random.uniform(1.5, 3.0))
       return True
   return False

def scan_endpoint(endpoint):
   print(f"\n[INFO] Scanning endpoint: {endpoint['url']} ({endpoint['method']})")
   print(" [*] Testing endpoint availability...")
   if handle_timeout():
       print(" [!] Endpoint unstable, continuing with caution")
   
   found_vulns = set()
   
   for payload in PAYLOADS:
       retry_count = 0
       while retry_count < 3:
           print(f" Testing payload: {payload}...")
           
           if handle_timeout():
               retry_count += 1
               continue
               
           time.sleep(random.uniform(0.5, 1.5))

           is_vulnerable = (endpoint["url"] in VULNERABLE_ENDPOINTS and 
                          payload in VULNERABLE_ENDPOINTS[endpoint["url"]] and
                          random.random() < 0.7)

           if is_vulnerable:
               if random.random() < 0.15:
                   print("\033[93m[!] POTENTIALLY VULNERABLE\033[0m")
               else:
                   print("\033[91m[!] VULNERABLE\033[0m")
                   found_vulns.add(payload)
           else:
               if random.random() < 0.15:
                   print("\033[93m[?] SUSPICIOUS\033[0m")
               else:
                   print("Not vulnerable")
           break
           
       if retry_count == 3:
           print(" [!] Maximum retries reached, skipping")
   
   return found_vulns

def progress_bar(task, duration=5):
   print(f"\n[*] {task}")
   for i in range(101):
       sys.stdout.write(f"\r Progress: [{'=' * (i // 2)}{' ' * (50 - (i // 2))}] {i}%")
       sys.stdout.flush()
       time.sleep(duration / 100)
   print()

def run_scanner():
   print_banner()
   time.sleep(1)
   print("[INFO] Starting SQL injection scan...")
   
   progress_bar("Loading attack patterns", duration=2)
   progress_bar("Compiling detection rules", duration=1)
   
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
   
   print("\n[INFO] Note: False negatives possible. Manual verification recommended.")

if __name__ == "__main__":
   try:
       run_scanner()
   except KeyboardInterrupt:
       print("\n\n[!] Scan interrupted")
       print("[!] Results incomplete")
       sys.exit(1)
