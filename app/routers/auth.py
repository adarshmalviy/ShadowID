from datetime import timedelta

from redis import Redis
from app.loggers import logger
from fastapi import APIRouter, Depends, HTTPException
from app.auth import create_access_token, create_refresh_token
from app.db.models import User
from app.config import settings
from app.security import encrypt_data, decrypt_data, is_rate_limited, block_user
from app.services.redis_service import RedisService

router = APIRouter()
r: Redis = RedisService.get_instance()


@router.post("/register")
async def register_user(seed: str):
    """
    seed: (could be from device info, a random string, or user-supplied input)
    """
    try:
        # Generate anonymous identifier using seed
        user = User(anonymous_identifier=User().generate_anonymous_identifier(seed))
        await user.save()
        return {
            "anonymous_identifier": user.anonymous_identifier,
            "message": "Registration successful",
        }
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/token")
async def login(anonymous_identifier: str):
    """
    User login with an anonymous identifier. Implements rate-limiting and token generation.
    """
    try:
        # Rate-limiting check
        if is_rate_limited(anonymous_identifier):
            raise HTTPException(
                status_code=429, detail="Too many login attempts. Try again later."
            )

        user = await User.filter(anonymous_identifier=anonymous_identifier).first()
        if not user:
            # Block further attempts for a duration if login fails
            block_user(anonymous_identifier)
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Create JWT token
        access_token = create_access_token(data={"sub": user.anonymous_identifier})
        refresh_token = create_refresh_token(data={"sub": user.anonymous_identifier})

        # Encrypt and store refresh token in Redis
        encrypted_refresh_token = encrypt_data(refresh_token)
        r.set(
            encrypted_refresh_token,
            user.anonymous_identifier,
            ex=timedelta(minutes=settings.refresh_token_expiry),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/token/refresh")
async def refresh_token(refresh_token: str):
    """
    Refresh the JWT access token using a valid refresh token. Implements token rotation.
    """
    try:
        encrypted_refresh_token = encrypt_data(refresh_token)
        stored_identifier = r.get(encrypted_refresh_token)

        if not stored_identifier:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        # Decode bytes to string (if using Redis)
        # stored_identifier = stored_identifier.decode("utf-8") # Currently: Redis response decoding is true

        user = await User.get_or_none(anonymous_identifier=stored_identifier)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        # Generate new JWT and refresh token
        new_access_token = create_access_token(data={"sub": stored_identifier})
        new_refresh_token = create_refresh_token(data={"sub": stored_identifier})

        # Encrypt and store the new refresh token, delete the old one
        encrypted_new_refresh_token = encrypt_data(new_refresh_token)
        r.set(
            encrypted_new_refresh_token,
            stored_identifier,
            ex=timedelta(minutes=settings.refresh_token_expiry),
        )
        r.delete(encrypted_refresh_token)

        return {"access_token": new_access_token, "refresh_token": new_refresh_token}

    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
