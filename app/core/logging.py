
import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    logger = logging.getLogger("app")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

        formatter = logging.Formatter(
            fmt="""{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}""",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"app.{name}")

