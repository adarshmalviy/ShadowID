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
RATE_LIMIT_WINDOW = settings.rate_limiting_window # in sec


def encrypt_data(data: str) -> str:
    """Encrypts the given data using Fernet symmetric encryption."""
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypts the given data."""
    return cipher_suite.decrypt(encrypted_data.encode()).decode()


# Rate-Limiting Functions
def is_rate_limited(identifier: str) -> bool:
    """
    Check if the user is rate-limited by tracking failed attempts within a time window.
    """
    attempts_key = f"login_attempts:{identifier}"
    blocked_key = f"blocked:{identifier}"

    # Check if the user is currently blocked
    blocked_until = r.get(blocked_key)
    if blocked_until and time.time() < float(blocked_until):
        return True

    # Retrieve number of attempts within the rate-limit window
    attempts = r.get(attempts_key)
    if attempts and int(attempts) >= MAX_ATTEMPTS:
        block_user(identifier)
        return True

    return False


def increment_attempts(identifier: str):
    """
    Increment login attempts for the user and apply rate-limiting based on a rolling window.
    """
    attempts_key = f"login_attempts:{identifier}"
    r.incr(attempts_key)
    r.expire(
        attempts_key, RATE_LIMIT_WINDOW
    )  # Expire the key after the rate limit window


def clear_attempts(identifier: str):
    """
    Clear the login attempts for the user after a successful login.
    """
    attempts_key = f"login_attempts:{identifier}"
    blocked_key = f"blocked:{identifier}"
    r.delete(attempts_key)
    r.delete(blocked_key)


def block_user(identifier: str):
    """
    Block the user for a duration that increases with the number of failed attempts.
    Exponential backoff increases block duration after each blocking event.
    """
    blocked_key = f"blocked:{identifier}"
    attempts_key = f"login_attempts:{identifier}"

    # Calculate block duration with exponential backoff
    current_attempts = r.get(attempts_key)
    if not current_attempts:
        current_attempts = 0
    else:
        current_attempts = int(current_attempts)

    backoff_duration = BLOCK_DURATION * (2**current_attempts)

    # Set block duration in Redis
    r.set(blocked_key, time.time() + backoff_duration)
    r.incr(attempts_key)  # Increase failed attempts count
    r.expire(
        attempts_key, RATE_LIMIT_WINDOW
    )  # Reset attempts after the rate limit window
