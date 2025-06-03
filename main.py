import logging

import uvicorn
from src.main import create_app
from src.config import settings

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("uvicorn_main")

app = create_app()
logger.info("app created")

if __name__ == "__main__":
    logger.info("server running")
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )