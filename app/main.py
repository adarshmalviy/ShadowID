from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from redis import RedisError
from tortoise.exceptions import DBConnectionError

from app.routers import (
    auth,
    spotlight_doc,
    health,
    user,
)
from app.config import settings
from app.db.orm_config import generate_schema, init_db, init_tortoise, close_db
from app.loggers import logger
from app.services.redis_service import RedisService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Structured lifespan with detailed logging and error handling for startup and shutdown."""

    try:
        await init_tortoise()
        logger.info("Database connection initialized successfully.")
    except DBConnectionError as db_error:
        logger.error(f"Failed to connect to database: {db_error}")
        raise db_error
    except Exception as e:
        logger.error(f"Unexpected error during database connection: {e}")
        raise e

    try:
        init_db(app)
        await generate_schema()
        logger.info("Database schema generated successfully.")
    except Exception as e:
        logger.error(f"Error generating schema: {e}")
        raise e

    try:
        RedisService.get_instance()
        logger.info("Redis connection initialized successfully.")
    except RedisError as redis_error:
        logger.error(f"Failed to connect to Redis: {redis_error}")
        raise redis_error
    except Exception as e:
        logger.error(f"Unexpected error during Redis initialization: {e}")
        raise e

    yield

    try:
        await close_db()
        logger.info("Database connection closed successfully.")
    except Exception as e:
        logger.error(f"Error during database shutdown: {e}")
        raise e


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
    app.include_router(router=auth.router, prefix="/auth", tags=["auth"])
    app.include_router(router=user.router, prefix="/user", tags=["user"])
    
    if settings.is_development:
        app.include_router(router=spotlight_doc.router, prefix="/sldoc", tags=["sldoc"])


app = create_app()
