from pwdlib import PasswordHash

# Initialize the Argon2 hasher
password_hash = PasswordHash.recommended()

# Utility function to hash passwords
def hash_password(password: str) -> str:
    return password_hash.hash(password)