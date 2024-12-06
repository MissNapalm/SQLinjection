import time
import random
import os
import pyfiglet

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def title_screen():
    """Displays the SarahCrack v1.0 title screen."""
    clear_screen()
    title = pyfiglet.figlet_format("SarahCrack v1.0")
    print(title)
    print("Advanced Hash Cracking Suite - Real Results Guaranteed (Not Really!)")
    print("=" * 80)
    input("Press ENTER to start...\n")

def realistic_progress(message, duration=2):
    """Simulates a realistic progress bar for cracking."""
    print(f"{message}...")
    for _ in range(20):
        time.sleep(duration / 20)
        print("█", end="", flush=True)
    print(" Done!")

def fake_crack(hash_to_crack):
    """Simulates cracking a hash with realistic steps."""
    clear_screen()
    print(f"Target hash: {hash_to_crack}")
    print("Cracking initiated. Please wait...\n")
    
    # Simulate hash identification
    time.sleep(1)
    hash_types = ["MD5", "SHA-1", "SHA-256", "bcrypt"]
    identified_type = random.choice(hash_types)
    print(f"[INFO] Detected hash type: {identified_type}\n")
    time.sleep(1)

    # Simulate realistic cracking steps
    steps = [
        "[STEP 1/5] Initializing attack vectors",
        "[STEP 2/5] Loading dictionaries",
        "[STEP 3/5] Performing brute force attack",
        "[STEP 4/5] Analyzing hash entropy",
        "[STEP 5/5] Finalizing decryption"
    ]

    for step in steps:
        realistic_progress(step, random.uniform(1, 2))

    # Special case: Known hash to resolve to "password123"
    if hash_to_crack == "482c811da5d5b4bc6d497ffa98491e38":
        cracked_password = "password123"
    else:
        # Generate a fake random password
        cracked_password = "".join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=random.randint(6, 12)))

    # Display the "cracked" result
    print("\n[RESULT] Password successfully cracked!")
    print(f"Hash: {hash_to_crack}")
    print(f"Password: {cracked_password}")
    print("=" * 80)

def main():
    title_screen()
    
    while True:
        clear_screen()
        print("Enter a hash to crack (or type 'exit' to quit):")
        user_input = input("> ").strip()
        
        if user_input.lower() == "exit":
            print("\nThank you for using SarahCrack v1.0. Stay safe!")
            break
        elif len(user_input) < 8:  # Simulate a basic hash validation
            print("Error: Invalid hash format. Please try again.")
            time.sleep(2)
        else:
            fake_crack(user_input)
            input("\nPress ENTER to crack another hash or type 'exit' next time.\n")

if __name__ == "__main__":
    main()
