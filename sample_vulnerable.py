
import subprocess
import hashlib

# Example 1: Insecure use of a shell command
def run_command(user_input):
    subprocess.call(user_input, shell=True)

# Example 2: Weak hashing algorithm
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Example 3: Hardcoded secret
API_KEY = "demo_secret_12345"

print("Sample application loaded")
