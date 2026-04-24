from pwdlib import PasswordHash

# Initialize the Argon2 hasher
password_hash = PasswordHash.recommended()

# Utility function to hash passwords
def hash_password(password: str) -> str:
    return password_hash.hash(password)

# Utility function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)