from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import (
    spotlight_doc,
    health,
    user,
)
from app.config import settings
from app.db.orm_config import generate_schema, init_db, init_tortoise, close_db
from app.loggers import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for the application."""
    # Initialize database
    try:
        await init_tortoise()
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")

    # await init_tortoise()
    init_db(app=app)
    try:
        await generate_schema()
    except Exception as e:
        logger.error(f"Failed to generate schema: {e}")

    yield

    await close_db()


def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI application."""
    app = FastAPI(
        title="ShadowID",
        description="Privacy Focused Authentication System",
        # Conditionally disable documentation based on IS_DEVELOPMENT
        docs_url="/docs" if settings.is_development else None,
        lifespan=lifespan,
    )

    configure_cors(app)
    register_routers(app)

    return app


def configure_cors(app: FastAPI) -> None:
    """Configures CORS settings for the application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins, customize as needed
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_routers(app: FastAPI) -> None:
    """Registers all the routers for the application."""

    app.include_router(router=health.router, prefix="/health", tags=["health"])
    app.include_router(router=user.router, prefix="/user", tags=["user"])
    
    if settings.is_development:
        # SL Docs
        app.include_router(router=spotlight_doc.router, prefix="/sldoc", tags=["sldoc"])


app = create_app()
