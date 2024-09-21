from cryptography.fernet import Fernet
from redis import Redis
from app.services.redis_service import RedisService
import time

from app.config import settings

r: Redis = RedisService.get_instance()
# Generate a key for encryption (do this once and store it securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Max login attempts and block duration for rate-limiting
MAX_ATTEMPTS = settings.max_login_attempts
BLOCK_DURATION = settings.login_block_duration  # in sec


def encrypt_data(data: str) -> str:
    """Encrypts the given data using Fernet symmetric encryption."""
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypts the given data."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()


# Rate-Limiting Functions
def is_rate_limited(identifier: str) -> bool:
    """
    Check if the given identifier (user) is rate-limited.
    """
    attempts = r.get(f"login_attempts:{identifier}")

    if attempts and int(attempts) >= MAX_ATTEMPTS:
        blocked_until = r.get(f"blocked:{identifier}")
        if blocked_until and time.time() < float(blocked_until):
            return True

        r.delete(f"login_attempts:{identifier}")
        r.delete(f"blocked:{identifier}")

    return False


def block_user(identifier: str):
    """
    Block the user by storing the block duration in Redis.
    """
    r.set(f"blocked:{identifier}", time.time() + BLOCK_DURATION)
    r.incr(f"login_attempts:{identifier}")
    r.expire(f"login_attempts:{identifier}", BLOCK_DURATION)
