from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.config import settings
from app.loggers import logger


DATABASE_URL = f"postgres://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

logger.debug(f"URL: {DATABASE_URL}")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.db.models",
                # "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )


async def init_tortoise() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    # conn = Tortoise.get_connection("default")
    # print(conn)

    # a = Tortoise.describe_models()
    # print(a)

async def generate_schema() -> None:
    await Tortoise.generate_schemas(safe=True)


async def close_db() -> None:
    await Tortoise.close_connections()
