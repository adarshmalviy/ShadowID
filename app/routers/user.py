from fastapi import Depends, FastAPI, HTTPException
from app.auth import create_access_token, oauth2_scheme, SECRET_KEY, ALGORITHM
from app.db.models import User
import jwt

app = FastAPI()


@app.post("/register")
async def register_user(seed: str):
    """
    seed: ... (could be from device info, a random string, or user-supplied input)
    """
    # Generate anonymous identifier using seed
    user = User(anonymous_identifier=User().generate_anonymous_identifier(seed))
    await user.save()
    return {
        "anonymous_identifier": user.anonymous_identifier,
        "message": "Registration successful",
    }


@app.post("/token")
async def login(anonymous_identifier: str):
    user = await User.filter(anonymous_identifier=anonymous_identifier).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Create JWT token
    access_token = create_access_token(data={"sub": user.anonymous_identifier})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = await User.filter(anonymous_identifier=identifier).first()
    return user