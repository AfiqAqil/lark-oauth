"""
Centralized logging configuration using loguru.
All modules should import logger from this file.
"""

import sys
import os
from loguru import logger

# Remove default handler
logger.remove()

# Console logging with colors (no HTML-like tags, use loguru's native coloring)
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# File logging for debugging (only if logs directory exists or can be created)
try:
    os.makedirs("logs", exist_ok=True)
    logger.add(
        "logs/lark_oauth.log",
        rotation="10 MB",
        retention="7 days",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )
except (OSError, PermissionError):
    # If we can't create logs directory, just skip file logging
    pass

# Export the configured logger
__all__ = ["logger"] 