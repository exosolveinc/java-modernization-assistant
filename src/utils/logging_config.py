import sys
from loguru import logger
from .config import settings

def setup_logging():
    """Configure logging for the application"""
    
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # Add file handler
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 week",
        level="DEBUG",
        format="{time} | {level} | {message}"
    )
    
    logger.info(f"Logging initialized at level {settings.LOG_LEVEL}")
