from datetime import timedelta
from app.loggers import logger
from fastapi import APIRouter, Depends, HTTPException
from app.auth import create_access_token, create_refresh_token
from app.db.models import User
from app.config import settings
import redis
import uuid

router = APIRouter()
r = redis.Redis()


@router.post("/register")
async def register_user(seed: str):
    """
    seed: ... (could be from device info, a random string, or user-supplied input)
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
    try:
        user = await User.filter(anonymous_identifier=anonymous_identifier).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Create JWT token
        access_token = create_access_token(data={"sub": user.anonymous_identifier})
        refresh_token = create_refresh_token(data={"sub": user.anonymous_identifier})
        r.set(
            refresh_token,
            user.anonymous_identifier,
            ex=timedelta(minutes=settings.refresh_token_expiry),
        )
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/token/refresh")
async def refresh_token(refresh_token: str):
    try:
        stored_identifier = r.get(refresh_token)
        
        # Decode bytes to string (if using Redis)
        stored_identifier = stored_identifier.decode("utf-8") # BUG
        
        is_user = await User.get_or_none(anonymous_identifier=stored_identifier)
        if not stored_identifier or not is_user:
            raise HTTPException(status_code=400, detail="Invalid refresh token")

        # Generate new JWT and refresh token
        new_access_token = create_access_token(data={"sub": stored_identifier})
        new_refresh_token = create_access_token(data={"sub": stored_identifier})

        # Store the new refresh token in Redis and delete the old one
        r.set(
            new_refresh_token,
            stored_identifier,
            ex=timedelta(
                minutes=settings.refresh_token_expiry,
            ),
        )
        r.delete(refresh_token)

        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
