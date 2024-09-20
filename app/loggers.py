import logging
from logging import config
from colorlog import ColoredFormatter

from app.config import settings

log_level = "DEBUG"

if not settings.is_development:
    log_level = "INFO"

logging_config = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(log_color)s [%(levelname)-8s] %(log_color)s [%(asctime)s] %(message)s",
            "()": ColoredFormatter,
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bold",
            },
        },
    },
    "handlers": {
        "console": {
            "level": log_level,
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "default": {
            "handlers": ["console"],
            "level": log_level,
            "propagate": False,  # Prevent duplicate logging
        },
    },
}

config.dictConfig(config=logging_config)

logger = logging.getLogger("default")
