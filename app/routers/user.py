from app.loggers import logger
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import HttpUrl
from app.auth import create_access_token, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.db.models import User
import jwt

router = APIRouter()


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
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    token: {token_type} {access_token}
    """
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        identifier: str = payload.get("sub")
        if identifier is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    try:

        user = await User.filter(anonymous_identifier=identifier).first()
        return user
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
