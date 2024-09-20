from datetime import timedelta
from app.loggers import logger
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import HttpUrl
from app.auth import create_access_token, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.db.models import User
import jwt

router = APIRouter()

@router.get("/me")
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


@router.get("/admin")
async def admin_endpoint(token: str = Depends(oauth2_scheme)):
    try:
        
        user = await get_current_user(token)
        if user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return {"message": "Welcome, admin"}
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
