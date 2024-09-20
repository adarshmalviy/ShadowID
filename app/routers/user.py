from app.loggers import logger
from fastapi import APIRouter, Depends, HTTPException
from app.auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from app.db.models import User
import jwt

router = APIRouter()

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current logged-in user details.
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
        if user is None:
            raise credentials_exception
        return user
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/admin")
async def admin_endpoint(token: str = Depends(oauth2_scheme)):
    """
    Restricted endpoint only for admin users.
    """
    try:
        user = await get_current_user(token)
        if user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return {"message": "Welcome, admin"}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
