from fastapi import FastAPI, HTTPException
from app.auth import create_access_token
from app.db.models import User

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
