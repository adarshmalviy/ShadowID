from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from app.config import settings
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiry
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expiry


def create_token(data: dict, expiry_minutes: int):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict):
    return create_token(data, ACCESS_TOKEN_EXPIRE_MINUTES)

def create_refresh_token(data: dict):
    return create_token(data, REFRESH_TOKEN_EXPIRE_MINUTES)
