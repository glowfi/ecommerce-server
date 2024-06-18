from argon2 import PasswordHasher


def get_password_hash(password: str) -> str:
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    ph = PasswordHasher()
    try:
        verified = ph.verify(hashed_password, plain_password)
        return verified
    except Exception as e:
        print(f"Error verifying password: {e}")
        return False
