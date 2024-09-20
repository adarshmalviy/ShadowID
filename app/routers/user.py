from fastapi import FastAPI, HTTPException
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
