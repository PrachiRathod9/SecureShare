import hashlib
import os
import secrets
from database import db

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2 with SHA-256 and a random salt."""
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${hashed}"

def verify_password(stored_hash: str, password_attempt: str) -> bool:
    """Verifies a password attempt against a stored salt$hash string."""
    try:
        if '$' not in stored_hash:
            return False
        salt, hashed = stored_hash.split('$', 1)
        attempt_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password_attempt.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return secrets.compare_digest(attempt_hash, hashed)
    except Exception:
        return False

def register_user(name: str, email: str, password: str):
    """Registers a new user in the database after validating fields."""
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return False, "All fields are required."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    # Check if email already exists
    existing = db.fetch_one("SELECT user_id FROM users WHERE email = %s", (email,))
    if existing:
        return False, "An account with this email already exists."

    pwd_hash = hash_password(password)
    user_id = db.execute_query(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
        (name, email, pwd_hash)
    )

    # Log activity
    db.execute_query(
        "INSERT INTO activity_logs (user_id, action, filename) VALUES (%s, %s, %s)",
        (user_id, "User Registered Account", "")
    )

    return True, {"user_id": user_id, "name": name, "email": email}

def login_user(email: str, password: str):
    """Authenticates a user and returns user info if credentials are valid."""
    email = email.strip().lower()
    if not email or not password:
        return False, "Please fill in all fields."

    user = db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))
    if not user:
        return False, "Invalid email or password."

    if verify_password(user["password_hash"], password):
        # Log activity
        db.execute_query(
            "INSERT INTO activity_logs (user_id, action, filename) VALUES (%s, %s, %s)",
            (user["user_id"], "User Logged In", "")
        )
        return True, {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"]
        }
    else:
        return False, "Invalid email or password."
