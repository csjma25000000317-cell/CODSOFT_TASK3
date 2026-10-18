
import hashlib
import os
import secrets


def hash_password(password):
    """Hash a password using PBKDF2-HMAC-SHA256."""
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )

    return {
        "salt": salt.hex(),
        "password_hash": password_hash.hex(),
    }


# Load secrets from environment variables, not source code.
API_KEY = os.environ.get("API_KEY")

print("Secure sample application loaded.")
